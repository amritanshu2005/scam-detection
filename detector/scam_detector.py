"""Scam Detection Module

Improved heuristic detector using weighted keyword/phrase matching plus
pattern detectors (links, phone numbers, account-like numbers, IMPS refs).
This increases precision and recall for common scam templates while still
being lightweight and explainable.
"""

import re
from typing import List
import os
try:
    import joblib
    from sklearn.feature_extraction.text import TfidfVectorizer
except Exception:
    joblib = None

# Attempt to load a trained model pipeline if present
MODEL_PIPELINE = None
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model_pipeline.joblib')
if joblib and os.path.exists(MODEL_PATH):
    try:
        MODEL_PIPELINE = joblib.load(MODEL_PATH)
        print('[MODEL] Loaded trained model pipeline')
    except Exception as e:
        print(f'[MODEL] Failed to load model pipeline: {e}')


# Weighted keywords: more risky terms have higher weight
WEIGHTED_KEYWORDS = {
    # high-risk tokens
    "otp": 3,
    "one time password": 3,
    "upi": 3,
    "imps": 3,
    "transfered": 3,
    "transferred": 3,
    "credited": 2,
    "debited": 2,
    "account": 2,
    "a/c": 2,
    "account no": 3,
    "ref no": 3,
    "imps ref": 3,
    "call": 1,
    "call immediately": 2,
    "verify": 2,
    "verify now": 3,
    "urgent": 2,
    "immediately": 2,
    "click": 2,
    "click here": 3,
    "link": 2,
    "http://": 3,
    "https://": 3,
    ".com": 1,
    "winner": 2,
    "prize": 2,
    "lottery": 2,
    "refund": 2,
    "suspend": 2,
    "suspended": 2,
    "reactivate": 2,
    "blocked": 2,
    "bank": 2,
    "bank account": 3,
    # Indian context tokens
    "paytm": 2,
    "phonepe": 2,
    "gpay": 2,
    "bhai": 1,
    "sir": 1,
}


PHONE_RE = re.compile(r"\b(?:\+91[\-\s]?)?[6-9]\d{9}\b")
ACCOUNT_RE = re.compile(r"\b\d{9,18}\b")
IMPS_REF_RE = re.compile(r"\bref\s*no\s*[:\-\s]*\d{6,}\b", re.I)
LINK_RE = re.compile(r"https?://[^\s]+|www\.[^\s]+", re.I)


def _score_text(text: str) -> int:
    t = text.lower()
    score = 0

    # Keyword scoring
    for kw, w in WEIGHTED_KEYWORDS.items():
        if kw in t:
            score += w

    # Pattern bonuses
    if LINK_RE.search(text):
        score += 3
    if IMPS_REF_RE.search(text):
        score += 3
    if PHONE_RE.search(text):
        score += 2
    # account-like numbers
    acct_matches = ACCOUNT_RE.findall(text)
    if acct_matches:
        # longer numbers (likely account/IFSC-less account) add more weight
        score += 2 * len(acct_matches)

    return score


def detect(text: str, history: List[dict]) -> bool:
    """Return True if text is likely a scam.

    Heuristic: compute weighted score. If score >= threshold -> scam.
    History can increase confidence if previous messages were flagged.
    """
    try:
        score = _score_text(text)

        # If a trained ML pipeline exists, consult it and combine predictions
        model_flag = False
        if MODEL_PIPELINE is not None:
            try:
                prob = MODEL_PIPELINE.predict_proba([text])[0][1]
                print(f"[MODEL] predicted scam_prob={prob:.3f}")
                model_flag = prob >= 0.5
            except Exception as e:
                print(f"[MODEL] prediction error: {e}")
                model_flag = False

        # If recent history contains scam indicator, increase score
        hist_score = 0
        for h in (history or []):
            if isinstance(h, dict):
                hist_text = h.get("text", "")
            else:
                hist_text = str(h)
            hist_score += _score_text(hist_text) // 2

        total = score + (hist_score // 2)

        # Threshold tuned for recall; start with 3
        threshold = 3

        # If message is very short and has little context, require higher score
        if len(text) < 40:
            threshold = 4

        # Heuristic: if text looks like a victim reporting (first-person pleas),
        # reduce score so we don't mark victim complaints as scams.
        victim_phrases = re.compile(r"\b(i|my|me|not done by me|someone transferred|help me|please help|i am very scared)\b", re.I)
        victim_flag = bool(victim_phrases.search(text))
        if victim_flag:
            print("[DETECT] victim_flag true - reducing score to avoid false positive")
            total = max(0, total - 3)

        # Debug print for visibility during development
        print(f"[DETECT] score={score} hist={hist_score} total={total} threshold={threshold}")

        # Final decision: either the heuristic OR the ML model indicates scam
        if MODEL_PIPELINE is not None:
            return model_flag or (total >= threshold)

        return total >= threshold
    except Exception as e:
        print(f"[DETECT ERROR] {e}")
        return False

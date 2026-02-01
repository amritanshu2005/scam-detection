"""
Scam Detection Module
Advanced scam detection using pattern matching, heuristics, and context analysis
"""

import re
from typing import List, Dict, Any
from collections import Counter


class ScamDetector:
    """Detects scam intent in messages"""
    
    def __init__(self):
        # Scam indicators - patterns that suggest scam intent
        self.scam_patterns = [
            # Financial urgency
            r'\b(urgent|immediate|act now|limited time|expire|suspended|blocked|frozen)\b',
            r'\b(claim|reward|prize|winner|lucky|bonus|refund)\b',
            r'\b(verify|update|confirm|validate|reactivate)\b.*\b(account|card|bank|upi)\b',
            
            # Payment requests
            r'\b(pay|transfer|send money|deposit|fee|charge|payment)\b',
            r'\b(upi|bank account|account number|ifsc|routing)\b',
            
            # Phishing indicators
            r'\b(click here|link|website|portal|login|password)\b',
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            
            # Suspicious requests
            r'\b(otp|verification code|pin|password|credentials)\b',
            r'\b(share|send|provide|give).*\b(details|information|number|id)\b',
            
            # Authority impersonation
            r'\b(bank|government|irs|tax|police|court|legal)\b.*\b(action|notice|case|complaint)\b',
        ]
        
        self.scam_keywords = [
            'scam', 'fraud', 'phishing', 'urgent payment', 'verify account',
            'suspended account', 'win prize', 'claim reward', 'free money',
            'lottery winner', 'tax refund', 'bank verification'
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.scam_patterns]
    
    def detect(self, message: str, conversation_history: List[Dict[str, Any]]) -> bool:
        """
        Advanced scam detection with context awareness and scoring
        
        Args:
            message: Current message to analyze
            conversation_history: Previous messages in conversation
            
        Returns:
            True if scam intent detected, False otherwise
        """
        message_lower = message.lower()
        score = 0.0
        
        # 1. Explicit scam keywords (high weight)
        keyword_matches = sum(1 for keyword in self.scam_keywords if keyword in message_lower)
        if keyword_matches > 0:
            score += 0.4 * keyword_matches
        
        # 2. Pattern matching (medium weight)
        pattern_matches = sum(1 for pattern in self.compiled_patterns if pattern.search(message))
        score += 0.25 * pattern_matches
        
        # 3. Urgency indicators (medium weight)
        urgency_words = ['urgent', 'immediate', 'asap', 'now', 'today', 'within', 'hours', 'minutes']
        urgency_count = sum(1 for word in urgency_words if word in message_lower)
        if urgency_count >= 2:
            score += 0.3
        
        # 4. Financial data requests (high weight)
        financial_patterns = [
            r'\b\d{9,18}\b',  # Account numbers
            r'\b(account|bank|upi|ifsc|routing)\s*(?:no|number|#|id)?\s*:?\s*\d+',
            r'upi://',
            r'paytm|phonepe|gpay|bhim',
        ]
        financial_matches = sum(1 for pattern in financial_patterns if re.search(pattern, message, re.IGNORECASE))
        if financial_matches > 0:
            score += 0.35
        
        # 5. Suspicious URL patterns (high weight)
        url_patterns = [
            r'http[s]?://[^\s]+',
            r'www\.[^\s]+',
            r'bit\.ly|tinyurl|short\.link|t\.co',
        ]
        suspicious_urls = sum(1 for pattern in url_patterns if re.search(pattern, message, re.IGNORECASE))
        if suspicious_urls > 0:
            score += 0.3
        
        # 6. Context analysis from conversation history
        if len(conversation_history) > 0:
            recent_messages = conversation_history[-5:]  # Last 5 messages
            recent_text = " ".join([msg.get("content", "") for msg in recent_messages])
            
            # If previous messages had scam indicators
            context_patterns = sum(1 for pattern in self.compiled_patterns if pattern.search(recent_text))
            if context_patterns > 0:
                score += 0.2
        
        # 7. Authority impersonation (high weight)
        authority_patterns = [
            r'\b(bank|government|irs|tax|police|court|legal|rbi|income tax)\b',
            r'\b(official|authorized|mandatory|required|compulsory)\b',
        ]
        authority_matches = sum(1 for pattern in authority_patterns if re.search(pattern, message, re.IGNORECASE))
        if authority_matches >= 2:
            score += 0.4
        
        # 8. Request for sensitive information (high weight)
        sensitive_patterns = [
            r'\b(share|send|provide|give|submit).*\b(account|password|pin|otp|credentials|details)',
            r'\b(verify|confirm|validate).*\b(account|card|bank|upi|identity)',
        ]
        sensitive_matches = sum(1 for pattern in sensitive_patterns if re.search(pattern, message, re.IGNORECASE))
        if sensitive_matches > 0:
            score += 0.35
        
        # Threshold: Score >= 0.6 indicates scam
        return score >= 0.6
    
    def get_confidence_score(self, message: str, conversation_history: List[Dict[str, Any]] = None) -> float:
        """
        Get confidence score for scam detection (0.0 to 1.0)
        
        Args:
            message: Message to analyze
            conversation_history: Optional conversation history for context
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        if conversation_history is None:
            conversation_history = []
        
        # Use the same detection logic but return the score
        message_lower = message.lower()
        score = 0.0
        
        # Calculate score using same logic as detect()
        keyword_matches = sum(1 for keyword in self.scam_keywords if keyword in message_lower)
        score += 0.4 * min(keyword_matches, 2)  # Cap at 2
        
        pattern_matches = sum(1 for pattern in self.compiled_patterns if pattern.search(message))
        score += 0.25 * min(pattern_matches, 3)  # Cap at 3
        
        urgency_words = ['urgent', 'immediate', 'asap', 'now', 'today']
        urgency_count = sum(1 for word in urgency_words if word in message_lower)
        if urgency_count >= 2:
            score += 0.3
        
        financial_patterns = [r'\b\d{9,18}\b', r'upi://', r'paytm|phonepe']
        if any(re.search(p, message, re.IGNORECASE) for p in financial_patterns):
            score += 0.35
        
        if re.search(r'http[s]?://', message, re.IGNORECASE):
            score += 0.3
        
        # Normalize to 0-1 scale
        return min(1.0, score)


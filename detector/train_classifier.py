"""
Train a TF-IDF + LogisticRegression classifier using labeled examples in data/examples.csv
Saves a pipeline to detector/model_pipeline.joblib
"""
import os
import csv
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / 'data' / 'examples.csv'
MODEL_PATH = Path(__file__).resolve().parent / 'model_pipeline.joblib'

def load_examples():
    examples = []
    labels = []
    if not DATA_FILE.exists():
        print('No examples.csv found at', DATA_FILE)
        return examples, labels
    with open(DATA_FILE, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 3: continue
            _ts, label, text = row[0], row[1].strip().lower(), row[2]
            if label not in ('scam','legit'): continue
            examples.append(text)
            labels.append(1 if label=='scam' else 0)
    return examples, labels

if __name__ == '__main__':
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import classification_report
        import joblib
    except Exception as e:
        print('Missing training dependencies. Install scikit-learn and joblib.')
        raise

    X, y = load_examples()
    if not X:
        print('No training examples found. Use detector/collect_examples.py to add examples.')
        raise SystemExit(1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1,2), max_features=20000)),
        ('clf', LogisticRegression(class_weight='balanced', max_iter=1000))
    ])

    print('Training classifier on', len(X_train), 'examples...')
    pipeline.fit(X_train, y_train)

    print('Evaluating...')
    preds = pipeline.predict(X_test)
    print(classification_report(y_test, preds))

    joblib.dump(pipeline, MODEL_PATH)
    print('Saved model pipeline to', MODEL_PATH)

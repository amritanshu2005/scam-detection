"""
Simple helper to collect labeled examples for future model training.
Run as a script to append examples to `data/examples.csv`.
"""
import os
import csv
from datetime import datetime

ROOT = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT, "..", "data")
EXAMPLES_FILE = os.path.join(DATA_DIR, "examples.csv")

os.makedirs(DATA_DIR, exist_ok=True)

def append_example(text: str, label: str):
    """Append a labeled example. label should be 'scam' or 'legit'."""
    with open(EXAMPLES_FILE, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.utcnow().isoformat(), label, text])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', choices=['scam', 'legit'], required=True)
    parser.add_argument('--text', required=True)
    args = parser.parse_args()
    append_example(args.text, args.label)
    print(f"Appended example as {args.label}")

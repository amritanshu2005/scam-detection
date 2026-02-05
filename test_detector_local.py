from detector.scam_detector import detect

examples = [
    ("Sir! Someone transferred MY money?? Not done by me sir! What do I do!! I am very scared! Please help me!", False),
    ("Dear Customer, Your a/c no. XXXXXXXXX6904 is credited by Rs.864.00 on 02-02-26 by a/c linked to mobile 7XXXXXX968-RAKESH BHOI (IMPS Ref no 603300989312).If not done by you, call 1800111109. -SBI", True),
    ("Congratulations! You won a prize. Click here http://win.example.com to claim.", True),
    ("Lunch at 1pm? Let's meet.", False),
    ("Verify your UPI 98765@bank immediately to avoid suspension.", True),
]

for text, expected in examples:
    result = detect(text, [])
    print(f"TEXT: {text[:80]!r}...\n DETECTED: {result} (expected {expected})\n")

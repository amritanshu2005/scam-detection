#!/usr/bin/env python
"""Test improved agent responses"""
from agent.agent import generate_reply

# Test with the actual scam message from the screenshot
scam_msg = 'Dear Customer, Your a/c no. XXXXXXXX6904 is credited by Rs.864.00 on 02-02-26 by a/c linked to mobile 7XXXXXX968-RAKESH BHOI (IMPS Ref no 603300989312).If not done by you, call 1800111109.-SBI'

print('=== Scammer message ===')
print(scam_msg)
print('\n=== Agent response ===')
reply = generate_reply(scam_msg, [])
print(f'"{reply}"\n')

# Test more scam types
test_messages = [
    'Your account is blocked! Verify immediately!',
    'Click this link to verify UPI: http://example.com',
    'Send your bank account number now!',
    'Enter your OTP code immediately!',
]

print('=== More test cases ===\n')
for msg in test_messages:
    reply = generate_reply(msg, [])
    print(f'Scammer: {msg}')
    print(f'Agent:   "{reply}"\n')

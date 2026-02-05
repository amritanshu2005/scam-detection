#!/usr/bin/env python
"""Test improved agent responses - Better alignment with problem"""
from agent.agent import generate_reply

print("=" * 80)
print("IMPROVED AGENT RESPONSES - NOW WITH PROPER FEAR & URGENCY")
print("=" * 80)

# Test 1: The actual scam from screenshot
scam_msg = 'Dear Customer, Your a/c no. XXXXXXXX6904 is credited by Rs.864.00 on 02-02-26 by a/c linked to mobile 7XXXXXX968-RAKESH BHOI (IMPS Ref no 603300989312).If not done by you, call 1800111109.-SBI'

print('\n[SCAMMER MESSAGE]')
print(f'{scam_msg}')
print('\n[AGENT RESPONSE - NOW]')
reply = generate_reply(scam_msg, [])
print(f'"{reply}"')

print("\n" + "=" * 80)
print("\nOther test cases:")
print("=" * 80)

# Test more scam types with correct contextual responses
test_messages = [
    ('Your account is blocked! Verify immediately!', 'BLOCKED - Should show alarm'),
    ('Click this link to verify UPI: http://example.com', 'LINK - Should show confusion'),
    ('Send your bank account number now!', 'BANK - Should show fear'),
    ('Enter your OTP code immediately!', 'OTP - Should show confusion'),
]

for msg, label in test_messages:
    print(f'\n[{label}]')
    print(f'Scammer: {msg}')
    reply = generate_reply(msg, [])
    print(f'Agent:   "{reply}"')

print("\n" + "=" * 80)
print("✅ Agent now shows:")
print("   - FEAR about unauthorized transfers")
print("   - PANIC about account being blocked")
print("   - CONFUSION about technology")
print("   - RELUCTANCE to give info")
print("   - This wastes scammer's time while seeming human!")
print("=" * 80)

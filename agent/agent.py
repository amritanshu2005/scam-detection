def generate_reply(message, history):
    turn = len(history)

    if turn == 0:
        return "Why will my account be blocked? I am scared."

    if turn < 4:
        return "I don't understand this properly. Can you explain again?"

    if turn < 7:
        return "I tried but it is asking for UPI ID. Which one should I send?"

    if turn < 10:
        return "This is not working. Can you send bank details instead?"

    return "I will go to bank tomorrow, phone is confusing."

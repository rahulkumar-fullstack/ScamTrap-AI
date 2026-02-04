import random

AGENT_RESPONSES = [
    "Why is my account being suspended?",
    "I didn’t receive any warning before. What happened?",
    "Can you explain what I did wrong?",
    "This sounds serious… what should I do?",
    "I’m worried. How can I fix this?",
    "Is this about my bank account?",
    "I don’t understand. Please explain.",
    "Are you sure this is urgent?",
    "What verification do you need?",
    "I just want to fix the issue quickly."
]


def generate_reply() -> str:
    return random.choice(AGENT_RESPONSES)

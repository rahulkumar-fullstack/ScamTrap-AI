import re
from collections import defaultdict


UPI_REGEX = r"\b[\w.-]+@[\w.-]+\b"
PHONE_REGEX = r"\+?\d{10,13}"
URL_REGEX = r"https?://[^\s]+"

SUSPICIOUS_KEYWORDS = [
    "urgent",
    "verify",
    "account blocked",
    "otp",
    "suspended",
    "payment",
    "click now",
    "act now",
    "limited time",
    "confirm identity",
    "password reset",
    "security alert",
    "unusual activity",
    "login attempt",
    "verify account",
    "update information",
    "bank alert",
    "wire transfer",
    "invoice attached",
    "pending transaction",
    "claim prize",
    "free gift",
    "lottery winner",
    "tax refund",
    "refund pending",
    "delivery failed",
    "reconfirm details",
    "unlock account",
    "reactivate account",
    "account compromised",
    "fraud alert",
    "final notice",
    "legal action",
    "court notice",
    "ssn suspended",
    "identity verification",
    "confirm payment",
    "reset immediately",
    "time sensitive",
    "confidential request",
    "do not ignore",
    "click link",
    "open attachment",
    "download form"
]


async def extract_intelligence(messages: list[dict]) -> dict:
    intelligence = defaultdict(set)

    for msg in messages:
        text = msg["text"].lower()

        # UPI IDs
        upi_matches = re.findall(UPI_REGEX, text)
        intelligence["upiIds"].update(upi_matches)

        # Phone numbers
        phone_matches = re.findall(PHONE_REGEX, text)
        intelligence["phoneNumbers"].update(phone_matches)

        # URLs
        url_matches = re.findall(URL_REGEX, text)
        intelligence["phishingLinks"].update(url_matches)

        # Keywords
        for word in SUSPICIOUS_KEYWORDS:
            if word in text:
                intelligence["suspiciousKeywords"].add(word)

    return {
        "bankAccounts": [],
        "upiIds": list(intelligence["upiIds"]),
        "phishingLinks": list(intelligence["phishingLinks"]),
        "phoneNumbers": list(intelligence["phoneNumbers"]),
        "suspiciousKeywords": list(intelligence["suspiciousKeywords"])
    }

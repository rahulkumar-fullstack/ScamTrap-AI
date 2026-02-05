import re

UPI_REGEX = r"\b[\w.-]+@[\w.-]+\b"
PHONE_REGEX = r"\+?\d{10,13}"
LINK_REGEX = r"https?://[^\s]+"

SUSPICIOUS_KEYWORDS = [
    "urgent",
    "verify",
    "blocked",
    "suspended",
    "otp",
    "payment",
    "account",
]


def extract_intelligence(text: str):
    upi_ids = re.findall(UPI_REGEX, text)
    phones = re.findall(PHONE_REGEX, text)
    links = re.findall(LINK_REGEX, text)

    keywords = [
        word for word in SUSPICIOUS_KEYWORDS
        if word.lower() in text.lower()
    ]

    return {
        "upiIds": list(set(upi_ids)),
        "phoneNumbers": list(set(phones)),
        "phishingLinks": list(set(links)),
        "suspiciousKeywords": list(set(keywords)),
    }

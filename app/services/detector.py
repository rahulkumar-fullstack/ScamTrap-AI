from sentence_transformers import SentenceTransformer, util
from app.core.config import settings
import asyncio

# Load model once at startup
model = SentenceTransformer(settings.minilm_model)

# Define scam patterns to detect
SCAM_PATTERNS = [
    # Bank / account threats
    "Your bank account will be blocked",
    "Your account has been suspended verify now",
    "Unauthorized login detected confirm immediately",
    "Your account storage is full verify password now",
    "Aadhaar linked account flagged urgent update required",
    "Login attempt detected confirm identity now",

    # UPI / payment fraud
    "Share your UPI ID to prevent account freeze",
    "Refund pending send OTP to receive money",
    "Payment failed click to retry",
    "Fake refund sent send back money to receive refund",
    "Instant investment profits transfer now to get payout",

    # Phishing urgency
    "Urgent action required verify identity",
    "Click link to secure your account",
    "Final warning respond immediately",
    "Update your security settings to avoid suspension",
    "Confirm transaction details immediately",

    # Fake offers and retail impersonation
    "You won a lottery claim prize now",
    "Congratulations you are selected for reward",
    "Free gift waiting confirm details",
    "Exclusive festive gift inside open link to claim",
    "Limited time deal just for you click now",

    # Government / official impersonation
    "KYC verification required avoid penalty",
    "Income tax notice immediate action",
    "SIM card will be blocked update Aadhaar",
    "Cybercrime notice account under investigation follow link",

    # Delivery and shopping scams
    "Package delivery failed update address",
    "Courier on hold pay clearance fee",
    "Your parcels are waiting click to reschedule delivery",
    "Fake discount code for Prime Day shoppers",
    "Unpaid shipping fee click link to pay",

    # Job and opportunity scams
    "Work from home earn daily guaranteed",
    "Processing fee required for job confirmation",
    "Instant job offer pay small fee to apply",

    # AI and impersonation / social engineering
    "Boss needs urgent transfer before meeting",
    "Support agent fixing payment issue share details",
    "Deepfake voice call urgent money request",
    "Loved one in trouble send money immediately",

    # Smishing and SMS based
    "Unpaid toll fee pay now to avoid fine",
    "Security alert verify your account via link",
    "Package delivery could not be completed update info",

    # QR and malicious link traps
    "Scan this QR code to confirm identity",
    "QR code failed scan to fix now",
    "Download greeting to view your personalized message"
]

# Precompute embeddings for scam patterns
PATTERN_EMBEDDINGS = model.encode(SCAM_PATTERNS, convert_to_tensor=True)

async def is_scam(message: str, threshold: float = 0.7) -> bool:
    loop = asyncio.get_event_loop()

    # Encode incoming message off main thread
    message_embedding = await loop.run_in_executor(
        None,
        lambda: model.encode(message, convert_to_tensor=True)
    )

    similarities = util.cos_sim(message_embedding, PATTERN_EMBEDDINGS)
    max_similarity = similarities.max().item()

    return max_similarity >= threshold



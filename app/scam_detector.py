from sentence_transformers import SentenceTransformer, util

# Load MiniLM model once (global)
model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    cache_folder="./models"
)

# Some Known scam patterns
SCAM_PATTERNS = [
    "verify your bank account immediately",
    "urgent action required",
    "your account will be blocked",
    "share your OTP",
    "confirm your UPI details",
    "payment failed retry now",
    "click this link to verify",
    "suspend your account today"
]

pattern_embeddings = model.encode(SCAM_PATTERNS, convert_to_tensor=True)


def is_scam(message: str, threshold: float = 0.55) -> bool:
    message_embedding = model.encode(message, convert_to_tensor=True)

    similarities = util.cos_sim(message_embedding, pattern_embeddings)

    max_score = similarities.max().item()

    return max_score > threshold

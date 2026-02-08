from sentence_transformers import SentenceTransformer, util
from app.models.model import get_model
import asyncio

# Get the loaded model instance
model = get_model()

# Define scam patterns to detect
SCAM_PATTERNS = [
    # Bank / account threats
    "Your bank account will be blocked",
    "Your account has been suspended verify now",
    "Unauthorized login detected confirm immediately",
    "Your account storage is full verify password now",
    "Aadhaar linked account flagged urgent update required",
    "Login attempt detected confirm identity now",
    "Verify your account to avoid lockout",
    "Deactivate alert: confirm your credentials",
    "We noticed suspicious activity on your account",
    "Confirm recent transaction to prevent closure",
    "Account access restricted click to restore",
    "Password reset required to avoid suspension",
    "Re-verify your account within 24 hours",
    "Your account has been temporarily frozen",
    "Security breach detected change password now",

    # UPI / payment fraud
    "Share your UPI ID to prevent account freeze",
    "Refund pending send OTP to receive money",
    "Payment failed click to retry",
    "Fake refund sent send back money to receive refund",
    "Instant investment profits transfer now to get payout",
    "Send OTP to claim your refund",
    "Transfer immediately to secure your refund",
    "Provide bank details to receive transfer",
    "Pay small fee to release funds",
    "Confirm UPI PIN to complete refund",

    # Phishing urgency
    "Urgent action required verify identity",
    "Click link to secure your account",
    "Final warning respond immediately",
    "Update your security settings to avoid suspension",
    "Confirm transaction details immediately",
    "This is your final reminder act now",
    "Immediate verification required to avoid penalty",
    "Security update required click here",
    "Verify now or account will be deleted",

    # Fake offers and retail impersonation
    "You won a lottery claim prize now",
    "Congratulations you are selected for reward",
    "Free gift waiting confirm details",
    "Exclusive festive gift inside open link to claim",
    "Limited time deal just for you click now",
    "Claim your exclusive coupon before it expires",
    "Activate your voucher to get discount",
    "Click to reveal secret discount code",
    "Claim free trial - provide card to continue",
    "Your order is ready for pickup click to confirm",

    # Government / official impersonation
    "KYC verification required avoid penalty",
    "Income tax notice immediate action",
    "SIM card will be blocked update Aadhaar",
    "Cybercrime notice account under investigation follow link",
    "Tax refund pending verify bank details",
    "Court summons open link to view",
    "Notice from the Revenue Department respond now",
    "Government grant approved submit details",
    "National ID verification required immediately",
    "Visa application incomplete update now",

    # Delivery and shopping scams
    "Package delivery failed update address",
    "Courier on hold pay clearance fee",
    "Your parcels are waiting click to reschedule delivery",
    "Fake discount code for Prime Day shoppers",
    "Unpaid shipping fee click link to pay",
    "Delivery attempt failed confirm new delivery time",
    "Pay customs duty to release parcel",
    "Missed delivery collect by paying fee",
    "Parcel returned to sender pay to redeliver",
    "Verify your delivery to avoid return",

    # Job and opportunity scams
    "Work from home earn daily guaranteed",
    "Processing fee required for job confirmation",
    "Instant job offer pay small fee to apply",
    "You are hired start immediately pay orientation fee",
    "Become a mystery shopper send purchase receipts",
    "Send bank details to receive salary advance",
    "Apply now for guaranteed placement pay registration",
    "Freelance role - pay deposit to secure job",
    "Zero experience jobs pay training fee",
    "Receive commission for small upfront payment",

    # AI and impersonation / social engineering
    "Boss needs urgent transfer before meeting",
    "Support agent fixing payment issue share details",
    "Deepfake voice call urgent money request",
    "Loved one in trouble send money immediately",
    "I'm stuck abroad send money to help",
    "Urgent: call me back or transfer immediately",
    "Friend's account compromised send code to help",
    "Trust me I'm from IT - provide login details",
    "Manager requests immediate payroll change transfer now",
    "Employee verification required provide SSN",

    # Smishing and SMS based
    "Unpaid toll fee pay now to avoid fine",
    "Security alert verify your account via link",
    "Package delivery could not be completed update info",
    "Reply YES to confirm your identity",
    "Press 1 to speak to an agent about this charge",
    "Text BACK with your OTP to refund",
    "SMS: urgent - verify card to avoid chargeback",
    "Reply STOP to unsubscribe - confirm identity first",
    "You have a new voicemail click to listen",
    "Dial this number to claim your prize",

    # QR and malicious link traps
    "Scan this QR code to confirm identity",
    "QR code failed scan to fix now",
    "Download greeting to view your personalized message",
    "Scan to pay to receive cashback",
    "Scan to view your parcel location",
    "Open the link in browser to verify your account",
    "Tap to install the security update QR",
    "Scan now to win instant reward",

    # Additional patterns — crypto, investments, loans, travel, subscriptions, tech support
    "Guaranteed returns no risk invest now",
    "Crypto airdrop - click to claim free tokens",
    "Withdraw your bonus - confirm wallet private key",
    "Send crypto to verify your account",
    "Low-risk high-yield investment send money now",
    "Loan approved instant transfer - pay processing fee",
    "Student loan relief requires admin fee",
    "Mortgage assistance pay to unlock lower rate",
    "Book your travel voucher claim before expiry",
    "Confirm payment to secure low fare",
    "Subscription renewal failed update payment details",
    "Your streaming account will be cancelled update now",
    "Install this app to continue service",
    "Tech support alert: virus found click to remove",
    "Call support now to avoid data loss",
    "Remote access required to fix your computer",
    "Update required: install attachment to secure device",

    # Romance / social scams
    "I love you, send money to help with emergency",
    "Send money so I can visit you",
    "Romantic partner stranded abroad needs cash",
    "Help me pay medical bills I'll repay later",
    "Trust me I'm real - send gift card",

    # Charity / donation scams
    "Support disaster victims donate now",
    "Verified charity - send donation via link",
    "Help a child in need click to donate",
    "Charity registration pending confirm bank details",

    # Invoice / business email compromise (BEC)
    "Urgent invoice attached please pay now",
    "Final invoice overdue immediate payment required",
    "Change vendor bank details for upcoming payment",
    "Please confirm wire transfer details ASAP",
    "New payment instructions from CEO - comply urgently",

    # Misc common short SMS/call lines
    "Your verification code is 123456 share it to verify",
    "Send the code to complete login",
    "Don't ignore this message reply immediately",
    "Open attachment to view important document",
    "Click here to view account statement",
    "You have an unpaid bill settle now",
    "Act now to avoid service interruption",

    # Education / scholarship and prize
    "You've been awarded a scholarship claim it now",
    "Prize notification: claim your iPhone by paying fee",
    "You are a winner of our gift hamper confirm details",

    # Rental / real estate scams
    "Rent your property for quick cash send deposit",
    "Pay security deposit to reserve the apartment",
    "Landlord abroad needs transfer to secure lease",

    # Safety-net / recovery shims (phrases that ask for codes or to bypass auth)
    "Send the verification code to recover account",
    "Share your one-time password to complete check",
    "Confirm 2FA code to proceed with refund",
    "Please forward the SMS code to our agent",

    # Misc variations / casual language
    "Hey, I need quick help, can you send money?",
    "Open this urgent message from bank",
    "You have an unpaid tax bill click for details",
    "Confirm your PAN card to avoid fine",
    "Activate account by verifying mobile number",
    "Coupon activated - provide card to charge shipping"
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



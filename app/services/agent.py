from sentence_transformers import util
import random
import asyncio
from app.services.detector import model 

INTENT_PATTERNS = {
    "otp_request": [
        "Send OTP now",
        "Share the verification code",
        "Tell me the security code",
        "Please send the OTP",
        "Resend the verification code",
        "What's the one-time password?",
        "Give me the 6-digit code",
        "Text me the authentication code",
        "Email the verification code to me",
        "Provide the MFA code",
        "I didn't get the OTP, resend it",
        "Paste the OTP here",
        "Forward the SMS code",
        "I need the login code right now",
        "Enter the verification pin for me",
        "Send the auth code immediately",
        "Read me the OTP you received",
        "Type the code you got by SMS",
        "Confirm the login code",
        "What code did you just receive?"
    ],

    "urgency_threat": [
        "Account will be blocked immediately",
        "Final warning respond now",
        "Urgent action required",
        "Your account will be suspended",
        "Respond within 24 hours or lose access",
        "Final notice: take action now",
        "Failure to act will result in termination",
        "Immediate response required — this is your last chance",
        "Comply now or consequences will follow",
        "Deadline today, respond ASAP",
        "We will escalate this unless you reply",
        "Act now to avoid penalties",
        "Immediate compliance required",
        "This is your final opportunity",
        "Time sensitive — respond now",
        "Critical alert: act immediately",
        "Last reminder before shutdown",
        "Service will be disabled today",
        "Emergency action needed",
        "Reply instantly to avoid lockout"
    ],

    "payment_request": [
        "Send money to this account",
        "Transfer payment immediately",
        "Pay processing fee now",
        "Wire funds to this account",
        "Pay the invoice now",
        "Complete payment to release order",
        "Make a transfer to the following account",
        "Send remittance immediately",
        "Deposit the fee to avoid service disruption",
        "Charge my card now",
        "Authorize payment of $<AMOUNT>",
        "You need to pay the outstanding balance",
        "Transfer $X to settle this",
        "Send payment today",
        "Clear the dues immediately",
        "Urgent bank transfer required",
        "Pay to confirm your account",
        "Submit payment proof now",
        "Send advance payment",
        "Complete the transaction now"
    ],

    "phishing_link": [
        "Click this link to verify",
        "Open this website now",
        "Login using this link",
        "Verify your account here: <LINK>",
        "Reset password by clicking this URL",
        "Authenticate via this link",
        "Confirm billing details at this website",
        "Use this short link to verify identity",
        "Open the attachment or follow the link",
        "Sign in here to avoid suspension",
        "Visit this secure portal",
        "Click here to confirm details",
        "Follow this link immediately",
        "Use the link below to login",
        "Tap this link to continue",
        "Secure your account here",
        "Open the verification page",
        "Access your account using this URL"
    ],

    "sensitive_info_request": [
        "Send me your password",
        "What's your PIN?",
        "Give me your SSN",
        "Share your bank account number",
        "Provide credit card number and CVV",
        "What's your mother's maiden name?",
        "Upload your passport or ID scan",
        "Share the secret answer to your account",
        "Send the API token/private key",
        "I need your login credentials",
        "Tell me your security answers",
        "Share your personal details",
        "Provide your identity number",
        "Send your card details",
        "Give me your login email and password"
    ],

    "impersonation_support": [
        "I'm calling from IT, reset your password now",
        "This is Amazon support — confirm payment info",
        "Bank security here, verify your account",
        "Support agent requesting your credentials",
        "I'm from HR, send your details for payroll",
        "IT Admin: provide your MFA code",
        "Customer care asking for account password",
        "Company security team contacting you",
        "Official support message — respond",
        "Admin requesting urgent verification"
    ],

    "malicious_attachment": [
        "Open the attached invoice",
        "See attached document to proceed",
        "Download the file to view details",
        "Please open the attachment and enable macros",
        "The invoice is attached — run it",
        "Extract the zip and run the installer",
        "Open the attached payment receipt",
        "Review the attached statement",
        "Run the attached security update",
        "Open attachment for urgent info"
    ],

    "reward_or_prize": [
        "You won a prize, claim now",
        "Click here to receive your gift card",
        "Congratulations — you've been selected",
        "Claim your reward by verifying your details",
        "Free voucher if you confirm your account",
        "Win a $1000 gift card — click to claim",
        "You are today's lucky winner",
        "Claim your bonus reward now",
        "Exclusive reward waiting for you",
        "Redeem your prize immediately"
    ],

    "social_engineering": [
        "I'm the CEO, approve this payment immediately",
        "Can you urgently transfer funds for me?",
        "Help me move money to this vendor",
        "Approve this transaction — I need it done now",
        "Do this favor: wire money to this account",
        "Handle this confidential payment",
        "Process this request quietly",
        "Urgent executive request",
        "Send funds on my behalf",
        "This must stay confidential"
    ],

    "account_recovery": [
        "I can't access my account, reset it",
        "Bypass MFA and recover my account",
        "I lost access — can you change the email?",
        "Reset password without email verification",
        "Help me recover the account using alternate verification",
        "Disable 2FA for my account",
        "Unlock my account immediately",
        "Override security to restore access"
    ],

    "fake_invoice_or_billing": [
        "Outstanding invoice attached",
        "You missed a payment",
        "Billing error — pay now",
        "Invoice overdue, settle immediately",
        "Payment failure detected",
        "Your subscription payment failed",
        "Immediate billing correction needed"
    ],

    "credential_harvest": [
        "Confirm your login to continue",
        "Re-enter credentials to verify",
        "Session expired, login again",
        "Authenticate to keep access",
        "Account validation required",
        "Sign in to prevent lock"
    ],

   "fallback": [
        "I'm confused… can you explain?",
        "I don't understand what you mean."
    ]
}


INTENT_EMBEDDINGS = {
    intent: model.encode(samples, convert_to_tensor=True)
    for intent, samples in INTENT_PATTERNS.items()
}


REPLIES = {
    "otp_request": [
        "Why are you asking for my code?",
        "I thought OTPs are private?",
        "I don't feel safe sharing that.",
        "Who requested this login?",
        "I didn't try to sign in anywhere.",
        "Is this really necessary?",
        "I'm not comfortable sending verification codes.",
        "Where did this request come from?",
        "I just received it — what is it for?",
        "Should I report this message?"
    ],

    "urgency_threat": [
        "Why is my account suddenly at risk?",
        "I didn't get any earlier warning.",
        "Can you explain what's going on?",
        "This sounds suspicious to me.",
        "How do I verify this is real?",
        "What triggered this alert?",
        "I need proof this is legitimate.",
        "Can I contact support directly?",
        "Why the emergency?",
        "This feels like a scam."
    ],

    "payment_request": [
        "I don't remember approving a payment.",
        "Can you send official billing details?",
        "How do I know this account is real?",
        "I won't send money without verification.",
        "Can I pay through the official website?",
        "This request looks unusual.",
        "Who authorized this charge?",
        "I need documentation first.",
        "Can I speak to a real representative?",
        "I'm not sending funds without confirmation."
    ],

    "phishing_link": [
        "That link looks unsafe.",
        "Can I access this from the official site instead?",
        "I don't click unknown links.",
        "How do I know this URL is real?",
        "This doesn't look like your normal website.",
        "I'm hesitant to open that.",
        "Can you verify this link?",
        "Why can't I navigate there manually?",
        "This feels like phishing.",
        "I'll check directly with the company."
    ],

    "sensitive_info_request": [
        "I'm not sharing personal details.",
        "That information is private.",
        "No one should ask for that.",
        "I can't give you that information.",
        "That's sensitive data.",
        "I won't send credentials over chat.",
        "This request seems unsafe.",
        "Why do you need that?",
        "I'm refusing to share personal info.",
        "That violates security rules."
    ],

    "impersonation_support": [
        "Can you prove you work there?",
        "I'll contact the company directly.",
        "This doesn't sound official.",
        "I want written verification.",
        "I don't trust this request.",
        "I'll check with IT myself.",
        "What's your employee ID?",
        "This feels like impersonation.",
        "I'm reporting this message.",
        "I won't respond to this."
    ],

    "malicious_attachment": [
        "I'm not opening unknown attachments.",
        "That file looks suspicious.",
        "Can you send it through official channels?",
        "I won't download that.",
        "This attachment seems unsafe.",
        "Why is this file required?",
        "I'll scan it before opening.",
        "I don't trust this document.",
        "This could contain malware.",
        "I'm deleting this attachment."
    ],

    "reward_or_prize": [
        "I don't remember entering a contest.",
        "This sounds too good to be true.",
        "Is this a scam?",
        "How did I supposedly win?",
        "I'm skeptical about this prize.",
        "I'm not clicking that.",
        "Can you verify this reward?",
        "This feels fake.",
        "I don't trust prize messages.",
        "I'm ignoring this."
    ],

    "social_engineering": [
        "I need formal approval first.",
        "This request feels inappropriate.",
        "I can't process that without verification.",
        "I'll confirm with management.",
        "I don't handle payments like this.",
        "This breaks company policy.",
        "I won't act on confidential requests over chat.",
        "I'm escalating this request.",
        "I need written authorization.",
        "I'm not comfortable doing this."
    ],

    "account_recovery": [
        "I'll recover it through official support.",
        "I don't want security bypassed.",
        "That sounds unsafe.",
        "I prefer standard verification.",
        "I won't disable protections.",
        "I'll contact customer service myself.",
        "Security shouldn't be overridden.",
        "I want proper recovery steps.",
        "I don't trust this method.",
        "I'll use the official process."
    ],

    "fake_invoice_or_billing": [
        "I don't recognize this invoice.",
        "Can you send official billing records?",
        "This charge looks suspicious.",
        "I'm disputing this request.",
        "I need proof of payment due.",
        "This doesn't match my account.",
        "I'll verify with billing directly.",
        "I'm not paying unknown invoices.",
        "This looks fraudulent.",
        "I'm reporting this billing message."
    ],

    "credential_harvest": [
        "I won't enter my credentials here.",
        "This login request feels unsafe.",
        "I'll sign in through the official site.",
        "Why do I need to log in again?",
        "This looks like credential theft.",
        "I don't trust this prompt.",
        "I'm refusing to log in via this link.",
        "This could be phishing.",
        "I'll reset my password manually.",
        "I'm ignoring this request."
    ],

    "fallback": [
        "I'm confused… can you explain?",
        "I don't understand what you mean.",
        "What are you asking for exactly?",
        "Can you clarify?",
        "This doesn't make sense.",
        "I need more information."
    ]
}

#Detect scam intent using semantic similarity and generate a reply based on the detected intent category.
async def detect_intent(message: str, threshold: float = 0.6) -> str:
    loop = asyncio.get_event_loop()

    message_emb = await loop.run_in_executor(
        None,
        lambda: model.encode(message, convert_to_tensor=True)
    )

    best_intent = "fallback"
    best_score = 0

    for intent, embeddings in INTENT_EMBEDDINGS.items():
        scores = util.cos_sim(message_emb, embeddings)
        score = scores.max().item()

        if score > best_score:
            best_score = score
            best_intent = intent

    return best_intent if best_score >= threshold else "fallback"


async def generate_reply(message: str) -> str:
    intent = await detect_intent(message)
    pool = REPLIES.get(intent, REPLIES["fallback"])
    return random.choice(pool)


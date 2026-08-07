"""
Application constants.
"""

# ==========================================================
# Supported Documents
# ==========================================================

SUPPORTED_DOCUMENT_TYPES = [
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".txt",
]

SUPPORTED_IMAGE_TYPES = [
    ".png",
    ".jpg",
    ".jpeg",
]

SUPPORTED_PDF_TYPES = [
    ".pdf",
]

SUPPORTED_TEXT_TYPES = [
    ".txt",
]

# ==========================================================
# Upload Limits
# ==========================================================

MAX_UPLOAD_SIZE_MB = 25

# Maximum number of invoices that can be submitted together in a
# single batch upload (/process-invoices).
MAX_BATCH_INVOICES = 50

# ==========================================================
# AI
# ==========================================================

DEFAULT_CONFIDENCE_THRESHOLD = 80

DEFAULT_TEMPERATURE = 0.0

REQUEST_TIMEOUT = 30

MAX_PROVIDER_RETRIES = 2

# ==========================================================
# Logging
# ==========================================================

DEFAULT_LOG_LEVEL = "INFO"

# ==========================================================
# Risk Scoring
# ==========================================================

RISK_SCORE_VALIDATION_FAILED = 40

RISK_SCORE_POLICY_REVIEW = 20

RISK_SCORE_PER_ERROR = 10

RISK_SCORE_PER_WARNING = 5

RISK_SCORE_HIGH_VALUE_INVOICE = 15

HIGH_VALUE_INVOICE_THRESHOLD = 100000

RISK_SCORE_DUPLICATE_SUSPECTED = 25

RISK_SCORE_DUPLICATE_EXACT = 45

RISK_SCORE_NEW_VENDOR = 10

RISK_SCORE_MAX = 100

RISK_LEVEL_CRITICAL_THRESHOLD = 80

RISK_LEVEL_HIGH_THRESHOLD = 60

RISK_LEVEL_MEDIUM_THRESHOLD = 30
"""Environment variable loading, CORS origin, and court-domain allowlist."""

import os
from dotenv import load_dotenv

load_dotenv()

ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "http://localhost:3000")

# Court-domain allowlist for URL validation (input sanitization).
# Every *.courts.ca.gov subdomain plus known exceptions.
COURT_DOMAIN_ALLOWLIST = [
    ".courts.ca.gov",  # covers all 58 county subdomains + selfhelp.courts.ca.gov
    "lacourt.ca.gov",  # LA current
    "lacourt.org",     # LA legacy
]

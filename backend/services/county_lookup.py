"""Deterministic 58-domain lookup table. County <-> domain matching.

URL validation: only official court domains pass. This is the server-side
mirror of the client-side allowlist check (security checklist).
"""

import json
from pathlib import Path
from urllib.parse import urlparse

from backend.config import COURT_DOMAIN_ALLOWLIST

COUNTY_DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "county_domains.json"

_county_data: dict | None = None


def _load_county_data() -> dict:
    global _county_data
    if _county_data is None:
        with open(COUNTY_DATA_PATH, "r", encoding="utf-8") as f:
            _county_data = json.load(f)
    return _county_data


def get_county_config(county_code: str) -> dict | None:
    """Return the config dict for a county code, or None if not found."""
    data = _load_county_data()
    return data.get(county_code)


def resolve_county_from_url(url: str) -> str | None:
    """Given a court URL, return the county code or None.

    Raises ValueError if the URL is not on the court-domain allowlist.
    """
    # Parse and validate
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    domain = parsed.hostname
    if not domain:
        raise ValueError("Could not parse a valid domain from the URL provided.")

    # Allowlist check
    allowed = False
    for allowed_domain in COURT_DOMAIN_ALLOWLIST:
        if domain == allowed_domain.lstrip(".") or domain.endswith(allowed_domain):
            allowed = True
            break

    if not allowed:
        raise ValueError(
            f"'{domain}' is not an official California court domain. "
            "Please paste the URL from your jury summons (it should end in .courts.ca.gov or be lacourt.ca.gov)."
        )

    # Match against known counties
    data = _load_county_data()
    for code, county_info in data.items():
        for county_domain in county_info.get("domains", []):
            if domain == county_domain or domain.endswith("." + county_domain):
                return code

    # Valid court domain but not a county we have data for yet
    return None

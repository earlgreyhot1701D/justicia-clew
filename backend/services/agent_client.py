"""Calls the right DO Gradient AI agent endpoint. Key server-side only.

Plain httpx, not the OpenAI SDK. ?agent=true on the URL turns retrieval on.
Only SB is wired for real tonight; LA, SF, Fresno, Inyo are stubbed.
"""

import os
import httpx


async def ask_agent(county_prefix: str, question: str) -> dict:
    """Send a question to the county's DO agent and return the parsed response.

    Returns either an AskResponse-shaped dict or a RefusalResponse-shaped dict,
    determined by parsing the agent's reply for refusal signals.
    """
    endpoint = os.environ.get(f"AGENT_ENDPOINT_{county_prefix}")
    key = os.environ.get(f"AGENT_ACCESS_KEY_{county_prefix}")

    if not endpoint or not key:
        raise EnvironmentError(f"Missing AGENT_ENDPOINT_{county_prefix} or AGENT_ACCESS_KEY_{county_prefix} in environment.")

    url = f"{endpoint}/api/v1/chat/completions?agent=true"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    body = {
        "messages": [{"role": "user", "content": question}],
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, headers=headers, json=body)
        resp.raise_for_status()
        data = resp.json()

    # Parse the agent's response
    return _parse_agent_response(data, county_prefix)


def _parse_agent_response(data: dict, county_prefix: str) -> dict:
    """Extract structured answer or refusal from the raw agent response.

    The agent is instructed to include source quotes and to refuse clearly
    when it can't answer from the corpus. This parser interprets those signals.
    """
    # Extract the assistant message content
    choices = data.get("choices", [])
    if not choices:
        raise ValueError("Empty response from agent")

    content = choices[0].get("message", {}).get("content", "")
    if not content:
        raise ValueError("No content in agent response")

    # Detect refusal patterns — the agent is instructed to refuse and provide phone
    refusal_signals = [
        "i cannot answer",
        "i can't answer",
        "i can't advise",
        "i cannot advise",
        "i can't predict",
        "i cannot predict",
        "i don't have",
        "i do not have",
        "not in the information",
        "not in my knowledge",
        "cannot find",
        "not available in",
        "please contact",
        "call the jury",
        "i can't give",
        "i cannot give",
        "i can't tell you",
        "i cannot tell you",
    ]

    content_lower = content.lower()
    is_refusal = any(signal in content_lower for signal in refusal_signals)

    if is_refusal:
        # Map county to phone number and hours (real numbers for demo counties)
        phone = _get_jury_phone(county_prefix)
        hours = _get_jury_hours(county_prefix)
        return {
            "refusal": True,
            "message": content,
            "phone": phone,
            "hours": hours,
        }

    # Non-refusal: structured answer
    # The agent is instructed to include source attribution, parse it out
    return {
        "answer": content,
        "quote": _extract_quote(content),
        "source_label": _detect_source_label(content),
        "source_url": _get_source_url(county_prefix),
        "last_checked": "July 2026",
    }


def _get_jury_phone(county_prefix: str) -> str:
    """Return the real jury services phone number for a county."""
    phones = {
        "SB": "(805) 882-4530",
        "LA": "NOT_VERIFIED_STUB",
        "SF": "NOT_VERIFIED_STUB",
        "FRESNO": "NOT_VERIFIED_STUB",
        "INYO": "NOT_VERIFIED_STUB",
    }
    return phones.get(county_prefix, "Check your summons for the jury office phone number.")


def _get_jury_hours(county_prefix: str) -> str:
    """Return office hours to pair with the jury phone number, so a refusal
    never sends someone to call a line that won't answer right now."""
    hours = {
        "SB": "Mon-Fri, 8am-3pm, excluding holidays. Automated info line answers anytime: 877-544-5094.",
    }
    return hours.get(county_prefix, "Check your summons for office hours.")


def _extract_quote(content: str) -> str:
    """Extract a quoted passage from the agent's response if present."""
    # Look for text in quotation marks as the source quote
    import re
    quotes = re.findall(r'"([^"]{10,})"', content)
    if quotes:
        return quotes[0]
    # Fallback: look for text after common attribution phrases
    for marker in ["according to", "from the website:", "the site states:"]:
        if marker in content.lower():
            idx = content.lower().index(marker)
            snippet = content[idx + len(marker):].strip()
            # Take up to the first period or 200 chars
            end = snippet.find(".")
            if end > 0:
                return snippet[:end + 1]
            return snippet[:200]
    return ""


def _detect_source_label(content: str) -> str:
    """Determine if the answer came from county site or statewide JC site."""
    statewide_signals = ["judicial council", "self-help center", "selfhelp.courts.ca.gov", "california courts"]
    content_lower = content.lower()
    if any(s in content_lower for s in statewide_signals):
        return "statewide"
    return "county"


def _get_source_url(county_prefix: str) -> str:
    """Return the primary source URL for a county's jury information."""
    urls = {
        "SB": "https://www.santabarbara.courts.ca.gov",
        "LA": "https://www.lacourt.ca.gov/pages/lp/juror-services",
        "SF": "https://sf.courts.ca.gov/divisions/jury-services",
        "FRESNO": "https://www.fresno.courts.ca.gov/divisions/jury-service",
        "INYO": "https://www.inyo.courts.ca.gov/general-information/jury-service",
    }
    return urls.get(county_prefix, "https://www.courts.ca.gov")

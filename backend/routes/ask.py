"""POST /api/ask — chip taps and free-text questions, same path."""

from fastapi import APIRouter, HTTPException, Request
from backend.models.schemas import AskRequest, AskResponse, RefusalResponse
from backend.services.agent_client import ask_agent
from backend.services.county_lookup import get_county_config
from backend.services.rate_limit import check_rate_limit

router = APIRouter()


@router.post("/ask")
async def ask_question(req: AskRequest, request: Request):
    client_id = request.client.host if request.client else "unknown"
    if not check_rate_limit(client_id):
        raise HTTPException(
            status_code=429,
            detail={"error": "rate_limited", "message": "Too many questions too quickly. Please wait a minute and try again."},
        )

    county_cfg = get_county_config(req.county)
    if county_cfg is None:
        raise HTTPException(
            status_code=400,
            detail={"error": "unknown_county", "message": f"County '{req.county}' is not available yet. Try Santa Barbara or start with statewide info."},
        )

    try:
        result = await ask_agent(county_cfg["agent_env_prefix"], req.question)
    except Exception as e:
        print(f"agent_client error: {e}")
        raise HTTPException(
            status_code=502,
            detail={"error": "agent_unavailable", "message": "Could not reach the court information service right now. Please try again in a moment."},
        )

    return result

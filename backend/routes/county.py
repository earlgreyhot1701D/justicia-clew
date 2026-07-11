"""POST /api/resolve-county — URL paste -> county lookup with allowlist validation."""

from fastapi import APIRouter, HTTPException
from backend.models.schemas import ResolveCountyRequest, ResolveCountyResponse
from backend.services.county_lookup import resolve_county_from_url

router = APIRouter()


@router.post("/resolve-county", response_model=ResolveCountyResponse)
async def resolve_county(req: ResolveCountyRequest):
    try:
        county = resolve_county_from_url(req.url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": "invalid_url", "message": str(e)})
    if county is None:
        raise HTTPException(
            status_code=400,
            detail={"error": "unknown_domain", "message": "Could not match that URL to a California court. Try pasting the full URL from your jury summons."},
        )
    return ResolveCountyResponse(county=county)

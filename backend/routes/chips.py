"""GET /api/chips?county= — returns tagged FAQ chips for a county."""

import json
from pathlib import Path
from fastapi import APIRouter, Query, HTTPException

router = APIRouter()

CHIPS_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "faq_chips.json"


@router.get("/chips")
async def get_chips(county: str = Query(..., min_length=1)):
    try:
        with open(CHIPS_PATH, "r", encoding="utf-8") as f:
            all_chips = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail={"error": "config_missing", "message": "FAQ chips data not found. Please contact support."})
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail={"error": "config_invalid", "message": "FAQ chips data is malformed. Please contact support."})

    # Return chips tagged for this county or statewide
    filtered = [c for c in all_chips if c.get("tag") == "statewide" or c.get("county") == county]
    return filtered

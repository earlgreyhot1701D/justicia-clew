"""Pydantic request/response shapes — includes refusal shape."""

from pydantic import BaseModel, Field
from typing import Optional


class ResolveCountyRequest(BaseModel):
    url: str = Field(..., min_length=1, max_length=2048)


class ResolveCountyResponse(BaseModel):
    county: str


class AskRequest(BaseModel):
    county: str = Field(..., min_length=1, max_length=50)
    question: str = Field(..., min_length=1, max_length=1000)


class AskResponse(BaseModel):
    answer: str
    quote: str
    source_label: str  # "county" or "statewide"
    source_url: str
    last_checked: str


class RefusalResponse(BaseModel):
    refusal: bool = True
    message: str
    phone: str

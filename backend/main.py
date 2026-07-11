"""FastAPI app instance — mounts routers, CORS lock, /health endpoint, static frontend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.config import ALLOWED_ORIGIN
from backend.routes import county, chips, ask

app = FastAPI(title="Justicia Clew", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(county.router, prefix="/api")
app.include_router(chips.router, prefix="/api")
app.include_router(ask.router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}


# Static frontend — html=True serves index.html at /
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

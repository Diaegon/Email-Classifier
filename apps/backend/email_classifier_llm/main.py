from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .routers.classify import router as classify_router

app = FastAPI(title="Email Classifier LLM API")

# Dev CORS (ajuste em produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

app.include_router(classify_router, prefix="/api")

# Servir frontend estático (apps/frontend)
_frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
if _frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(_frontend_dir), html=True), name="frontend")

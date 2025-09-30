from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from .routers.classify import router as classify_router
from .routers.clients import router as clients_router
from .database import init_database

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
    return {"status": "ok", "message": "Email Classifier API is running"}

app.include_router(classify_router, prefix="/api")
app.include_router(clients_router, prefix="/api")

# Inicializar banco de dados
init_database()

# Servir frontend estático (apps/frontend)
_frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
print(f"Frontend directory: {_frontend_dir}")
print(f"Frontend exists: {_frontend_dir.exists()}")
if _frontend_dir.exists():
    print(f"Mounting frontend from: {_frontend_dir}")
    app.mount("/", StaticFiles(directory=str(_frontend_dir), html=True), name="frontend")
else:
    # Fallback se frontend não existir
    print("Frontend not found, using fallback")
    @app.get("/")
    def root() -> dict:
        return {"message": "Email Classifier API", "docs": "/docs", "health": "/health"}

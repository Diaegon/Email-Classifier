from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
from core.path import FRONTEND_DIR


from .routers.classify import router as classify_router
from .routers.clients import router as clients_router


app = FastAPI(title="Email Classifier LLM API")



#@app.get("/health")
def health() -> dict:
    """Health check endpoint para Railway"""
    try:
        # Verificar se o banco está acessível
        from .database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "message": "Email Classifier API is running",
            "database": "connected",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Database connection failed: {str(e)}",
            "database": "disconnected",
            "timestamp": "2024-01-01T00:00:00Z"
        }

app.include_router(classify_router, prefix="/api")
#app.include_router(clients_router, prefix="/api")

app.mount(
    "/",
    StaticFiles(directory=str(FRONTEND_DIR), html=True),
    name="frontend"
    )

        

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
import sys

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

@app.get("/debug")
def debug() -> dict:
    """Debug endpoint para verificar configuração"""
    _frontend_paths = [
        Path(__file__).resolve().parents[2] / "frontend",  # Local
        Path("/app/apps/frontend"),  # Railway
        Path("./apps/frontend"),  # Railway alternativo
        Path("../frontend"),  # Fallback
    ]
    
    result = {
        "current_file": __file__,
        "working_dir": os.getcwd(),
        "paths_tested": []
    }
    
    for path in _frontend_paths:
        exists = path.exists()
        result["paths_tested"].append({
            "path": str(path),
            "exists": exists,
            "files": list(path.iterdir()) if exists else []
        })
    
    return result

@app.get("/health")
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
app.include_router(clients_router, prefix="/api")

# Inicializar banco de dados com tratamento de erro
def setup_database():
    """Configura o banco de dados com tratamento de erro"""
    try:
        print("🔄 Inicializando banco de dados...")
        init_database()
        print("✅ Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar banco de dados: {e}")
        print("⚠️  Aplicação continuará sem banco de dados")
        # Em produção, você pode querer falhar aqui
        # sys.exit(1)

# Executar setup do banco
setup_database()

# Servir frontend estático (apps/frontend)
# Tentar diferentes caminhos para compatibilidade com Railway
_frontend_paths = [
    Path(__file__).resolve().parents[2] / "frontend",  # Local
    Path("/app/apps/frontend"),  # Railway
    Path("./apps/frontend"),  # Railway alternativo
    Path("../frontend"),  # Fallback
]

_frontend_dir = None
for path in _frontend_paths:
    print(f"Tentando frontend em: {path}")
    if path.exists():
        _frontend_dir = path
        print(f"✅ Frontend encontrado em: {path}")
        break

if _frontend_dir:
    print(f"Mounting frontend from: {_frontend_dir}")
    # Listar arquivos do frontend para debug
    try:
        frontend_files = list(_frontend_dir.iterdir())
        print(f"Frontend files: {[f.name for f in frontend_files]}")
    except Exception as e:
        print(f"Erro ao listar arquivos do frontend: {e}")
    
    app.mount("/", StaticFiles(directory=str(_frontend_dir), html=True), name="frontend")
    print("✅ Frontend montado com sucesso!")
else:
    # Fallback se frontend não existir
    print("❌ Frontend not found in any path, using fallback")
    @app.get("/")
    def root() -> dict:
        return {
            "message": "Email Classifier API", 
            "docs": "/docs", 
            "health": "/health",
            "debug": "/debug",
            "error": "Frontend not found",
            "tried_paths": [str(p) for p in _frontend_paths]
        }

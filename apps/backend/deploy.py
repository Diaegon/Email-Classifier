#!/usr/bin/env python3
"""
Script de deploy para Railway
Executa migrações e inicia a aplicação
"""

import os
import sys
import subprocess
from pathlib import Path

# Adicionar o diretório do backend ao path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def run_migrations():
    """Executa migrações do banco de dados"""
    print("🔄 Executando migrações do banco de dados...")
    
    try:
        # Importar e executar migrações
        from email_classifier_llm.database import init_database, engine
        from sqlalchemy import text
        
        # Verificar conexão
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexão com banco de dados estabelecida")
        
        # Executar migrações
        init_database()
        print("✅ Migrações executadas com sucesso!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao executar migrações: {e}")
        return False

def start_app():
    """Inicia a aplicação FastAPI"""
    print("🚀 Iniciando aplicação...")
    
    # Configurar porta
    port = int(os.getenv("PORT", 8000))
    print(f"📡 Porta configurada: {port}")
    
    try:
        import uvicorn
        print("✅ Uvicorn importado com sucesso")
        
        # Configurar uvicorn
        config = uvicorn.Config(
            "email_classifier_llm.main:app",
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
        
        print("✅ Configuração do Uvicorn criada")
        server = uvicorn.Server(config)
        print("✅ Servidor Uvicorn criado")
        
        print(f"🌐 Iniciando servidor na porta {port}...")
        server.run()
        
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
        print(f"❌ Tipo do erro: {type(e).__name__}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        sys.exit(1)

def main():
    """Função principal do deploy"""
    print("🚀 Iniciando deploy do Email Classifier...")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    db_url = os.getenv("DB_DATABASE_URL")
    if not db_url:
        print("⚠️  DB_DATABASE_URL não encontrada")
        print("   Usando SQLite como fallback")
    else:
        print(f"📊 Banco de dados: {db_url.split('://')[0]}")
    
    # Executar migrações
    if not run_migrations():
        print("⚠️  Migrações falharam, continuando sem banco de dados")
    
    # Iniciar aplicação
    start_app()

if __name__ == "__main__":
    main()

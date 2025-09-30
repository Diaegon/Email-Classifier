#!/usr/bin/env python3
"""
Script de deploy para Railway
Executa migrações e inicia a aplicação
"""

import os
import sys
import subprocess
from pathlib import Path

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
    
    try:
        import uvicorn
        uvicorn.run(
            "email_classifier_llm.main:app",
            host="0.0.0.0",
            port=int(os.getenv("PORT", 8000)),
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
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

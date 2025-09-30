#!/usr/bin/env python3
"""
Script para executar migrações automaticamente no deploy
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório do projeto ao path
sys.path.append(str(Path(__file__).parent))

def run_migrations():
    """Executa migrações do banco de dados"""
    print("🔄 Executando migrações do banco de dados...")
    
    try:
        from email_classifier_llm.database import init_database, engine
        from sqlalchemy import text
        
        # Verificar se o banco está acessível
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

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)

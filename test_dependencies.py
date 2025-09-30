#!/usr/bin/env python3
"""
Script para testar dependências do banco de dados
"""

import sys

def test_dependencies():
    """Testa se todas as dependências estão disponíveis"""
    print("🧪 Testando dependências do banco de dados...")
    
    # Testar SQLAlchemy
    try:
        import sqlalchemy
        print(f"✅ SQLAlchemy: {sqlalchemy.__version__}")
    except ImportError as e:
        print(f"❌ SQLAlchemy não encontrado: {e}")
        return False
    
    # Testar PostgreSQL
    try:
        import psycopg2
        print(f"✅ psycopg2: {psycopg2.__version__}")
    except ImportError:
        print("⚠️  psycopg2 não encontrado (PostgreSQL não disponível)")
    
    # Testar MySQL
    try:
        import pymysql
        print(f"✅ pymysql: {pymysql.__version__}")
    except ImportError:
        print("⚠️  pymysql não encontrado (MySQL não disponível)")
    
    # Testar FastAPI
    try:
        import fastapi
        print(f"✅ FastAPI: {fastapi.__version__}")
    except ImportError as e:
        print(f"❌ FastAPI não encontrado: {e}")
        return False
    
    # Testar Uvicorn
    try:
        import uvicorn
        print(f"✅ Uvicorn: {uvicorn.__version__}")
    except ImportError as e:
        print(f"❌ Uvicorn não encontrado: {e}")
        return False
    
    return True

def test_database_connection():
    """Testa conexão com banco de dados"""
    print("\n🔍 Testando conexão com banco de dados...")
    
    try:
        from apps.backend.email_classifier_llm.database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexão com banco de dados funcionando!")
            return True
            
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Teste de Dependências")
    print("=" * 40)
    
    # Testar dependências
    if not test_dependencies():
        print("❌ Algumas dependências estão faltando")
        sys.exit(1)
    
    # Testar conexão com banco
    if not test_database_connection():
        print("❌ Problema na conexão com banco de dados")
        sys.exit(1)
    
    print("\n✅ Todos os testes passaram!")

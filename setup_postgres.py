#!/usr/bin/env python3
"""
Script para configurar PostgreSQL automaticamente
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_docker():
    """Verifica se Docker está instalado"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker encontrado:", result.stdout.strip())
            return True
        else:
            print("❌ Docker não encontrado")
            return False
    except FileNotFoundError:
        print("❌ Docker não instalado")
        return False

def start_postgres_docker():
    """Inicia PostgreSQL via Docker"""
    print("🐳 Iniciando PostgreSQL via Docker...")
    
    # Verificar se docker-compose existe
    if not Path("docker-compose.yml").exists():
        print("❌ docker-compose.yml não encontrado")
        return False
    
    try:
        # Iniciar containers
        result = subprocess.run(['docker-compose', 'up', '-d'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ PostgreSQL iniciado com sucesso!")
            print("📊 Dados de conexão:")
            print("   Host: localhost")
            print("   Port: 5432")
            print("   Database: email_classifier")
            print("   User: postgres")
            print("   Password: password123")
            print("   URL: postgresql://postgres:password123@localhost:5432/email_classifier")
            print("\n🌐 PgAdmin (opcional): http://localhost:8080")
            print("   Email: admin@admin.com")
            print("   Password: admin123")
            return True
        else:
            print("❌ Erro ao iniciar PostgreSQL:", result.stderr)
            return False
    except FileNotFoundError:
        print("❌ docker-compose não encontrado")
        print("💡 Instale Docker Desktop: https://www.docker.com/products/docker-desktop/")
        return False

def create_env_file():
    """Cria arquivo .env com configurações do PostgreSQL"""
    env_content = """# Configuração do Banco de Dados
DB_DATABASE_URL=postgresql://postgres:password123@localhost:5432/email_classifier

# Configuração do LLM (escolha uma)
LLM_PROVIDER=google
GOOGLE_API_KEY=sua_chave_aqui
GOOGLE_MODEL=gemini-2.0-flash
"""
    
    env_path = Path("apps/backend/.env")
    env_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Arquivo .env criado em: {env_path}")

def test_connection():
    """Testa conexão com PostgreSQL"""
    print("🔍 Testando conexão com PostgreSQL...")
    
    try:
        # Aguardar PostgreSQL inicializar
        time.sleep(5)
        
        # Testar conexão
        result = subprocess.run([
            'docker', 'exec', 'email-classifier-postgres',
            'psql', '-U', 'postgres', '-d', 'email_classifier', '-c', 'SELECT version();'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Conexão com PostgreSQL funcionando!")
            return True
        else:
            print("❌ Erro na conexão:", result.stderr)
            return False
    except Exception as e:
        print(f"❌ Erro ao testar conexão: {e}")
        return False

def show_instructions():
    """Mostra instruções de uso"""
    print("\n" + "="*60)
    print("🚀 POSTGRESQL CONFIGURADO COM SUCESSO!")
    print("="*60)
    print("\n📋 Próximos passos:")
    print("1. Configure sua API LLM no arquivo .env")
    print("2. Execute as migrações:")
    print("   cd apps/backend")
    print("   python migrate.py init")
    print("   python migrate.py upgrade")
    print("3. Inicie o servidor:")
    print("   python -c \"import uvicorn; uvicorn.run('email_classifier_llm.main:app', host='0.0.0.0', port=8000)\"")
    print("\n🔧 Comandos úteis:")
    print("   docker-compose up -d    # Iniciar PostgreSQL")
    print("   docker-compose down     # Parar PostgreSQL")
    print("   docker-compose logs     # Ver logs")
    print("\n🌐 Acesse:")
    print("   Aplicação: http://localhost:8000")
    print("   PgAdmin: http://localhost:8080")

def main():
    print("🐘 Configurador de PostgreSQL para Email Classifier")
    print("="*50)
    
    # Verificar Docker
    if not check_docker():
        print("\n💡 Instale Docker Desktop primeiro:")
        print("   https://www.docker.com/products/docker-desktop/")
        return False
    
    # Iniciar PostgreSQL
    if not start_postgres_docker():
        return False
    
    # Aguardar inicialização
    print("⏳ Aguardando PostgreSQL inicializar...")
    time.sleep(10)
    
    # Testar conexão
    if not test_connection():
        print("⚠️  PostgreSQL pode estar ainda inicializando...")
        print("   Tente novamente em alguns minutos")
    
    # Criar arquivo .env
    create_env_file()
    
    # Mostrar instruções
    show_instructions()
    
    return True

if __name__ == "__main__":
    main()

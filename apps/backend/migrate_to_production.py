#!/usr/bin/env python3
"""
Script para migrar dados do SQLite para PostgreSQL em produção
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório do projeto ao path
sys.path.append(str(Path(__file__).parent))

from email_classifier_llm.database import get_engine_config, SessionLocal
from email_classifier_llm.models.client import Client
from sqlalchemy import create_engine, text

def migrate_sqlite_to_postgres():
    """
    Migra dados do SQLite para PostgreSQL
    """
    print("🔄 Iniciando migração de SQLite para PostgreSQL...")
    
    # URLs dos bancos
    sqlite_url = "sqlite:///./email_classifier.db"
    postgres_url = os.getenv("DB_DATABASE_URL")
    
    if not postgres_url:
        print("❌ Erro: DB_DATABASE_URL não encontrada")
        print("Configure a variável de ambiente com a URL do PostgreSQL")
        return False
    
    try:
        # Conectar ao SQLite
        print("📖 Conectando ao SQLite...")
        sqlite_engine = create_engine(sqlite_url, **get_engine_config())
        sqlite_session = SessionLocal(bind=sqlite_engine)
        
        # Conectar ao PostgreSQL
        print("📖 Conectando ao PostgreSQL...")
        postgres_engine = create_engine(postgres_url, **get_engine_config())
        postgres_session = SessionLocal(bind=postgres_engine)
        
        # Verificar se o PostgreSQL tem dados
        existing_clients = postgres_session.query(Client).count()
        if existing_clients > 0:
            print(f"⚠️  PostgreSQL já possui {existing_clients} clientes")
            response = input("Deseja continuar e adicionar os dados do SQLite? (s/N): ")
            if response.lower() != 's':
                print("❌ Migração cancelada")
                return False
        
        # Ler dados do SQLite
        print("📊 Lendo dados do SQLite...")
        clients = sqlite_session.query(Client).all()
        print(f"📊 Encontrados {len(clients)} clientes no SQLite")
        
        if not clients:
            print("ℹ️  Nenhum cliente encontrado no SQLite")
            return True
        
        # Migrar dados
        print("🔄 Migrando dados...")
        migrated_count = 0
        
        for client in clients:
            try:
                # Verificar se já existe no PostgreSQL
                existing = postgres_session.query(Client).filter(
                    Client.cpf == client.cpf
                ).first()
                
                if not existing:
                    # Criar novo cliente no PostgreSQL
                    new_client = Client(
                        nome_completo=client.nome_completo,
                        cpf=client.cpf,
                        data_nascimento=client.data_nascimento,
                        numero_cliente=client.numero_cliente,
                        email=client.email,
                        perfil_investidor=client.perfil_investidor,
                        ativos_custodiados=client.ativos_custodiados,
                        plano_contratual_em_dia=client.plano_contratual_em_dia
                    )
                    postgres_session.add(new_client)
                    migrated_count += 1
                else:
                    print(f"⚠️  Cliente {client.cpf} já existe no PostgreSQL")
                    
            except Exception as e:
                print(f"❌ Erro ao migrar cliente {client.cpf}: {e}")
                continue
        
        # Commit das mudanças
        postgres_session.commit()
        print(f"✅ Migração concluída! {migrated_count} clientes migrados")
        
        # Fechar conexões
        sqlite_session.close()
        postgres_session.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante a migração: {e}")
        return False

def verify_migration():
    """
    Verifica se a migração foi bem-sucedida
    """
    print("\n🔍 Verificando migração...")
    
    postgres_url = os.getenv("DB_DATABASE_URL")
    if not postgres_url:
        print("❌ DB_DATABASE_URL não encontrada")
        return False
    
    try:
        postgres_engine = create_engine(postgres_url, **get_engine_config())
        postgres_session = SessionLocal(bind=postgres_engine)
        
        # Contar clientes
        client_count = postgres_session.query(Client).count()
        print(f"📊 Total de clientes no PostgreSQL: {client_count}")
        
        # Mostrar alguns exemplos
        if client_count > 0:
            print("\n📋 Exemplos de clientes migrados:")
            clients = postgres_session.query(Client).limit(3).all()
            for client in clients:
                print(f"  - {client.nome_completo} ({client.cpf})")
        
        postgres_session.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar migração: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Script de Migração SQLite → PostgreSQL")
    print("=" * 50)
    
    # Verificar se estamos em produção
    if not os.getenv("DB_DATABASE_URL"):
        print("❌ Este script deve ser executado em produção com DB_DATABASE_URL configurada")
        sys.exit(1)
    
    # Executar migração
    if migrate_sqlite_to_postgres():
        verify_migration()
        print("\n✅ Migração concluída com sucesso!")
    else:
        print("\n❌ Migração falhou!")
        sys.exit(1)

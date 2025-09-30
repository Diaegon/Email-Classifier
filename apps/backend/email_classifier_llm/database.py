from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os
from contextlib import contextmanager
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Configurações do banco de dados"""
    database_url: str = "sqlite:///./email_classifier.db"
    
    class Config:
        env_file = ".env"
        env_prefix = "DB_"
        extra = "ignore"  # Ignora variáveis extras não definidas


# Instanciar configurações
db_settings = DatabaseSettings()

# URL do banco de dados (com fallback para SQLite)
DATABASE_URL = db_settings.database_url

# Configurar engine baseado no tipo de banco
def get_engine_config():
    """Retorna configuração do engine baseada no tipo de banco"""
    if DATABASE_URL.startswith("sqlite"):
        return {
            "connect_args": {"check_same_thread": False},
            "echo": False  # Set to True for SQL query logging
        }
    elif DATABASE_URL.startswith("postgresql"):
        return {
            "echo": False,
            "pool_pre_ping": True,  # Verifica conexões antes de usar
            "pool_recycle": 300,    # Recicla conexões a cada 5 minutos
        }
    elif DATABASE_URL.startswith("mysql"):
        return {
            "echo": False,
            "pool_pre_ping": True,
            "pool_recycle": 300,
        }
    else:
        return {"echo": False}


# Criar engine do SQLAlchemy
engine = create_engine(DATABASE_URL, **get_engine_config())

# Criar SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency para obter sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Cria todas as tabelas no banco de dados"""
    from .models.client import Base
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db_session():
    """
    Context manager para gerenciar sessões do banco de dados.
    
    Uso recomendado:
    with get_db_session() as db:
        # operações com o banco
        db.query(Client).all()
        # sessão é fechada automaticamente
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database():
    """Inicializa o banco de dados com dados de exemplo"""
    create_tables()
    
    # Adicionar dados de exemplo se o banco estiver vazio
    with get_db_session() as db:
        from .models.client import Client
        from datetime import date
        
        # Verificar se já existem clientes
        if db.query(Client).count() == 0:
            # Dados de exemplo
            sample_clients = [
                Client(
                    nome_completo="João Silva Santos",
                    cpf="123.456.789-00",
                    data_nascimento=date(1985, 3, 15),
                    numero_cliente="CLI001",
                    email="joao.silva@email.com",
                    perfil_investidor="Conservador",
                    ativos_custodiados="Tesouro Selic, CDB, LCI",
                    plano_contratual_em_dia=True
                ),
                Client(
                    nome_completo="Maria Oliveira Costa",
                    cpf="987.654.321-00",
                    data_nascimento=date(1990, 7, 22),
                    numero_cliente="CLI002",
                    email="maria.oliveira@email.com",
                    perfil_investidor="Moderado",
                    ativos_custodiados="Ações, FIIs, Tesouro IPCA+",
                    plano_contratual_em_dia=True
                ),
                Client(
                    nome_completo="Pedro Ferreira Lima",
                    cpf="456.789.123-00",
                    data_nascimento=date(1978, 11, 8),
                    numero_cliente="CLI003",
                    email="pedro.ferreira@email.com",
                    perfil_investidor="Agressivo",
                    ativos_custodiados="Ações, Opções, Criptomoedas",
                    plano_contratual_em_dia=False
                ),
                Client(
                    nome_completo="Ana Paula Rodrigues",
                    cpf="789.123.456-00",
                    data_nascimento=date(1992, 5, 30),
                    numero_cliente="CLI004",
                    email="ana.rodrigues@email.com",
                    perfil_investidor="Moderado",
                    ativos_custodiados="FIIs, CDB, Tesouro Selic",
                    plano_contratual_em_dia=True
                ),
                Client(
                    nome_completo="Carlos Eduardo Souza",
                    cpf="321.654.987-00",
                    data_nascimento=date(1983, 9, 12),
                    numero_cliente="CLI005",
                    email="carlos.souza@email.com",
                    perfil_investidor="Conservador",
                    ativos_custodiados="Poupança, CDB, LCI",
                    plano_contratual_em_dia=True
                )
            ]
            
            for client in sample_clients:
                db.add(client)
            
            db.commit()
            print("Dados de exemplo adicionados ao banco de dados")

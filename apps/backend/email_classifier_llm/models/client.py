from sqlalchemy import Column, Integer, String, Date, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
from typing import Optional

Base = declarative_base()


class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    nome_completo = Column(String(255), nullable=False, index=True)
    cpf = Column(String(14), unique=True, nullable=False, index=True)
    data_nascimento = Column(Date, nullable=False)
    numero_cliente = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    perfil_investidor = Column(String(50), nullable=False)
    ativos_custodiados = Column(Text, nullable=True)
    plano_contratual_em_dia = Column(Boolean, default=True, nullable=False)
    
    def to_dict(self) -> dict:
        """Converte o modelo para dicionário para serialização JSON"""
        return {
            "id": self.id,
            "nome_completo": self.nome_completo,
            "cpf": self.cpf,
            "data_nascimento": self.data_nascimento.isoformat() if self.data_nascimento else None,
            "numero_cliente": self.numero_cliente,
            "email": self.email,
            "perfil_investidor": self.perfil_investidor,
            "ativos_custodiados": self.ativos_custodiados,
            "plano_contratual_em_dia": self.plano_contratual_em_dia
        }

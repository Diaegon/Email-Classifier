from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from ..models.client import Client


class ClientService:
    def __init__(self, db: Session):
        self.db = db
    
    def search_clients(self, query: str) -> List[Client]:
        """
        Busca clientes por nome, CPF, número do cliente ou email
        """
        if not query or len(query.strip()) < 2:
            return []
        
        search_term = f"%{query.strip()}%"
        
        clients = self.db.query(Client).filter(
            or_(
                Client.nome_completo.ilike(search_term),
                Client.cpf.ilike(search_term),
                Client.numero_cliente.ilike(search_term),
                Client.email.ilike(search_term)
            )
        ).limit(10).all()
        
        return clients
    
    def get_client_by_id(self, client_id: int) -> Optional[Client]:
        """
        Busca um cliente específico por ID
        """
        return self.db.query(Client).filter(Client.id == client_id).first()
    
    def get_client_by_cpf(self, cpf: str) -> Optional[Client]:
        """
        Busca um cliente específico por CPF
        """
        return self.db.query(Client).filter(Client.cpf == cpf).first()
    
    def get_client_by_number(self, numero_cliente: str) -> Optional[Client]:
        """
        Busca um cliente específico por número do cliente
        """
        return self.db.query(Client).filter(Client.numero_cliente == numero_cliente).first()
    
    def get_all_clients(self, limit: int = 50) -> List[Client]:
        """
        Retorna todos os clientes com limite
        """
        return self.db.query(Client).limit(limit).all()

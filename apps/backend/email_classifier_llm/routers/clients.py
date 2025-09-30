from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from ..services.client_service import ClientService
from ..models.client import Client

router = APIRouter(tags=["clients"])


@router.get("/clients/search")
async def search_clients(
    q: str = Query(..., min_length=2, description="Termo de busca (nome, CPF, número do cliente ou email)"),
    db: Session = Depends(get_db)
):
    """
    Busca clientes por termo de pesquisa
    """
    try:
        client_service = ClientService(db)
        clients = client_service.search_clients(q)
        
        return {
            "success": True,
            "count": len(clients),
            "clients": [client.to_dict() for client in clients]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca de clientes: {str(e)}")


@router.get("/clients/{client_id}")
async def get_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    """
    Busca um cliente específico por ID
    """
    try:
        client_service = ClientService(db)
        client = client_service.get_client_by_id(client_id)
        
        if not client:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        return {
            "success": True,
            "client": client.to_dict()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar cliente: {str(e)}")


@router.get("/clients")
async def list_clients(
    limit: int = Query(50, ge=1, le=100, description="Número máximo de clientes a retornar"),
    db: Session = Depends(get_db)
):
    """
    Lista todos os clientes com limite
    """
    try:
        client_service = ClientService(db)
        clients = client_service.get_all_clients(limit)
        
        return {
            "success": True,
            "count": len(clients),
            "clients": [client.to_dict() for client in clients]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar clientes: {str(e)}")

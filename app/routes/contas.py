# Path: app/routes/contas.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.mysql import get_db
from app.schemas.contas import (
    ContaCreate,
    ContaUpdate,
    ContaResponse,
    ContasListResponse,
    ContaDeleteResponse,
)
from app.services.contas import ContasService

router = APIRouter()


# Criar um serviço de contas
def get_contas_service(db: Session = Depends(get_db)):
    return ContasService(db)


@router.get("/", response_model=list[ContasListResponse])
async def get_contas(service: ContasService = Depends(get_contas_service)):
    contas = service.get_all_contas()
    return contas


@router.get("/{conta_id}", response_model=ContaResponse)
async def get_conta(
    conta_id: str, service: ContasService = Depends(get_contas_service)
):
    db_conta = service.get_conta_by_id(conta_id)
    if not db_conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return db_conta


@router.post("/", response_model=ContaResponse)
async def create_conta(
    conta: ContaCreate, service: ContasService = Depends(get_contas_service)
):
    db_conta = service.create_conta(conta)
    return db_conta


@router.put("/{conta_id}", response_model=ContaResponse)
async def update_conta(
    conta_id: str,
    conta: ContaUpdate,
    service: ContasService = Depends(get_contas_service),
):
    db_conta = service.update_conta(conta_id, conta)
    if not db_conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return db_conta


@router.delete("/{conta_id}", response_model=ContaDeleteResponse)
async def delete_conta(
    conta_id: str, service: ContasService = Depends(get_contas_service)
):
    db_conta = service.delete_conta(conta_id)
    if not db_conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return {"id": conta_id, "mensagem": "Conta deletada com sucesso"}

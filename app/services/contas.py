# Path: app/services/contas.py

from sqlalchemy.orm import Session
from app.models.contas import Contas
from app.schemas.contas import ContaCreate, ContaUpdate
from uuid import uuid4
from datetime import datetime


class ContasService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_contas(self):
        return self.db.query(Contas).all()

    def get_conta_by_id(self, conta_id: str):
        return self.db.query(Contas).filter(Contas.id == conta_id).first()

    def create_conta(self, conta: ContaCreate):
        db_conta = Contas(
            id=str(uuid4()),
            tipo=conta.tipo,
            descricao=conta.descricao,
            valor=conta.valor,
            data_vencimento=conta.data_vencimento,
            data_emissao=datetime.utcnow(),
        )
        self.db.add(db_conta)
        self.db.commit()
        self.db.refresh(db_conta)
        return db_conta

    def update_conta(self, conta_id: str, conta: ContaUpdate):
        db_conta = self.db.query(Contas).filter(Contas.id == conta_id).first()
        if not db_conta:
            return None  # Conta não encontrada

        for key, value in conta.dict(exclude_unset=True).items():
            setattr(db_conta, key, value)

        self.db.commit()
        self.db.refresh(db_conta)
        return db_conta

    def delete_conta(self, conta_id: str):
        db_conta = self.db.query(Contas).filter(Contas.id == conta_id).first()
        if not db_conta:
            return None  # Conta não encontrada

        self.db.delete(db_conta)
        self.db.commit()
        return db_conta

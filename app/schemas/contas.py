# Path: app/schemas/contas.py

from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
import uuid


# Schema para a criação de uma nova conta
class ContaCreate(BaseModel):
    tipo: str = Field(
        ..., example="A Receber", description="Tipo da conta: 'A Receber' ou 'A Pagar'"
    )
    descricao: str = Field(
        ...,
        max_length=255,
        example="Aluguel de Outubro",
        description="Descrição da conta",
    )
    valor: float = Field(
        ...,
        example=1500.00,
        description="Valor da conta (pode ser negativo para contas a pagar)",
    )
    data_vencimento: date = Field(
        ..., example="2025-10-05", description="Data de vencimento da conta"
    )

    class Config:
        from_attributes = True


# Schema para a resposta da criação de uma conta
class ContaResponse(BaseModel):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        example=str(uuid.uuid4()),
        description="ID da conta gerado automaticamente",
    )
    tipo: str = Field(..., example="A Receber")
    descricao: str = Field(..., max_length=255)
    valor: float = Field(..., example=1500.00)
    data_vencimento: date
    data_emissao: datetime

    class Config:
        from_attributes = True


# Schema para a atualização de uma conta (PUT)
class ContaUpdate(BaseModel):
    tipo: Optional[str] = Field(None, example="A Receber")
    descricao: Optional[str] = Field(None, max_length=255)
    valor: Optional[float] = Field(None, example=1500.00)
    data_vencimento: Optional[date] = Field(None, example="2025-10-05")

    class Config:
        from_attributes = True


# Schema para a resposta de todas as contas (GET ALL)
class ContasListResponse(BaseModel):
    id: str
    tipo: str
    descricao: str
    valor: float
    data_vencimento: date
    data_emissao: datetime

    class Config:
        from_attributes = True


# Schema para deletar uma conta (DELETE)
class ContaDeleteResponse(BaseModel):
    id: str
    mensagem: str = "Conta deletada com sucesso"

    class Config:
        from_attributes = True

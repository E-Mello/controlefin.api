# Path: app/models/contas.py

from sqlalchemy import Column, String, Integer, Enum, Date, DECIMAL, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy.orm import validates
from datetime import datetime

Base = declarative_base()


class Contas(Base):
    __tablename__ = "contas"

    # ID da conta (UUID como string)
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Tipo da conta (A Receber ou A Pagar)
    tipo = Column(Enum("A Receber", "A Pagar", name="tipo_conta"), nullable=False)

    # Descrição da conta
    descricao = Column(String(255), nullable=False)

    # Valor da conta (pode ser positivo ou negativo)
    valor = Column(DECIMAL(15, 2), nullable=False)

    # Data de vencimento
    data_vencimento = Column(Date, nullable=False)

    # Data de emissão (definido automaticamente como o timestamp atual)
    data_emissao = Column(TIMESTAMP, default=datetime.utcnow)

    # Método de validação para garantir que o tipo seja válido
    @validates("tipo")
    def validate_tipo(self, key, value):
        if value not in ["A Receber", "A Pagar"]:
            raise ValueError("O tipo deve ser 'A Receber' ou 'A Pagar'")
        return value

    def __repr__(self):
        return f"<Conta(id={self.id}, tipo={self.tipo}, descricao={self.descricao}, valor={self.valor}, data_vencimento={self.data_vencimento}, data_emissao={self.data_emissao})>"

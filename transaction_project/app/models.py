from typing import Any

from app.db import Base
from sqlalchemy import DECIMAL, Column, Integer, String


class Transaction(Base):
    __tablename__ = "transaction"

    id: Column[int] = Column(Integer, primary_key=True, autoincrement=True)
    amount: Column[DECIMAL] = Column(DECIMAL(precision=10, scale=2))
    currency: Column[str] = Column(String(3))
    timestamp: Column[int] = Column(Integer)
    description: Column[str] = Column(String)

    def __init__(
        self,
        amount: Column[DECIMAL],
        currency: Column[str],
        timestamp: Column[int],
        description: Column[str],
    ):
        self.amount = amount
        self.currency = currency
        self.timestamp = timestamp
        self.description = description

    def serialize(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "amount": self.amount,
            "currency": self.currency,
            "timestamp": self.timestamp,
            "description": self.description,
        }

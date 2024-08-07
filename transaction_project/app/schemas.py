from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field, field_validator


class Transaction(BaseModel):
    id: int
    amount: Decimal = Field(ge=0.01, decimal_places=2)
    currency: str  # TODO: use enum
    timestamp: int
    description: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 13,
                    "amount": "35.4",
                    "currency": "USD",
                    "timestamp": 1653624000,
                    "description": "Transfer to bank account",
                }
            ]
        },
        "from_attributes": True,
    }


class TransactionCreate(BaseModel):
    amount: Decimal = Field(ge=0.01, decimal_places=2)
    currency: str
    timestamp: int
    description: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "amount": "35.4",
                    "currency": "USD",
                    "timestamp": 1653624000,
                    "description": "Transfer to bank account",
                }
            ]
        },
    }


class TransactionUpdate(BaseModel):
    amount: Decimal | None = Field(ge=0.01, decimal_places=2, default=None)
    currency: str | None = None
    timestamp: int | None = None
    description: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "amount": "36.6",
                    "description": "Transfer from bank account",
                }
            ]
        },
    }

    def fields_with_values(self) -> dict[str, Any]:
        return {k: v for k, v in self.model_dump().items() if v is not None}

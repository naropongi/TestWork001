from typing import Any

from app.db import get_session
from app.models import Transaction
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


class TransactionRepository:
    @staticmethod
    async def get_by_id(
        transaction_id: int,
    ) -> Transaction | None:
        async with get_session() as session:
            statement = select(Transaction).where(Transaction.id == transaction_id)
            return await session.scalar(statement)

    @staticmethod
    async def save_from_dict(
        transaction: dict,
    ) -> Transaction:
        async with get_session() as session:
            transaction_obj = Transaction(**transaction)
            session.add(transaction_obj)
            try:
                await session.commit()
            except (
                IntegrityError
            ):  # TODO: this exception should be handled better cause it is not a primary key only
                raise ValueError("Transaction already exists")

            return transaction_obj

    @staticmethod
    async def update_transaction(
        transaction_id: int,
        fields_to_update: dict[str, Any],
    ) -> Transaction:
        async with get_session() as session:
            transaction = await session.scalar(
                select(Transaction).where(Transaction.id == transaction_id)
            )
            if not transaction:
                raise ValueError("Transaction not found")

            for field, value in fields_to_update.items():
                setattr(transaction, field, value)
            await session.commit()

            return transaction

    @staticmethod
    async def delete_by_id(
        transaction_id: int,
    ) -> None:
        async with get_session() as session:
            transaction = await session.scalar(
                select(Transaction).where(Transaction.id == transaction_id)
            )

            if not transaction:
                ValueError("Transaction not found")

            await session.delete(transaction)
            await session.commit()

from app.models import Transaction
from app.repos import TransactionRepository
from app.schemas import Transaction as TransactionSchema
from app.schemas import TransactionCreate as TransactionCreateSchema
from app.schemas import TransactionUpdate as TransactionUpdateSchema
from app.tasks import send_email_notification


async def get_transaction_by_id(transaction_id: int) -> TransactionSchema | None:
    if transaction := await TransactionRepository.get_by_id(transaction_id):
        return TransactionSchema.model_validate(transaction)
    else:
        raise ValueError("Transaction not found")


async def save_transaction(transaction: TransactionCreateSchema) -> TransactionSchema:
    result = await TransactionRepository.save_from_dict(transaction.model_dump())
    notify_transaction_created(result)
    return TransactionSchema.model_validate(result)


async def update_transaction(
    transaction_id: int, transaction_update: TransactionUpdateSchema
) -> TransactionSchema:
    fields_to_update = transaction_update.fields_with_values()
    result_transaction = await TransactionRepository.update_transaction(
        transaction_id, fields_to_update
    )
    return TransactionSchema.model_validate(result_transaction)


async def delete_transaction_by_id(transaction_id: int) -> None:
    await TransactionRepository.delete_by_id(transaction_id)


def notify_transaction_created(transaction: Transaction) -> None:
    send_email_notification.delay(transaction.serialize())  # type: ignore

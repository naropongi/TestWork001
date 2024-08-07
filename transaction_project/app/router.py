from app.schemas import Transaction as TransactionSchema
from app.schemas import TransactionCreate as TransactionCreateSchema
from app.schemas import TransactionUpdate as TransactionUpdateSchema
from app.service import (
    delete_transaction_by_id,
    get_transaction_by_id,
    save_transaction,
    update_transaction,
)
from fastapi import APIRouter, HTTPException

router = APIRouter()

not_found_response = {
    404: {
        "description": "Not found",
        "content": {
            "application/json": {"example": {"detail": "Transaction not found"}}
        },
    },
}

already_exists_response = {
    409: {
        "description": "Already exists",
        "content": {
            "application/json": {"example": {"detail": "Transaction already exists"}}
        },
    },
}

internal_server_error_response = {
    500: {
        "description": "Internal server error",
        "content": {
            "application/json": {"example": {"detail": "Something went wrong"}}
        },
    },
}


@router.get(
    "/transaction/{transaction_id}",
    responses={
        **not_found_response,
        **internal_server_error_response,
    },
)
async def get_transaction(transaction_id: int) -> TransactionSchema | None:
    try:
        return await get_transaction_by_id(transaction_id)
    except ValueError as e:
        if e.args and e.args[0] == "Transaction not found":
            raise HTTPException(status_code=404, detail=e.args[0])
        else:
            raise HTTPException(status_code=500, detail="Something went wrong")


@router.post(
    "/transaction",
    responses={
        **already_exists_response,
        **internal_server_error_response,
    },
)
async def post_transaction(transaction: TransactionCreateSchema) -> TransactionSchema:
    try:
        return await save_transaction(transaction)
    except ValueError as e:
        if e.args and e.args[0] == "Transaction already exists":
            raise HTTPException(status_code=409, detail=e.args[0])
        else:
            raise HTTPException(status_code=500, detail="Something went wrong")


@router.patch(
    "/transaction/{transaction_id}",
    responses={
        **not_found_response,
        **internal_server_error_response,
    },
)
async def patch_transaction(
    transaction_id: int, transaction_update: TransactionUpdateSchema
) -> TransactionSchema:
    try:
        return await update_transaction(transaction_id, transaction_update)
    except ValueError as e:
        if e.args and e.args[0] == "Transaction not found":
            raise HTTPException(status_code=404, detail=e.args[0])
        else:
            raise HTTPException(status_code=500, detail="Something went wrong")


@router.delete(
    "/transaction/{transaction_id}",
    responses={
        **not_found_response,
        **internal_server_error_response,
    },
    response_description="Transaction deleted successfully",
)
async def delete_transaction(transaction_id: int) -> None:
    try:
        await delete_transaction_by_id(transaction_id)
    except ValueError as e:
        if e.args and e.args[0] == "Transaction not found":
            raise HTTPException(status_code=404, detail=e.args[0])
        else:
            raise HTTPException(status_code=500, detail="Something went wrong")

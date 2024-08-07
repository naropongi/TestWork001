from decimal import Decimal
from unittest.mock import patch

from app.main import app
from app.models import Transaction
from fastapi.testclient import TestClient

client = TestClient(app)


@patch("app.service.notify_transaction_created")
@patch("app.repos.TransactionRepository.save_from_dict")
def test_post_transaction(mock, notify_mock):
    transaction = {
        "id": 1,
        "amount": "35.41",
        "currency": "USD",
        "timestamp": 1653624000,
        "description": "Transfer to bank account",
    }

    mock.return_value = Transaction(**transaction)

    response = client.post(
        "/transaction",
        json=transaction,
    )

    assert response.status_code == 200
    assert response.json() == {**transaction}

    assert mock.call_count == 1
    assert mock.call_args_list[0][0] == (
        {
            **{k: v for k, v in transaction.items() if k != "id"},
            "amount": Decimal("35.41"),
        },
    )


def test_negative_post_transaction():
    response = client.post(
        "/transaction",
        json={
            "id": 34,
            "amount": "35.41",
            "currency": "USD",
            "timestamp": 1653624000.222,
            "description": "Transfer to bank account",
        },
    )

    assert response.status_code == 422


@patch("app.repos.TransactionRepository.get_by_id")
def test_get_transaction(mock):
    transaction = {
        "id": 34,
        "amount": "35.41",
        "currency": "USD",
        "timestamp": 1653624000,
        "description": "Transfer to bank account",
    }

    mock.return_value = Transaction(**transaction)

    response = client.get("/transaction/34")

    assert response.status_code == 200
    assert response.json() == transaction

    assert mock.call_count == 1
    assert mock.call_args_list[0][0] == (34,)


@patch("app.repos.TransactionRepository.get_by_id")
def test_negative_get_transaction(mock):
    mock.return_value = None
    response = client.get("/transaction/34")

    assert response.status_code == 404

    assert mock.call_count == 1
    assert mock.call_args_list[0][0] == (34,)


@patch("app.repos.TransactionRepository.update_transaction")
def test_patch_transaction(mock):
    transaction = {
        "id": 12,
        "amount": "35.41",
        "currency": "USD",
        "timestamp": 1653624000,
        "description": "Transfer to bank account",
    }
    mock.return_value = Transaction(**transaction)

    response = client.patch(
        "/transaction/12",
        json={
            "description": "Transfer FROM bank account",
        },
    )

    assert response.status_code == 200

    assert mock.call_count == 1
    assert mock.call_args_list[0][0] == (
        12,
        {"description": "Transfer FROM bank account"},
    )


def test_negative_patch_transaction():
    response = client.patch(
        "/transaction/12",
        json={
            "amount": "35.666",
        },
    )

    assert response.status_code == 422


@patch("app.repos.TransactionRepository.delete_by_id")
def test_delete_transaction(mock):
    response = client.delete("/transaction/123")

    assert response.status_code == 200

    assert mock.call_count == 1
    assert mock.call_args_list[0][0] == (123,)


@patch("app.repos.TransactionRepository.delete_by_id")
def test_negative_delete_transaction(mock):
    mock.side_effect = ValueError("Transaction not found")

    response = client.delete("/transaction/0")

    assert response.status_code == 404

    assert mock.call_count == 1
    assert mock.call_args_list[0][0] == (0,)

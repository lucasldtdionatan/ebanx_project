from fastapi import status
from fastapi.testclient import TestClient
from apps.main import app, accounts_manager

client = TestClient(app)


def test_reset_accounts():
    response = client.post("/reset")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "State reset successfully"}


def test_get_balance_for_non_existing_account():
    response = client.get("/balance", params={"account_id": 1234})

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Account not found"}


def test_create_account_with_initial_balance():
    data = {"type": "deposit", "destination": "100", "amount": 10}
    response = client.post("/event", json=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"destination": {"id": "100", "balance": 10}}


def test_deposit_into_existing_account():
    accounts_manager.accounts["100"] = 10
    data = {"type": "deposit", "destination": "100", "amount": 10}
    response = client.post("/event", json=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"destination": {"id": "100", "balance": 20}}


def test_get_balance_for_existing_account():
    accounts_manager.accounts["100"] = 20
    response = client.get("/balance", params={"account_id": 100})
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == 20


def test_withdraw_from_non_existing_account():
    data = {"type":"withdraw", "origin":"200", "amount":10}
    response = client.post("/event", json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_withdraw_from_existing_account():
    accounts_manager.accounts["100"] = 20
    data = {"type": "withdraw", "origin": "100", "amount": 5}
    response = client.post("/event", json=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"origin": {"id": "100", "balance": 15}}


def test_wihdraw_of_greater_value_than_have_in_the_account():
    accounts_manager.accounts["100"] = 20
    data = {"type": "withdraw", "origin": "100", "amount": 25}
    response = client.post("/event", json=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "You do not have this value available, your balance: 20"}


def test_transfer_from_existing_account():
    accounts_manager.accounts["100"] = 15

    data = {"type": "transfer", "origin": "100", "amount": 15, "destination": "300"}
    response = client.post("/event", json=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "origin": {"id": "100", "balance": 0}, 
        "destination": {"id": "300", "balance": 15}
    }


def test_from_non_existing_account():
    data = {"type": "transfer", "origin": "200", "amount": 15, "destination": "300"}
    response = client.post("/event", json=data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
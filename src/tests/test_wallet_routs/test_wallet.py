import pytest
from src.application.dtos.wallet import DeleteType
from src.application.dtos.operation import OperationType


@pytest.mark.asyncio
async def test_create_wallet(client):
    response = await client.post("/api/v1/wallets/create", json={"balance": 100})
    wallet = response.json()["result"]
    wallet_uuid = wallet["uuid"]
    wallet_by_uuid = await client.get(f"/api/v1/wallets/{wallet_uuid}")
    assert response.status_code == 201
    assert wallet == wallet_by_uuid.json()["result"]


@pytest.mark.asyncio
async def test_get_list_wallets(client):
    await client.post("/api/v1/wallets/create", json={"balance": 100})
    await client.post("/api/v1/wallets/create", json={"balance": 100})
    await client.post("/api/v1/wallets/create", json={"balance": 100})

    response = await client.get("/api/v1/wallets/")
    wallets_list = response.json()

    assert len(wallets_list["result"]) == 3


@pytest.mark.asyncio
async def test_delete(client):
    await client.post("/api/v1/wallets/create", json={"balance": 100})
    await client.post("/api/v1/wallets/create", json={"balance": 100})
    response_wallet = await client.post("/api/v1/wallets/create", json={"balance": 100})

    response_list = await client.get("/api/v1/wallets/")
    wallets_list = response_list.json()["result"]
    assert len(wallets_list) == 3

    wallet = response_wallet.json()["result"]
    del_res = await client.delete(
        f"/api/v1/wallets/{DeleteType.only_empty_wallet.value}",
        params={"wallet_uuid": wallet["uuid"]},
    )
    assert 400 == del_res.status_code

    del_res_2 = await client.delete(
        f"/api/v1/wallets/{DeleteType.not_empty_wallet.value}",
        params={"wallet_uuid": wallet["uuid"]},
    )

    assert 202 == del_res_2.status_code

    response_list_2 = await client.get("/api/v1/wallets/")
    wallets_list_2 = response_list_2.json()["result"]

    assert len(wallets_list_2) == 2


@pytest.mark.asyncio
async def test_operation_deposit(client):
    wallet_res = await client.post("/api/v1/wallets/create", json={"balance": 100})
    wallet = wallet_res.json()["result"]

    operation_depos_res = await client.post(
        f"/api/v1/wallets/{wallet["uuid"]}/operation",
        json={"operation": f"{OperationType.deposit.value}", "amount": 100},
    )
    assert 202 == operation_depos_res.status_code

    wallet_res_2 = await client.get(f"/api/v1/wallets/{wallet["uuid"]}")
    wallet_2 = wallet_res_2.json()["result"]

    assert wallet_2["balance"] == "200.00"


@pytest.mark.asyncio
async def test_operation_withdraw(client):
    wallet_res = await client.post("/api/v1/wallets/create", json={"balance": 100})
    wallet = wallet_res.json()["result"]

    operation_depos_res = await client.post(
        f"/api/v1/wallets/{wallet["uuid"]}/operation",
        json={"operation": f"{OperationType.withdraw.value}", "amount": 100},
    )
    assert 202 == operation_depos_res.status_code

    wallet_res_2 = await client.get(f"/api/v1/wallets/{wallet["uuid"]}")
    wallet_2 = wallet_res_2.json()["result"]

    assert wallet_2["balance"] == "0.00"

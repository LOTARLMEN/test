from decimal import Decimal

from fastapi import APIRouter, HTTPException, status
from uuid import UUID
from src.application.dtos.operation import OperationBody, OperationType
from src.application.dtos.wallet import (
    WalletCreate,
    DeleteType,
    WalletResponse,
)
from src.infrastructure import (
    DeleteUsecase,
    GetUsecase,
    DepositUsecase,
    WithdrawUsecase,
    CreateUsecase,
)

router = APIRouter(prefix="/api/v1/wallets", tags=["Wallets"])


@router.get("/{wallet_uuid}", response_model=WalletResponse)
async def get_wallet(
    wallet_uuid: str,
    get_uc: GetUsecase,
) -> WalletResponse:
    valid_uuid = UUID(wallet_uuid)
    wallet = await get_uc.get_wallet_by_uuid(valid_uuid)
    return wallet


@router.post(
    "/{wallet_uuid}/operation",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=WalletResponse,
)
async def wallet_operation(
    wallet_uuid: UUID,
    operation: OperationBody,
    deposit_uc: DepositUsecase,
    withdraw_uc: WithdrawUsecase,
) -> WalletResponse:
    amount = Decimal(operation.amount)

    if operation.operation == OperationType.deposit:
        return await deposit_uc.execute(wallet_uuid, amount)

    if operation.operation == OperationType.withdraw:
        return await withdraw_uc.execute(wallet_uuid, amount)

    raise HTTPException(status_code=400, detail="Unknown operation type")


@router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=WalletResponse
)
async def create_wallet(wallet: WalletCreate, uc: CreateUsecase) -> WalletResponse:
    new_wallet = await uc.execute(wallet)
    return new_wallet


@router.get("/", response_model=list[WalletResponse])
async def get_wallets(uc: GetUsecase) -> list[WalletResponse]:
    wallets = await uc.get_wallets()
    return wallets


@router.delete("/{delete_type}", status_code=status.HTTP_202_ACCEPTED)
async def delete_wallet(
    wallet_uuid: str, delete_type: DeleteType, uc: DeleteUsecase
) -> dict[str, str]:
    valid_uuid = UUID(wallet_uuid)
    await uc.execute(valid_uuid, delete_type)
    return {"result": f"Wallet {valid_uuid} was deleted"}

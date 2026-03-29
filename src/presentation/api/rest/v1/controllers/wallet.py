from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.db.session import get_async_session
from src.infrastructure.db.models.wallet_model import Wallet
from src.application.dtos.schemas import OperationBody, OperationType

router = APIRouter(prefix="/api/v1/wallets", tags=["Wallets"])


@router.get("/{uuid}")
async def get_wallet(uuid: str, db: AsyncSession = Depends(get_async_session)):
    valid_uuid = UUID(uuid)
    wallet = await Wallet.get_wallet_by_uuid(db, valid_uuid)
    return {"result": wallet}


@router.post("/{uuid}/operation")
async def wallet_operation(uuid: str, operation_body: OperationBody,
                           db: AsyncSession = Depends(get_async_session)):
    try:
        valid_uuid = UUID(uuid)

        if operation_body.operation == OperationType.deposit:
            wallet = await Wallet.deposit(db, valid_uuid, operation_body.amount)
        else:
            wallet = await Wallet.withdraw(db, valid_uuid, operation_body.amount)

        await db.commit()

        return {"status": "success", "balance": wallet.balance}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))



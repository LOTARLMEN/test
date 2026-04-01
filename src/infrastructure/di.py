from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.db.session import get_async_session
from src.infrastructure.db.uow import UnitOfWork
from src.application.usecases.wallet import (
    DepositUseCase,
    CreateUseCase,
    DeleteUseCase,
    WithdrawUseCase,
    GetWalletUseCase,
)

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


def get_uow(session: SessionDep) -> UnitOfWork:
    return UnitOfWork(session)


uow_depends = Annotated[UnitOfWork, Depends(get_uow)]


async def get_create_wallet_usecase(uow: uow_depends) -> CreateUseCase:
    return CreateUseCase(uow)


async def get_deposit_usecase(uow: uow_depends) -> DepositUseCase:
    return DepositUseCase(uow)


async def get_delete_usecase(uow: uow_depends) -> DeleteUseCase:
    return DeleteUseCase(uow)


async def get_withdraw_usecase(uow: uow_depends) -> WithdrawUseCase:
    return WithdrawUseCase(uow)


async def get_wallet_usecase(uow: uow_depends) -> GetWalletUseCase:
    return GetWalletUseCase(uow)


DeleteUsecase = Annotated[DeleteUseCase, Depends(get_delete_usecase)]
GetUsecase = Annotated[GetWalletUseCase, Depends(get_wallet_usecase)]
DepositUsecase = Annotated[DepositUseCase, Depends(get_deposit_usecase)]
WithdrawUsecase = Annotated[WithdrawUseCase, Depends(get_withdraw_usecase)]
CreateUsecase = Annotated[CreateUseCase, Depends(get_create_wallet_usecase)]

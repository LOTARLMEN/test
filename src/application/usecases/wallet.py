import uuid as uuid_pkg

from ..exceptions import (
    InsufficientFundsError,
    WalletNotEmptyError,
    WalletNotFoundError,
)

from src.infrastructure import UnitOfWork
from src.application.dtos import WalletCreate, WalletResponse
from src.infrastructure.db.models import Wallet


class WalletUseCase:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow


class GetWalletUseCase(WalletUseCase):

    async def get_wallets(self):
        async with self.uow:
            wallets = await self.uow.wallets.get_wallets()
            return [WalletResponse.model_validate(wallet) for wallet in wallets]

    async def get_wallet_by_uuid(self, uuid: uuid_pkg.UUID):
        async with self.uow:
            wallet = await self.uow.wallets.get_by_uuid(uuid)
            return WalletResponse.model_validate(wallet)


class WithdrawUseCase(WalletUseCase):

    async def execute(self, uuid, amount):
        async with self.uow:
            wallet = await self.uow.wallets.get_by_uuid(uuid, for_update=True)

            if not wallet:
                raise WalletNotFoundError

            if wallet.balance < amount:
                raise InsufficientFundsError

            wallet.balance -= amount

            await self.uow.commit()
            await self.uow.session.refresh(wallet)

            return WalletResponse.model_validate(wallet)


class DepositUseCase(WalletUseCase):

    async def execute(self, uuid, amount):
        async with self.uow:
            wallet = await self.uow.wallets.get_by_uuid(uuid, for_update=True)

            if not wallet:
                raise WalletNotFoundError

            wallet.balance += amount

            await self.uow.commit()
            await self.uow.session.refresh(wallet)

            return WalletResponse.model_validate(wallet)


class DeleteUseCase(WalletUseCase):

    async def execute(self, uuid: uuid_pkg.UUID):
        async with self.uow:
            wallet = await self.uow.wallets.get_by_uuid(uuid)

            if not wallet:
                raise WalletNotFoundError

            if wallet.balance != 0:
                raise WalletNotEmptyError

            await self.uow.wallets.delete(wallet)
            await self.uow.commit()


class CreateUseCase(WalletUseCase):

    async def execute(self, wallet: WalletCreate):
        async with self.uow:
            new_wallet = Wallet(**wallet.model_dump())

            await self.uow.wallets.add(new_wallet)
            await self.uow.commit()

            await self.uow.session.refresh(new_wallet)

            return WalletResponse.model_validate(new_wallet)

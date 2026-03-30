import uuid as uuid_pkg
from src.infrastructure import UnitOfWork
from src.application.dtos import WalletCreate
from src.infrastructure.db.models import Wallet


class WalletUseCase:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow


class GetWalletUseCase(WalletUseCase):

    async def get_wallets(self):
        async with self.uow:
            wallets = await self.uow.wallets.get_wallets()
            return wallets

    async def get_wallet_by_uuid(self, uuid: uuid_pkg.UUID):
        async with self.uow:
            wallet = await self.uow.wallets.get_by_uuid(uuid)
            return wallet


class WithdrawUseCase(WalletUseCase):

    async def execute(self, uuid, amount):
        async with self.uow:
            wallet = await self.uow.wallets.get_by_uuid(uuid, for_update=True)

            if not wallet:
                raise Exception("Not found")

            if wallet.balance < amount:
                raise Exception("Not enough money")

            wallet.balance -= amount

            await self.uow.commit()


class DepositUseCase(WalletUseCase):

    async def execute(self, uuid, amount):
        async with self.uow:
            wallet = await self.uow.wallets.get_by_uuid(uuid, for_update=True)

            if not wallet:
                raise Exception("Not found")

            wallet.balance += amount

            await self.uow.commit()


class DeleteUseCase(WalletUseCase):

    async def execute(self, uuid: uuid_pkg.UUID):
        async with self.uow:
            wallet = await self.uow.wallets.get_by_uuid(uuid)

            if not wallet:
                raise Exception("Wallet not found")

            if wallet.balance != 0:
                raise Exception("Cannot delete wallet with balance")

            await self.uow.wallets.delete(wallet)
            await self.uow.commit()


class CreateUseCase(WalletUseCase):

    async def execute(self, wallet: WalletCreate):
        async with self.uow:
            new_wallet = Wallet(**wallet.model_dump())

            await self.uow.wallets.add(new_wallet)
            await self.uow.commit()

            await self.uow.session.refresh(new_wallet)

            return new_wallet

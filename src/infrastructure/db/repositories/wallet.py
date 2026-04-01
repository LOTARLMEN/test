from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.db.models.wallet import Wallet
import uuid as uuid_pkg


class WalletRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_wallets(self) -> Sequence[Wallet]:
        result = await self.session.execute(select(Wallet))
        return result.scalars().all()

    async def get_by_uuid(
        self, uuid: uuid_pkg.UUID, for_update: bool = False
    ) -> Wallet | None:
        stmt = select(Wallet).where(Wallet.uuid == uuid)

        if for_update:
            stmt = stmt.with_for_update()

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, wallet: Wallet) -> None:
        await self.session.delete(wallet)

    async def add(self, wallet: Wallet) -> None:
        self.session.add(wallet)

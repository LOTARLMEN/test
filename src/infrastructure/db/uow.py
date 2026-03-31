from sqlalchemy.ext.asyncio import AsyncSession
from .repositories import WalletRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.wallets = WalletRepository(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

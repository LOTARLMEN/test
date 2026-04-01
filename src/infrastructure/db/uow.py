from traceback import TracebackException
from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.db.repositories.wallet import WalletRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.wallets = WalletRepository(session)

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(
        self, exc_type: Exception, exc_val: TracebackException, exc_tb: TracebackType
    ) -> None:
        if exc_type:
            await self.session.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

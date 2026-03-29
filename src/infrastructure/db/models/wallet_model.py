import uuid as uuid_pkg
from datetime import datetime
from decimal import Decimal

from sqlalchemy import UUID, select, Numeric, DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass



class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True),
                                                default=uuid_pkg.uuid4,
                                                unique=True,
                                                index=True)

    balance: Mapped[Decimal] = mapped_column(Numeric(precision=15, scale=2), default=Decimal("0.00"))

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )


    @classmethod
    async def get_wallet_by_uuid(cls, conn: AsyncSession, uuid: uuid_pkg.UUID):
        result = await conn.execute(select(cls).where(cls.uuid == uuid))
        return result.scalar_one_or_none()

    @classmethod
    async def withdraw(cls, conn: AsyncSession, uuid: uuid_pkg.UUID, amount: int):
        wallet = await conn.execute(select(cls).where(cls.uuid == uuid).with_for_update())
        wallet = wallet.scalar_one_or_none()
        if wallet:
            if wallet.balance >= amount:
                wallet.balance -= amount
                await conn.commit()
            else:
                raise Exception("The balance must be greater than zero.")
        else:
            raise Exception("The wallet is not in the database")

        return wallet

    @classmethod
    async def deposit(cls, conn: AsyncSession, uuid: uuid_pkg.UUID, amount: int):
        wallet = await conn.execute(select(cls).where(cls.uuid == uuid).with_for_update())
        wallet = wallet.scalar_one_or_none()
        if wallet:
            wallet.balance += amount
            await conn.commit()
        else:
            raise Exception("The wallet is not in the database")

        return wallet

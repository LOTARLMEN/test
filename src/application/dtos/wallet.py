from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WalletCreate(BaseModel):
    balance: Decimal = Decimal("0.00")


class WalletResponse(BaseModel):
    uuid: UUID
    balance: Decimal

    model_config = ConfigDict(from_attributes=True)


class WalletListResponse(BaseModel):
    result: list[WalletResponse]


class WalletSingleResponse(BaseModel):
    result: WalletResponse

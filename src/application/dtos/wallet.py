from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WalletCreate(BaseModel):
    balance: Decimal = Decimal("0.00")


class WalletResponse(BaseModel):
    id: int
    uuid: UUID
    balance: Decimal

    model_config = ConfigDict(from_attributes=True)


class DeleteType(Enum):
    only_empty_wallet = "ONLY EMPTY WALLET"
    not_empty_wallet = "NOT EMPTY WALLET"

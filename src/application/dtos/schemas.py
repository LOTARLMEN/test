from pydantic import BaseModel
import enum


class OperationType(enum.Enum):
    deposit = "DEPOSIT"
    withdraw = "WITHDRAW"


class OperationBody(BaseModel):

    operation: OperationType
    amount: int



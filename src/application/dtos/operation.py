from pydantic import BaseModel, Field
import enum


class OperationType(enum.Enum):
    deposit = "DEPOSIT"
    withdraw = "WITHDRAW"


class OperationBody(BaseModel):
    operation: OperationType = Field(
        ..., description="DEPOSIT for deposit\nWITHDRAW for withdraw"
    )
    amount: int

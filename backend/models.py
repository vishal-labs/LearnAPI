from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class onBoardUser(BaseModel):
    username: str
    email: EmailStr
    password: str

class loginUser(BaseModel):
    email: EmailStr
    password: str

class onlyEmail(BaseModel):
    email: EmailStr

class makeUserAdmin(BaseModel):
    email : EmailStr
    adminKey : str
class transactionTransfer(BaseModel):
    fromUserEmail: EmailStr
    toUserEmail: EmailStr
    transactionAmount: int
class transactionWithdrawal(transactionTransfer):
    toUserEmail : Optional[EmailStr] = Field(None, description="Null for withdrawals")

class transactionDeposit(transactionTransfer):
    fromUserEmail: Optional[EmailStr] = Field(None, description="Null for deposits")

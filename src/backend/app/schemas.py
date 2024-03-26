from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# TRANSACTION SCHEMAS
# -----------------------------------------------------------------------------
class transactionBase(BaseModel):
    amount: int
    date: str
    transactionType: str

class createTransaction(transactionBase):
    balance: float

class Transaction(transactionBase):
    transactionID: int
    accountID: int

    class Config:
        from_attributes = True

class updateTransaction(BaseModel):
    amount: Optional[int] = None
    balance: Optional[float] = None


# ACCOUNT SCHEMAS
# -----------------------------------------------------------------------------
class accountBase(BaseModel):
    date: str
    balance: float
    accountType: str


class accountCreate(accountBase):
    pass

class Account(accountBase):
    accountID: int
    userID: int
    transaction = list[Transaction] = []

    class Config:
        from_attributes = True

class accountUpdate(BaseModel):
    name: Optional[str] = None
    balance: Optional[float] = None



# USER SCHEMAS
# -----------------------------------------------------------------------------
class userBase(BaseModel):
    name: str
    email: str

class userCreate(userBase):
    password: str

class User(userBase):
    id: int
    isActive: bool
    accounts = list[Account] = []

    class Config:
        from_attributes = True

class userUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    isActive: Optional[bool] = None
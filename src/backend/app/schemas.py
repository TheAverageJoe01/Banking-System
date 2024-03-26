from typing import Optional
from pydantic import BaseModel, ConfigDict
from .schemas import Account


# TRANSACTION SCHEMAS
# -----------------------------------------------------------------------------
class transactionBase(BaseModel):
    amount: int
    date: str
    transaction_type: str

class createTransaction(transactionBase):
    balance: float

class Transaction(transactionBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class updateTransaction(BaseModel):
    amount: Optional[int] = None
    balance: Optional[float] = None


# ACCOUNT SCHEMAS
# -----------------------------------------------------------------------------
class accountBase(BaseModel):
    name: str
    date: str
    balance: float
    account_type: str


class accountCreate(accountBase):
    pass

class Account(accountBase):
    id: int
    transaction = list[Transaction] = []

    class Config:
        from_attributes = True

class accountUpdate(BaseModel):
    name: Optional[str] = None
    balance: Optional[float] = None



# USER SCHEMAS
# -----------------------------------------------------------------------------
class userBase(BaseModel):
    email: str

class userCreate(userBase):
    password: str

class User(userBase):
    id: int
    is_active: bool
    accounts = list[Account] = []

    class Config:
        from_attributes = True

class userUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
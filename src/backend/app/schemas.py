from typing import Optional
from pydantic import BaseModel, ConfigDict
from .schemas import Account


# TRANSACTION SCHEMAS
# -----------------------------------------------------------------------------
class transactionBase(BaseModel):
    id: int
    user_id: int
    amount: int
    date: str
    transaction_type: str
    balance: float

class createTransaction(transactionBase):
    user_id: int
    amount: int
    date: str
    transaction_type: str
    balance: float

class Transaction(transactionBase):
    id: int
    user_id: int
    amount: int
    date: str
    transactionType: str
    balance: float

    class Config:
        from_attributes = True

class updateTransaction(BaseModel):
    amount: Optional[int] = None
    date: Optional[str] = None
    transaction_type: Optional[str] = None
    balance: Optional[float] = None


# ACCOUNT SCHEMAS
# -----------------------------------------------------------------------------
class accountBase(BaseModel):
    id: int
    name: str
    balance: float
    accountType: str


class accountCreate(accountBase):
    name: str
    balance: float
    accountType: str

class Account(accountBase):
    id: int
    name: str
    balance: float
    accountType: str
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
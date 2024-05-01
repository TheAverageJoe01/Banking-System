from typing import Optional
from pydantic import BaseModel
from datetime import datetime

# TRANSACTION SCHEMAS
# -----------------------------------------------------------------------------
class transactionBase(BaseModel):
    amount: int
    date: str
    transactionType: str
#Base transaction class that defines the structure and data of any transaction type

class createTransaction(transactionBase):
    balance: float
#A class that extends the transaction base by adding a balance which will be used in deposits and withdraws

class Transaction(transactionBase):
    transactionID: int
    accountID: int

    class Config:
        from_attributes = True
#Transaction which extends the transactionbase with an accountID and transactionID
        
class updateTransaction(BaseModel):
    amount: Optional[int] = None
    balance: Optional[float] = None


# ACCOUNT SCHEMAS
# -----------------------------------------------------------------------------
class accountBase(BaseModel):
    #date: str
    balance: float
    accountType: str
    accountNumber: int
    userID: int
#Base details and structure for the account model like balance and account type that uses the basemodel


class accountCreate(accountBase):
    #accountNumber: int
    pass
#Schema to create the account that extends the account base defined above

class Account(accountBase):
    pass
    #transaction = list[Transaction] = []

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
#Contains the base structure and variables of the user model

class userCreate(userBase):
    password: str
#A class that extends the userbase class by adding a password that is defined by the user when creating an account

class User(userBase):
    id: int
    isActive: bool
    #accounts = list[Account] = []
#Extends the userbase class by adding a ID for the user as well as if the user is active (deleted/not deleted)

    class Config:
        from_attributes = True

class userUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    isActive: Optional[bool] = None
#A class to update the users information such as email and password
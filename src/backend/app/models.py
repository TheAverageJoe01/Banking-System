from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from datetime import datetime

from app.database import Base



# Create a class that will be used to create a table of users in the database
class User(Base):
    __tablename__ = 'users'
    #sets the name in the database to be users

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    isActive = Column(Boolean, default=True)
    #sets up the variables to be used in the user class

    accounts = relationship("Account", back_populates="user")
    #Establishes a relationship between the account and user class
    
# Create a class that will be used to create a table of accounts in the database
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    accountNumber = Column(Integer, unique=True, index=True)
    balance = Column(Float, index=True)
    accountType = Column(String, index=True)
    userID = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")
    #Establishes the relationships between the user and transaction classes

# Create a class that will be used to create a table of transactions in the database
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    accountID = Column(Integer, ForeignKey('accounts.id'))
    amount = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    transactionType = Column(String)
    balance = Column(Float)

    account = relationship("Account", back_populates="transactions")
    #Again, sets the relationships between the transaction and account class


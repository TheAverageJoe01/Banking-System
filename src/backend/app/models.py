from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship


from app.database import Base



# Create a class that will be used to create a table of users in the database
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    isActive = Column(Boolean, default=True)

    accounts = relationship("Account", back_populates="user")
    
# Create a class that will be used to create a table of accounts in the database
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    accountNumber = Column(Integer, index=True)
    balance = Column(Float, index=True)
    accountType = Column(String, index=True)
    userID = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

# Create a class that will be used to create a table of transactions in the database
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    accountID = Column(Integer, ForeignKey('accounts.id'))
    amount = Column(Float)
    date = Column(Date)
    transactionType = Column(String)
    balance = Column(Float)

    account = relationship("Account", back_populates="transactions")


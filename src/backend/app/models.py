from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.orm import relationship


from app.database import Base



# Create a class that will be used to create a table of users in the database
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    account = relationship("Account", back_populates="User")
    
# Create a class that will be used to create a table of accounts in the database
class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    balance = Column(float, index=True)
    accountType = Column(String, index=True)

    user = relationship("User", back_populates="Account")
    transactions = relationship("Transaction", back_populates="Account")

# Create a class that will be used to create a table of transactions in the database
class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer)
    date = Column(Date)
    transactionType = Column(String)
    balance = Column(Float)

    Account = relationship("Account", back_populates="transactions")


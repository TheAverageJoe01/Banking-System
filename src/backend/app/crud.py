from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import models, schemas

# For reference for the passlib:
# https://passlib.readthedocs.io/en/stable/lib/passlib.context.html

passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


# User crud
# --------------------------------------------------------------------------------
def getUser(db: Session, userID: int):
    return db.query(models.User).filter(models.User.id == userID).first()


# Function to get user via userID that is inputted by the user


def getUserByEmail(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# Function to get user via email address


def getUsers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# Function to get the first 100 users


def createUser(
    db: Session, user: schemas.userCreate
):  # if hashed password doesn't work this could be why
    hashedPassword = passwordContext.hash(user.password)
    dbUser = models.User(name=user.name, email=user.email, password=hashedPassword)
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)
    return dbUser


# Function to create a user using the schema userCreate defined in the schemas file


# Account crud
# --------------------------------------------------------------------------------
def getAccounts(db: Session, userID: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Account)
        .filter(models.Account.userID == userID)
        .offset(skip)
        .limit(limit)
        .all()
    )


# Function to get the first 100 accounts stored in the database


def getAccountByType(db: Session, userID: int, accountType: str):
    return (
        db.query(models.Account)
        .filter(models.Account.userID == userID)
        .filter(models.Account.accountType == accountType)
        .all()
    )


# Function to return an account specified via a userID and account type
def createAccount(db: Session, account: schemas.accountCreate, userID: int):
    # Query the database to find the maximum accountNumber for the given user
    max_account_number = db.query(models.Account.accountNumber).filter(models.Account.userID == userID).order_by(models.Account.accountNumber.desc()).first()

    # Increment the maximum accountNumber by 1 or set to 1 if no accounts exist for the user
    next_account_number = (max_account_number[0] + 1) if max_account_number else 1

    # Create the new account
    dbAccount = models.Account(
        balance=account.balance,
        accountType=account.accountType,
        userID=userID,
        accountNumber=next_account_number
    )

    # Add the new account to the session and commit the transaction
    db.add(dbAccount)
    db.commit()
    db.refresh(dbAccount)
    return dbAccount


# Function to create a user by creating an account number using accountCreate in schemas
# Prevents duplicate numbers by increasing the account after every account is created
# Adds the account to the database and refreshes it

def delete_account(db: Session, userID: int, account_number: int):

    account = db.query(models.Account).filter(models.Account.accountNumber == account_number, models.Account.userID == userID).first()
    if account:
        db.delete(account)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Account not found")
# Function deletes account based on current user, given the account number

# Transfer crud
# --------------------------------------------------------------------------------
# Function to deposit funds into a users account, user selects the amount to deposit and the accountID for the
# account, and checks whether the deposit is greater than 0
def depositToAccount(db: Session, userID: int, accountNumber: int, amount: float, isTransfer: bool = False):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    
    # Querying the account
    account = (
        db.query(models.Account)
        .filter(
            models.Account.userID == userID,
            models.Account.accountNumber == accountNumber,
        )
        .first()
    )

    if account:
        # Updating the account balance
        account.balance += amount
        # Creating a transaction object
        transaction = models.Transaction(
            accountID=account.id,
            amount=amount,
            transactionType="Transfer" if isTransfer else "Deposit",
            balance=account.balance,  # Assuming balance after deposit
        )

        # Adding the transaction to the session
        db.add(transaction)

        # Committing the changes
        db.commit()

        # Refreshing the account object to reflect the changes
        db.refresh(account)

        return transaction
    else:
        raise HTTPException(status_code=404, detail="Account not found")


# Function to withdraw funds from an account using the same method as withdraw, except it also checks that
# the account has more than the withdraw amount
def withdrawFromAccount(db: Session, userID: int, accountNumber: int, amount: float, isTransfer: bool = False):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")

    # Querying the account
    account = (
        db.query(models.Account)
        .filter(
            models.Account.userID == userID,
            models.Account.accountNumber == accountNumber,
        )
        .first()
    )

    if account and account.balance >= amount:
        # Updating the account balance
        account.balance -= amount

        # Creating a transaction object
        transaction = models.Transaction(
            accountID=account.id,
            amount=-amount,  # Negative amount for withdrawal
            transactionType="Transfer" if isTransfer else "Withdraw",
            balance=account.balance,  # Assuming balance after withdrawal
        )

        # Adding the transaction to the session
        db.add(transaction)

        # Committing the changes
        db.commit()

        # Refreshing the account object to reflect the changes
        db.refresh(account)

        return transaction
    else:
        raise HTTPException(
            status_code=400,
            detail="Transfer failed due to insufficient funds or invalid account",
        )

from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models,schemas
from passlib.context import CryptContext


# For reference for the passlib:
# https://passlib.readthedocs.io/en/stable/lib/passlib.context.html

passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User crud
# --------------------------------------------------------------------------------
def getUser(db: Session, userID: int):
    return db.query(models.User).filter(models.User.id == userID).first()
#Function to get user via userID that is inputted by the user


def getUserByEmail(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
#Function to get user via email address

def getUsers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
#Function to get the first 100 users

def createUser(db:Session, user: schemas.userCreate): #if hashed password doesn't work this could be why
    hashedPassword = passwordContext.hash(user.password)
    dbUser = models.User(name=user.name,email=user.email,password=hashedPassword)
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)
    return dbUser
#Function to create a user using the schema userCreate defined in the schemas file


# Account crud
# --------------------------------------------------------------------------------
def getAccounts(db: Session, userID: int, skip: int = 0, limit: int = 100):
    return db.query(models.Account).filter(models.Account.userID == userID).offset(skip).limit(limit).all()
#Function to get the first 100 accounts stored in the database

def getAccountByType(db: Session, userID: int, accountType: str):
    return db.query(models.Account).filter(models.Account.userID == userID).filter(models.Account.accountType == accountType).all()
#Function to return an account specified via a userID and account type
def createAccount(db: Session, account: schemas.accountCreate):
    # create a query to find account id 
    
    #last_account = db.query(models.Account).order_by(models.Account.id.desc()).first()
    #if last_account:
        #accountNumber = last_account.accountNumber + 1
    #else:
        #accountNumber = 1

    accountNumber = db.query(models.Account).filter(models.Account.userID==account.userID).count() + 1
    

    dbAccount = models.Account(balance = account.balance, accountType = account.accountType, userID = account.userID, accountNumber = accountNumber)
    db.add(dbAccount)
    db.commit()
    db.refresh(dbAccount)
    return dbAccount
#Function to create a user by creating an account number using accountCreate in schemas
#Prevents duplicate numbers by increasing the account after every account is created
#Adds the account to the database and refreshes it


# Transfer crud
# --------------------------------------------------------------------------------
def depositToAccount(db: Session, userID: int, accountNumber: int, amount: float):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    account = db.query(models.Account).filter(
        models.Account.userID == userID, 
        models.Account.accountNumber == accountNumber
    ).first()
    if account:
        account.balance += amount
        db.commit()
        db.refresh(account)
        return account
    else:
        raise HTTPException(status_code=404, detail="Account not found")
#Function to deposit funds into a users account, user selects the amount to deposit and the accountID for the
#account, and checks whether the deposit is greater than 0

def withdrawFromAccount(db: Session, userID: int, accountNumber: int, amount: float):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    account = db.query(models.Account).filter(
        models.Account.userID == userID, 
        models.Account.accountNumber == accountNumber
    ).first()
    if account and account.balance >= amount:
        account.balance -= amount
        db.commit()
        db.refresh(account)
        return account
    else:
        raise HTTPException(status_code=400, detail="Transfer failed due to insufficient funds or invalid account")
#Function to withdraw funds from an account using the same method as withdraw, except it also checks that
#the account has more than the withdraw amount
     
def transferFromAccount(db: Session, accountID: int, amount: float):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    account = db.query(models.Account).filter(models.Account.id == accountID).first()
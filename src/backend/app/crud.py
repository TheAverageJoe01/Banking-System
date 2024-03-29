from sqlalchemy.orm import Session
from fastapi import HTTPException
from . import models,schemas

# User crud
# --------------------------------------------------------------------------------
def getUser(db: Session, userID: int):
    return db.query(models.User).filter(models.User.id == userID).first()


def getUserByEmail(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def getUsers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def createUser(db:Session, user: schemas.userCreate):
    dbUser = models.User(name=user.name,email=user.email,password=user.password)
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)
    return dbUser


# Account crud
# --------------------------------------------------------------------------------
def getAccounts(db: Session, userID: int, skip: int = 0, limit: int = 100):
    return db.query(models.Account).filter(models.Account.userID == userID).offset(skip).limit(limit).all()

def getAccountByType(db: Session, userID: int, accountType: str):
    return db.query(models.Account).filter(models.Account.userID == userID).filter(models.Account.accountType == accountType).all()

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

# Transfer crud
# --------------------------------------------------------------------------------
def depositToAccount(db: Session, accountID: int, amount: float):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    account = db.query(models.Account).filter(models.Account.id == accountID).first()
    if account:
        account.balance += amount
        db.commit()
        db.refresh(account)
        return account
    else:
        raise HTTPException(status_code=404, detail="Account not found")

def withdrawFromAccount(db: Session, accountID: int, amount: float):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    account = db.query(models.Account).filter(models.Account.id == accountID).first()
    if account and account.balance >= amount:
        account.balance -= amount
        db.commit()
        db.refresh(account)
        return account
    else:
        raise HTTPException(status_code=400, detail="Transfer failed due to insufficient funds or invalid account")
    
def transferFromAccount(db: Session, accountID: int, amount: float):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than 0")
    account = db.query(models.Account).filter(models.Account.id == accountID).first()
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


from app import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

#Dependencies
def getDB():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()


# User
# --------------------------------------------------------------------------------------
@app.post("/users/", responseModel=schemas.User, status_code=201)
#Endpoint to receive input data
def createUser(user: schemas.UserCreate, db: Session = Depends(getDB)):
    dbUser = crud.getUserByEmail(db, email=user.email)
    if dbUser:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.createUser(db=db, user=user)



@app.get("/users/", responseModel=list[schemas.User])
def readUsers(skip: int=0, limit: int=100, db: Session = Depends(getDB)):
    users = crud.getUsers(db, skip=skip, limit=limit)
    return users #could be this?

@app.get("/users/{userID}", responseModel=schemas.User)
def readUser(userID: int, db: Session = Depends(getDB)):
    dbUser = crud.getUser(db,userID=userID)
    if dbUser is None:
        raise HTTPException(status_code=404, detail = "User not found")
    return dbUser

@app.put("/users/{userID}", responseModel=schemas.User)
def editUser(userID: int, updateUser: schemas.userUpdate, db: Session = Depends(getDB)):
    # Retrieve the existing user from the database
    dbUser = crud.getUser(db, userID=userID)
    if dbUser is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update model instance with the data from userUpdate schema
    userData = updateUser.dict(exclude_unset=True)
    for key, value in userData.items():
        setattr(dbUser, key, value)

    db.commit()
    db.refresh(dbUser)

    return dbUser

@app.delete("/users/{userID}")
def deleteUser(userID: int, db: Session = Depends(getDB)):

    dbUser = crud.getUser(db, userID=userID)
    if dbUser is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    db.delete(dbUser)
    db.commit()
    return {"ok": True}

# Account
# --------------------------------------------------------------------------------------
@app.post("/accounts/{userID}", responseModel=schemas.Account, status_code=201)
#Endpoint to receive input data
def createAccount(account: schemas.accountCreate, db: Session = Depends(getDB)):
    dbAccount = crud.getAccountByType(db, userID=account.userID, accountType=account.accountType)
    if dbAccount:
        raise HTTPException(status_code=400, detail="Account with this type and user already exists")
    return crud.createAccount(db=db, account=account)

@app.get("/accounts/{userID}", responseModel=list[schemas.Account])
def readAccountsByUserID(skip: int=0, limit: int=100, db: Session = Depends(getDB)):
    accounts = crud.getAccounts(db, skip=skip, limit=limit)
    return accounts

@app.get("/accounts/{userID}/{accountType}", responseModel=list[schemas.Account])
def readAccountByType(accountType: str, db: Session = Depends(getDB)):
    dbAccount = crud.getAccountByType(db, accountType==accountType)
    if dbAccount is None:
        raise HTTPException(status_code=404, detail = "User not found")
    return dbAccount


# DEPOSIT/WITHDRAW
# --------------------------------------------------------------------------------------
@app.post("/accounts/{accountID}/deposit/", responseModel=list[schemas.Account])
def deposit(accountID: int, amount: float, db: Session = Depends(getDB)):
    account_deposit = crud.depositToAccount(db, balance=amount)
    if account_deposit is None:
        raise HTTPException(status_code = 404, detail = "User not found")
    return account_deposit
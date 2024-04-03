from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from passlib.context import CryptContext
passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


from app import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Dependencies
def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User
# --------------------------------------------------------------------------------------
@app.post("/users/", response_model=schemas.User, status_code=201)
#Endpoint to receive input data
def createUser(user: schemas.userCreate, db: Session = Depends(getDB)):
    dbUser = crud.getUserByEmail(db, email = user.email)
    if dbUser:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.createUser(db=db, user=user)
#Uses the getuserbyemail function to check if the email is already used with an account, if not uses the createUser
#function to create a new user


@app.get("/users/", response_model=list[schemas.User])
def readUsers(skip: int=0, limit: int=100, db: Session = Depends(getDB)):
    users = crud.getUsers(db, skip=skip, limit=limit)
    return users 
#Uses the user schema and the readusers function to get up to the first 100 users from the database

@app.get("/users/{userID}", response_model=schemas.User)
def readUser(userID: int, db: Session = Depends(getDB)):
    dbUser = crud.getUser(db,userID=userID)
    if dbUser is None:
        raise HTTPException(status_code=404, detail = "User not found")
    return dbUser
#Uses the getUser function from crud to get a user specified by a unique userID, if not found displays an error

@app.put("/users/{userID}", response_model=schemas.User)
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
#Gets the user specified, and then deletes the user from the database, if no user found, displays error

# Login 
# --------------------------------------------------------------------------------------

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(getDB)):
    # Attempt to retrieve the user by username/email
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    
    # Verify the provided password against the stored hash
    if not passwordContext.verify(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    
    return {"access_token": user.email, "token_type": "bearer"}
#A login function to allow users to login to their account. Creates a form where the user inputs their email and password
#and then compares the email in the form to the database and see if there are any matches, if there is, then hashes
#the password inputted by the user in the form, and compares that hashed password to the one in the account when the user
#created the account


# Account
# --------------------------------------------------------------------------------------
@app.post("/accounts/{userID}", response_model=schemas.Account, status_code=201)
#Endpoint to receive input data
def createAccount(account: schemas.accountCreate, db: Session = Depends(getDB)):
    # dbAccount = crud.getAccountByType(db, userID=account.userID, accountType=account.accountType)
    #if dbAccount:
        #raise HTTPException(status_code=400, detail="Account with this type and user already exists")
    return crud.createAccount(db=db, account=account)
#Creates account by using the account schema to structure the data, uses the createAccount function to set the
#variables to a value

@app.get("/accounts/{userID}", response_model=list[schemas.Account])
def readAccountsByUserID(userID: int, skip: int=0, limit: int=100, db: Session = Depends(getDB)):
    accounts = crud.getAccounts(db, userID, skip=skip, limit=limit)
    return accounts
#Gets a specific account from the database using the UserID specified by the user using the getAccounts function

@app.get("/accounts/{userID}/{accountType}", response_model=list[schemas.Account])
def readAccountByType(accountType: str, userID, db: Session = Depends(getDB)):
    dbAccount = crud.getAccountByType(db, userID, accountType)
    if dbAccount is None:
        raise HTTPException(status_code=404, detail = "User not found")
    return dbAccount
#Gets a specific account type from the database by a specified userID and accountType, if no account is found
#displays an error message


# DEPOSIT/WITHDRAW
# --------------------------------------------------------------------------------------
@app.post("/accounts/{userID}/deposit/{accountNumber}", response_model=schemas.Account)
def deposit(userID: int, accountNumber: int, amount: float, db: Session = Depends(getDB)):
    account_deposit = crud.depositToAccount(db, userID = userID, accountNumber = accountNumber, amount=amount)
    if account_deposit is None:
        raise HTTPException(status_code = 404, detail = "User or Account not found")
    return account_deposit

@app.post("/accounts/{userID}/withdraw/{accountNumber}", response_model=schemas.Account)
def withdraw(userID: int, accountNumber: int, amount: float, db: Session = Depends(getDB)):
    account_withdraw = crud.withdrawFromAccount(db, userID = userID, accountNumber = accountNumber, amount=amount)
    if account_withdraw is None:
        raise HTTPException(status_code = 404, detail = "User or Account not found")
    return account_withdraw
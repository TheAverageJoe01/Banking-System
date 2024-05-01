from typing import Annotated
from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from passlib.context import CryptContext

passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


from app import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)



SECRET_KEY = "test"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


app = FastAPI()

# Dependencies
def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
token: Annotated[str, Depends(oauth2_scheme)]


def authenticateUser(username: str, password: str, db: Session = Depends(getDB)):
    user = db.query(models.User).filter(models.User.email == username).first()

    if not user:
        return False 
    if not passwordContext.verify(password, user.password):
        return False
    return user


def createToken(data: dict, expires_delta: timedelta | None = None):
    toEncode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    toEncode.Update({"exp": expire})
    encodedJWT = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJWT

def getCurrentUser(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id: int = payload.get("id")
        if username is None or id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return {"username": username, "id": id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")




userDependency = Annotated[dict, Depends(getCurrentUser)]

# User
# --------------------------------------------------------------------------------------
@app.post("/users/", response_model=schemas.User, status_code=201, tags=["Users"])
#Endpoint to receive input data
def createUser(user: schemas.userCreate, db: Session = Depends(getDB)):
    dbUser = crud.getUserByEmail(db, email = user.email)
    if dbUser:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.createUser(db=db, user=user)
#Uses the getuserbyemail function to check if the email is already used with an account, if not uses the createUser
#function to create a new user


@app.get("/users/", response_model=list[schemas.User], tags=["Users"])
def readUsers(skip: int=0, limit: int=100, db: Session = Depends(getDB)):
    users = crud.getUsers(db, skip=skip, limit=limit)
    return users 
#Uses the user schema and the readusers function to get up to the first 100 users from the database

@app.get("/users/", response_model=schemas.User, tags=["Users"])
def readUser(userID: userDependency, db: Session = Depends(getDB)):
    dbUser = crud.getUser(db, userID)
    if dbUser is None:
        raise HTTPException(status_code=404, detail = "User not found")
    return dbUser
#Uses the getUser function from crud to get a user specified by a unique userID, if not found displays an error

@app.put("/users/", response_model=schemas.User, tags=["Users"])
def editUser(userID: userDependency , updateUser: schemas.userUpdate, db: Session = Depends(getDB)):
    # Retrieve the existing user from the database
    dbUser = crud.getUser(db, userID)
    if dbUser is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update model instance with the data from userUpdate schema
    userData = updateUser.dict(exclude_unset=True)
    for key, value in userData.items():
        setattr(dbUser, key, value)

    db.commit()
    db.refresh(dbUser)

    return dbUser

@app.delete("/users/", tags=["Users"])
def deleteUser(userID: userDependency, db: Session = Depends(getDB)):

    dbUser = crud.getUser(db, userID)
    if dbUser is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    db.delete(dbUser)
    db.commit()
    return {"ok": True}
#Gets the user specified, and then deletes the user from the database, if no user found, displays error

# Login 
# --------------------------------------------------------------------------------------

@app.post("/token", tags=["Login"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(getDB)):
    # Attempt to retrieve the user by username/email
    user = authenticateUser(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    token = createToken(user.username, user.id, timedelta(minutes=30))
    
    return {"access_token": token, "token_type": "bearer"}
#A login function to allow users to login to their account. Creates a form where the user inputs their email and password
#and then compares the email in the form to the database and see if there are any matches, if there is, then hashes
#the password inputted by the user in the form, and compares that hashed password to the one in the account when the user
#created the account


# Account
# --------------------------------------------------------------------------------------
@app.post("/accounts/{userID}", response_model=schemas.Account, status_code=201, tags=["Accounts"])
#Endpoint to receive input data
def createAccount(account: schemas.accountCreate, db: Session = Depends(getDB)):
    # dbAccount = crud.getAccountByType(db, userID=account.userID, accountType=account.accountType)
    #if dbAccount:
        #raise HTTPException(status_code=400, detail="Account with this type and user already exists")
    return crud.createAccount(db=db, account=account)
#Creates account by using the account schema to structure the data, uses the createAccount function to set the
#variables to a value

@app.get("/accounts/{userID}", response_model=list[schemas.Account], tags=["Accounts"])
def readAccountsByUserID(userID: int, skip: int=0, limit: int=100, db: Session = Depends(getDB)):
    accounts = crud.getAccounts(db, userID, skip=skip, limit=limit)
    return accounts
#Gets a specific account from the database using the UserID specified by the user using the getAccounts function

@app.get("/accounts/{userID}/{accountType}", response_model=list[schemas.Account], tags=["Accounts"])
def readAccountByType(accountType: str, userID, db: Session = Depends(getDB)):
    dbAccount = crud.getAccountByType(db, userID, accountType)
    if dbAccount is None:
        raise HTTPException(status_code=404, detail = "User not found")
    return dbAccount
#Gets a specific account type from the database by a specified userID and accountType, if no account is found
#displays an error message


# DEPOSIT/WITHDRAW
# --------------------------------------------------------------------------------------
@app.post("/accounts/{userID}/deposit/{accountNumber}", response_model=schemas.Receipt, tags=["Transactions"])
def deposit(userID: int, accountNumber: int, amount: float, db: Session = Depends(getDB)):
    account_deposit = crud.depositToAccount(db, userID = userID, accountNumber = accountNumber, amount=amount)
    if account_deposit is None:
        raise HTTPException(status_code = 404, detail = "User or Account not found")
    return {"amount": amount, "time": account_deposit.date}

@app.post("/accounts/{userID}/withdraw/{accountNumber}", response_model=schemas.Receipt, tags=["Transactions"])
def withdraw(userID: int, accountNumber: int, amount: float, db: Session = Depends(getDB)):
    account_withdraw = crud.withdrawFromAccount(db, userID = userID, accountNumber = accountNumber, amount=amount)
    if account_withdraw is None:
        raise HTTPException(status_code = 404, detail = "User or Account not found")
    return {"amount": amount, "time": account_withdraw.date}

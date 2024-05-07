from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware

from typing import Optional, List

passwordContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


from app import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

SECRET_KEY = "test"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Frontend communication - Cross-origin resource sharing (CORS)
origins = ["http://localhost:3000"]  

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencies
def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# token: Annotated[str, Depends(oauth2_scheme)]


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
    toEncode.update({"exp": expire})
    encodedJWT = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encodedJWT
    
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username, id = payload.get("sub"), payload.get("id")
        if username is None:
            raise HTTPException(status_code=403, detail="Token is invalid or expired")
        return username, id
    except JWTError:
        raise HTTPException(status_code=403, detail="Token is invalid or expired")
    
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
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )

userDependency = Annotated[dict, Depends(getCurrentUser)]


# User
# --------------------------------------------------------------------------------------
@app.post("/users/", response_model=schemas.User, status_code=201, tags=["Users"])
# Endpoint to receive input data
def createUser(user: schemas.userCreate, db: Session = Depends(getDB)):
    dbUser = crud.getUserByEmail(db, email=user.email)
    if dbUser:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.createUser(db=db, user=user)


# Uses the getuserbyemail function to check if the email is already used with an account, if not uses the createUser
# function to create a new user


# Uses the user schema and the readusers function to get up to the first 100 users from the database


@app.get("/users/", response_model=schemas.User, tags=["Users"], status_code=200)
def readUser(user: userDependency, db: Session = Depends(getDB)):
    dbUser = crud.getUser(db, user["id"])
    if dbUser is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dbUser


# Uses the getUser function from crud to get a user specified by a unique userID, if not found displays an error


@app.put("/users/", response_model=schemas.userEdited, tags=["Users"], status_code=200)
def editEmail(
    user: userDependency, updateUser: schemas.userUpdate, db: Session = Depends(getDB)
):
    # Retrieve the existing user from the database
    dbUser = crud.getUser(db, user["id"])
    if dbUser is None:
        raise HTTPException(status_code=404, detail="User not found")

    newEmail = updateUser.email
    if db.query(models.User).filter(models.User.email == newEmail).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    dbUser.email = updateUser.email

    db.commit()
    db.refresh(dbUser)
    accessToken = createToken(
        {"sub": updateUser.email, "id": user["id"]}, timedelta(minutes=30)
    )
    refreshToken = createToken(
        {"sub": updateUser.email, "id": user["id"], "refresh": True},
        timedelta(days=7),
    )
    return {"user": updateUser, "accessToken": accessToken, "refreshToken": refreshToken}


@app.delete("/users/", status_code=200, tags=["Users"])
def deleteUser(user: userDependency, response_model=schemas.userDelete, db: Session = Depends(getDB)):

    dbUser = crud.getUser(db, user["id"])
    if dbUser is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # delete the accounts associated with the user
    accounts = crud.getAccounts(db, user["id"])
    for account in accounts:
        db.delete(account)

    db.delete(dbUser)
    db.commit()
    return {"message": "User successfully deleted"}


# Gets the user specified, and then deletes the user from the database, if no user found, displays error

# Login
# --------------------------------------------------------------------------------------


@app.post("/token/", tags=["Login"])
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], status_code=200,
    db: Session = Depends(getDB),
):
    # Attempt to retrieve the user by username/email
    user = authenticateUser(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    token = createToken({"sub": user.email, "id": user.id}, timedelta(minutes=30))

    return {"access_token": token, "token_type": "bearer"}

@app.get("/verify-token/{token}")
async def verify_user_token(token: str):
    username, id = verify_token(token=token)
    return {"message": "Token is valid", "username": username, "id": id}
#A login function to allow users to login to their account. Creates a form where the user inputs their email and password
#and then compares the email in the form to the database and see if there are any matches, if there is, then hashes
#the password inputted by the user in the form, and compares that hashed password to the one in the account when the user
#created the account


# Account
# --------------------------------------------------------------------------------------
@app.post(
    "/accounts/", response_model=schemas.Account, status_code=201, tags=["Accounts"]
)
# Endpoint to receive input data
def createAccount(
    user: userDependency, account: schemas.accountCreate, db: Session = Depends(getDB)
):
    # dbAccount = crud.getAccountByType(db, userID=account.userID, accountType=account.accountType)
    # if dbAccount:
    # raise HTTPException(status_code=400, detail="Account with this type and user already exists")
    return crud.createAccount(db=db, account=account, userID=user["id"])


# Creates account by using the account schema to structure the data, uses the createAccount function to set the
# variables to a value


@app.get("/accounts/", response_model=list[schemas.Account], status_code=200, tags=["Accounts"])
def readAccountsByUserID(
    userID: userDependency,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(getDB),
):
    accounts = crud.getAccounts(db=db, userID=userID["id"], skip=skip, limit=limit)
    return accounts
#Gets all accounts from the database using the UserID specified by the user using the getAccounts function


# Gets a specific account from the database using the UserID specified by the user using the getAccounts function


@app.get(
    "/accounts/{accountType}", response_model=list[schemas.Account], status_code=200, tags=["Accounts"]
)
def readAccountByType(
    accountType: str, userID: userDependency, db: Session = Depends(getDB)
):
    dbAccount = crud.getAccountByType(
        db=db, userID=userID["id"], accountType=accountType
    )
    if dbAccount is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dbAccount


# Gets a specific account type from the database by a specified userID and accountType, if no account is found
# displays an error message

@app.delete("/accounts/{account_number}", tags=["Accounts"])
def delete_account(account_number: int, userID: userDependency, db: Session = Depends(getDB)):

    crud.delete_account(db=db, userID=userID['id'], account_number=account_number)
    return {"message": "Account deleted successfully"}


# DEPOSIT/WITHDRAW
# --------------------------------------------------------------------------------------
@app.post(
    "/accounts/deposit/{accountNumber}",
    response_model=schemas.Receipt,
    status_code=200,
    tags=["Transactions"],
)
def deposit(
    user: userDependency,
    accountNumber: int,
    amount: float,
    db: Session = Depends(getDB),
):
    account_deposit = crud.depositToAccount(
        db, userID=user["id"], accountNumber=accountNumber, amount=amount
    )
    if account_deposit is None:
        raise HTTPException(status_code=404, detail="User or Account not found")
    
    return {"amount": amount, "time": account_deposit.date, "type": "Deposit"}


@app.post(
    "/accounts/withdraw/{accountNumber}",
    response_model=schemas.Receipt,
    status_code=200,
    tags=["Transactions"],
)
def withdraw(
    user: userDependency,
    accountNumber: int,
    amount: float,
    db: Session = Depends(getDB),
):
    account_withdraw = crud.withdrawFromAccount(
        db, userID=user["id"], accountNumber=accountNumber, amount=amount
    )
    if account_withdraw is None:
        raise HTTPException(status_code=404, detail="User or Account not found")
    
    return {"amount": amount, "time": account_withdraw.date, "type": "Withdraw"}


@app.post(
    "/accounts/transfer/{account1}/{account2}",
    response_model=schemas.Receipt,
    status_code=200,
    tags=["Transactions"],
)
def transfer(
    user: userDependency,
    account1: int,
    account2: int,
    amount: float,
    db: Session = Depends(getDB),
):
    try:
        account_withdraw = crud.withdrawFromAccount(
            db, userID=user["id"], accountNumber=account1, amount=amount, isTransfer=True
        )
        if account_withdraw is None:
            raise HTTPException(status_code=404, detail="User or Account not found")

        account_deposit = crud.depositToAccount(
            db, userID=user["id"], accountNumber=account2, amount=amount, isTransfer=True
        )
        if account_deposit is None:
            # If deposit fails, roll back the withdrawal
            crud.depositToAccount(
                db, userID=user["id"], accountNumber=account1, amount=amount, isTransfer=True
            )  # Rollback
            raise HTTPException(status_code=404, detail="User or Account not found")

        return {
            "amount": amount,
            "time": account_withdraw.date,
            "type": "Transfer"
        }
    except Exception as e:
        # Handle other exceptions such as database errors
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

# Transactions

# Function to convert Transaction objects to Receipt objects
def transaction_to_receipt(transaction: models.Transaction) -> schemas.Receipt:
    return schemas.Receipt(
        amount=transaction.amount,
        time=transaction.date,
        type=transaction.transactionType
    )

@app.get("/transactions/{account_number}", response_model=List[schemas.Receipt], tags=["Transactions"])
def get_transactions(
    account_number: int,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    transaction_type: Optional[str] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    db: Session = Depends(getDB)
):
    # Construct base query to filter transactions by account number
    query = db.query(models.Transaction).join(models.Account).filter(models.Account.accountNumber == account_number)

    # Apply additional filters if provided
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)
    if transaction_type:
        query = query.filter(models.Transaction.transactionType == transaction_type)
    if min_amount:
        query = query.filter(models.Transaction.amount >= min_amount)
    if max_amount:
        query = query.filter(models.Transaction.amount <= max_amount)

    # Execute the query, convert transactions to receipts, and return the results
    transactions = query.all()
    receipts = [transaction_to_receipt(transaction) for transaction in transactions]
    return receipts
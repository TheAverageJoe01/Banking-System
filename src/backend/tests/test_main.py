from fastapi import responses
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from main import app, getDB

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def overrideGetDB():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[getDB] = overrideGetDB

client = TestClient(app)

login_token = None

def test_create_user():
    global testUserData

    testUserData = json={
        "name": "Test User",
        "email": "testUser@email,com",
        "password": "testPassword"
    }

    response = client.post("/users/", json=testUserData)

    assert response.status_code == 200

    assert response.json()["message"] == "User created successfully"

def test_duplicate_email():

    userData = json={
        "name": "dublicate User",
        "email": "testUser@email,com",
        "password": "testPassword"
    }
    response = client.post("/users/", json=userData)

    assert response.status_code == 422

    assert response.json()["detail"] == "Email already registered"

def test_login_user():
    global login_token

    userData = json={
        "username": testUserData["email"],
        "password": testUserData["password"]
    }

    response = client.post("/token/", json=userData)

    assert response.status_code == 200

    assert response.json()["message"] == "Login successful"

    login_token = response.json()["access_token"]


def test_bad_login():
    userData = json={
        "username": "badEmail",
        "password": "badPassword"
    }

    response = client.post("/token/", json=userData)

    assert response.status_code == 401

    assert response.json()["detail"] == "Incorrect email or password"

def test_read_users():
    response = client.get("/users/", headers={"Authorization": f"Bearer {login_token}"})

    assert response.status_code == 200

    assert response.json()[0]["name"] == "Test User"

def test_bad_read_users():
    response = client.get("/users/", headers={"Authorization": f"Bearer badToken"})

    assert response.status_code == 401

    assert response.json()["detail"] == "Could not validate credentials"

def test_read_user_by_userID():
    response = client.get("/users/", headers={"Authorization": f"Bearer {login_token}"})

    assert response.status_code == 200

    assert response.json()["name"] == "Test User"
    
def test_bad_read_user_by_userID():
    response = client.get("/users/", headers={"Authorization ": f"Bearer badToken"})

    assert response.status_code == 401

    assert response.json()["detail"] == "userID not found"





def test_create_account():
    global testAccountData
    testAccountData = {
        "accountType": "Savings",
        "balance": 1000.0
    }
    response = client.post("/accounts/", json=testAccountData, headers={"Authorization": f"Bearer {login_token}"})
    assert response.status_code == 201
    assert response.json()["accountType"] == "Savings"
    assert response.json()["balance"] == 1000.0

def test_read_accounts_by_user_id():
    response = client.get("/accounts/", headers={"Authorization": f"Bearer {login_token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_read_account_by_type():
    response = client.get("/accounts/Savings", headers={"Authorization": f"Bearer {login_token}"})
    assert response.status_code == 200
    assert response.json()[0]["accountType"] == "Savings"

def test_deposit():
    account_number = 1  # Replace with the actual account number
    amount = 500.0
    response = client.post(f"/accounts/deposit/{account_number}", json={"amount": amount}, headers={"Authorization": f"Bearer {login_token}"})
    assert response.status_code == 200
    assert response.json()["amount"] == amount
    assert response.json()["transactionType"] == "Deposit"

def test_withdraw():
    account_number = 1  # Replace with the actual account number
    amount = 200.0
    response = client.post(f"/accounts/withdraw/{account_number}", json={"amount": amount}, headers={"Authorization": f"Bearer {login_token}"})
    assert response.status_code == 200
    assert response.json()["amount"] == amount
    assert response.json()["transactionType"] == "Withdraw"

def test_transfer():
    account1 = 1  # Replace with the actual account number
    account2 = 2  # Replace with the actual account number
    amount = 300.0
    response = client.post(f"/accounts/transfer/{account1}/{account2}", json={"amount": amount}, headers={"Authorization": f"Bearer {login_token}"})
    assert response.status_code == 200
    assert response.json()["amount"] == amount
    assert response.json()["transactionType"] == "Transfer"
    

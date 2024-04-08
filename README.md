# User and Account Banking System

This system provides a RESTful API for managing users and their accounts built with Python using FastAPI, SQLAlchemy, and OAuth2 for authentication.

# Features

-User Management: Create, read, update, search and delete users.

-Authentication: Secure login system using OAuth2 and bcrypt with password hashing for user authentication.

-Account Management: Create, read, and search user accounts by type.

-Deposit/Withdraw: Perform deposits into user accounts and withdrawals from user accounts.

# Installation

1.Clone the repository:
git clone https://github.com/TheAverageJoe01/Banking-System.git

2.Install dependencies:
pip install -r requirements.txt

3.Set up the database:
python app/database.py

4.Run the FastAPI server:
uvicorn app.main:app --reload

# Usage

Once the server is running, you can access the API documentation at http://localhost:8000/docs to interact with the endpoints using Swagger UI.

## Countdown 
// add count down here 

# User and Account Banking System

This system provides a RESTful API for managing users and their accounts built with Python using FastAPI, SQLAlchemy, and OAuth2 for authentication.

## Features

- User Management: Create, read, update, search and delete users.

- Authentication: Secure login system using OAuth2 and bcrypt with password hashing for user authentication.

- Account Management: Create, read, and search user accounts by type.

- Deposit/Withdraw: Perform deposits into user accounts and withdrawals from user accounts.

## Installation

1. Clone the repository
```bash
git clone git@github.com:TheAverageJoe01/Banking-System.git
```

2. Build Docker stack
```bash
docker compose up --build
```

## Usage

Once the server is running, you can access the API at the following endpoints:

- React App: (http://localhost:[TBD])
- SwaggerUI Documentation: (http://localhost:8000/docs)
- Redoc Documentation: (http://localhost:8000/redoc)


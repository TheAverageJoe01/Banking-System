from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# setting up the database
database = 'sqlite:///./bank.db'
engine = create_engine(
    database, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Initalises the database to store customer information and data

Base = declarative_base()


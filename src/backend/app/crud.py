from sqlalchemy.orm import Session

from . import models,schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db:Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_details(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Details).offset(skip).limit(limit).all()

def create_user_details(db:Session, details: schemas.DetailCreate, user_id: int):
    db_detail = models.Details(**details.dict(), user_id=user_id)
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail

#Account crud
def get_account_by_id(db:Session, id: int):
    return db.query(models.Account).filter(models.Account.id == id).first()



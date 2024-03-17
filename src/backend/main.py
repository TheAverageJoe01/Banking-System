from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


from app import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

#Dependencies
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User, status_code=201)
#Endpoint to receive input data
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)



@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users #could be this?

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db,user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail = "User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def edit_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    # Retrieve the existing user from the database
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update model instance with the data from UserUpdate schema
    user_data = user_update.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

        db_user = crud.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        db.delete(db_user)
        db.commit()
        return {"ok": True}

@app.post("/users/{user_id}/details/", response_model=schemas.Detail, status_code=201)
def create_user_details(
    user_id: int, details: schemas.DetailCreate, db: Session = Depends(get_db)):
    return crud.create_user_details(db=db, details=details, user_id=user_id)

@app.get("/details/", response_model=list[schemas.Detail])
def read_details(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    details = crud.get_details(db, skip=skip, limit=limit)
    return details
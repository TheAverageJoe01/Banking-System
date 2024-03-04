from fastapi import FastAPI
#from . import crud, models, schemas
#from code.database import SessionLocal, engine
#models.Base.metadata.create_all(bind=engine)
#Dependencies
#def get_db():
    #db= SessionLocal()
    #try:
        #yield db
    #finally
        #db.close()



app = FastAPI()


@app.post("/users/")
#Endpoint to receive input data
async def create_user(user: UserBase):
    #return {"User_name": user.name, "Email_name": email.name}
    return {"User:": user}



@app.get("/")
async def root():
    return {"message": "Hello lmao!"}
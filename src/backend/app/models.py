from sqlalchemy import Boolean, Column, Integer, String, Date
#from sqlalchemy.orm import relationship


from app.database import Base



# Create a class that will be used to create the table in the database
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)




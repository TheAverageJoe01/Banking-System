from sqlalchemy import Boolean, Column, Integer, String, Date
#from sqlalchemy import relationship

from typing import Optional

from .database import Base



# Create a class that will be used to create the table in the database
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    #name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    #postCode = Column(String)
    # DoB = Column(Date)




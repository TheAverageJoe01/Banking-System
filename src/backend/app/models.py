from sqlalchemy import Boolean, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


from app.database import Base



# Create a class that will be used to create the table in the database
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    details = relationship("Details", back_populates="user")

# Create a class that will be used to create a table to store user details and balance 
class Details(Base):
    __tablename__ = 'details'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    #date_of_birth = Column(Date)
    balance = Column(Integer)

    user = relationship("User", back_populates="details")

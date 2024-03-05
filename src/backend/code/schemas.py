from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    #name: str 
    #postCode: str
    #DoB: Optional[Date] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    #name: str
    #postCode: str
    #DoB: Optional[Date] = None

    class Config:
        from_attributes = True
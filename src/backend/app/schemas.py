from typing import Optional
from pydantic import BaseModel


class DetailBase(BaseModel):
    balance: int

class DetailCreate(DetailBase):
    pass

class Detail(DetailBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

class Post_model(BaseModel):
    title : str
    content : str
    published : bool = True


class PostCreate(Post_model):
    pass

class Post(Post_model):
    created_at: datetime

    class Config:
        from_attributes = True

class User_Create(BaseModel):
    
    email : EmailStr
    password : str

class ResponseUser(BaseModel):
    
    email : EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    acces_token : str
    token_type : str
    
class TokenData(BaseModel):
    id: Optional[int] = None
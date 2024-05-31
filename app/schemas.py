from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

class PostBase(BaseModel):
    title : str
    content : str
    published: bool = True# it will give by default true if we dont write any thing in body in postman
    #rating: Optional[int]=None  # optional field if user dont provide it will give value as zero

class PostCreate(PostBase):
    pass 
# it will inherit all the properties of PostBase  


class UserOut(BaseModel):
    id:int
    email:EmailStr
    # heere we made response bcoz we dont want our password to be shown after we enter, in the output    
    created_at:datetime

    class Config:
        orm_mode =True

class Post(PostBase): # this is for response we can only send what we want in o/pby default will 
    # wala should be mentioned
    
    id: int
    created_at:datetime
    owner_id:int
    owner:UserOut
    
    class Config:
        orm_mode =True
# the advtg of this response is we can onlyb send id which we want 
class PostOut(BaseModel):
    Post:Post
    votes:int
    class Config:
        orm_mode =True

class UserCreate(BaseModel):
    email : EmailStr 
    password: str




class UserLogin(BaseModel):
    email:EmailStr
    password:str   

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None

class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)    


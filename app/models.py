# Here we will write all the python codes for creating tableas etc etc 

from sqlalchemy import Column,Integer,Boolean,String,ForeignKey
from sqlalchemy.sql.expression import null,text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship

class Post(Base): # base bcoz we are using sqlalchemy
    __tablename__= "posts" # here we define the tablename

    id= Column(Integer,primary_key=True,nullable=False) # here all the coloumn name and its datatype
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(String,server_default='True',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    # ondelete = cascade is for if we delete a post of id 16 it should delete all posts of id not only one

    owner = relationship("User")    


class User(Base):
    __tablename__ = "users"

    id= Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    phone_number=Column(String)

class Vote(Base):
  __tablename__ = "votes"
  user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
  post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True )
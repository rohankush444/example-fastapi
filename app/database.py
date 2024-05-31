# sqlalchemy is used to connect to database we use this bcoxz in this we can write python code to create tables
# no need of sql queries #Following are the steps for connecting it to database

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . config import settings

SQLALCHEMY_DATABASE_URL= f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
#this is same as username password host in sql in sql alchemy we write like this

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
# it is used to connect to database

Base=declarative_base()

def get_db():
    db=SessionLocal() # this will try to talk to database 
    try:
        yield db
    finally:
        db.close()    
#this all need to be just pasted one time


"""
while True:

    try: 

        conn = psycopg2.connect(host = 'localhost' ,database= 'fastapi' , user= 'postgres' ,
        password= 'Rohan1234' , cursor_factory=RealDictCursor) 
# this cursor factory used to give nos to coloumns
        cursor=conn.cursor() 
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database is failed")
        print("Error",error)  
        time.sleep(2) # if connection failed every 2 second me try hoga
"""
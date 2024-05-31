from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from random import randrange # it is used to create an id by giving the range by our side
from . import models
from.database import engine
from .routers import user,post,auth,vote
from .config import settings

print(settings.database_username)
#models.Base.metadata.create_all(bind=engine)
#this all need to be just pasted one time

app= FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# this cors is used to run it to the any web server
# upwards origin =* means all web servers 

app.include_router(post.router) # this is bcoz from here we can user user.py and post.py
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
@app.get("/")
async def root():
    return {"message" : "Hello Rohan"}



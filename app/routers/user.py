from fastapi import FastAPI,Response,HTTPException,status,Depends,APIRouter
from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session

router=APIRouter(
     prefix="/users",
     tags=['users']
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user :schemas.UserCreate, db:Session=Depends(get_db)):

    # hash the password -user.password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.dict())

    db.add(new_user) # this will add the new post to database
    db.commit() # this will show the newly added post on databse
    db.refresh(new_user) # this will print the data on database
    
    return new_user


# to retrieve user

@router.get('/{id}',response_model=schemas.UserOut) # we used userout bcoz we dont want password to display
def get_user(id : int, db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} doesnt exist")
    return user

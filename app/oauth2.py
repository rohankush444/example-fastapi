from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas,models,database
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl='/login')


# SECRET _KEY
# Algorithm
# Expiration time

SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=settings.access_token_expire_minutes

def create_access_token(data:dict):
    to_encode=data.copy() # all the data will be copied

    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
    # it will shopw thhe expiry time and date
    to_encode.update({"exp":expire}) # it will update it

    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    # it will provide the algorithm means the token will be formed with this line
    return encoded_jwt


# to verify access token

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data=schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"could not validate",headers={"WWW_Authenticate":"Bearer"})
    token= verify_access_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id==token.id).first()
    return user  
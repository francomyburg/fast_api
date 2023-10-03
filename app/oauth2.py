from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas,database,models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    return encoded_jwt

def verify_acces_token(token:str,credentials_exception):
    
    try:    
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        id:str = payload.get("user.id")
        
        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id) 

    except JWTError:
        raise credentials_exception
    
    return token_data
     
def get_current_user(token:str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not valide credential",headers={"WWW-Authenticate":"Bearer"})
    
    token_data = verify_acces_token(token,credentials_exception)
   
    user = db.query(models.User).filter(models.User.id == token_data.id).first()

    return user

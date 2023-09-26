from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import ENVIROMENT,schemas
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

SECRET_KEY = ENVIROMENT.SECRET_KEY
ALGORITHM = ENVIROMENT.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = ENVIROMENT.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_acces_token(token:str,credentials_exception):
    try:    
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        id:str = payload.get("user_id")

        if id is None:
            return credentials_exception
        
        token_data = schemas.TokenData(id=id) 

    except JWTError:
        raise Exception
    
    return token_data
     
def get_current_user(token:str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not valide credential",headers={"WWW-Authenticate":"Bearer"})

    return verify_acces_token(token,credentials_exception)
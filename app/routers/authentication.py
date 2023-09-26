from fastapi import APIRouter,Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,utils,models,oauth2


router = APIRouter()

@router.post("/login",response_model=schemas.Token)
def login(user_credential:OAuth2PasswordRequestForm= Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email==user_credential.username).first()
    
    if not user:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credential")
    
    verify = utils.verifyPassword(user_credential.password, user.password)

    if not verify:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credential")
    
    token = oauth2.create_access_token(data={"user.id":user.id})
 
    return {"acces_token":token,"token_type":"bearer"}
        
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils
from ..database import get_db
from sqlalchemy.orm import Session



router = APIRouter(prefix="/users",tags=["Users"])





@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.ResponseUser)
def create_user(user: schemas.User_Create,db: Session = Depends(get_db)):

    #verificar si el email ya esta registrado
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El correo electrónico ya está en uso")
    
    #encriptar la contraseña
    utils.hashpassword(user)

    new_user = models.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return new_user

@router.get("/{id}",response_model=schemas.ResponseUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} was not found")
    
    return user


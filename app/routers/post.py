from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional,List


router = APIRouter(prefix="/posts",tags=["Posts"])





@router.get("/",response_model=list[schemas.Post])
def get_all_post(db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    
    post = db.query(models.Post).all()
    return post


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    

@router.get("/{id}",response_model=schemas.Post)
def get_post(id: int,db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""SELECT * FROM posts WHERE id=%s""",(id,))
    # post=cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id was not found")
    
    return post
    

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    """eliminar un elemento buscando por el id"""
    
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *;""",(id,))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id was not found")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,db: Session = Depends(get_db),user_id: int = Depends(oauth2.get_current_user)):
    "Actualizar un elemento por el id especificado"
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s,created_at=now()
    #                WHERE id=%s RETURNING *""",(post.title,post.content,post.published,id))
    # post = cursor.fetchone()
    # conn.commit()
    update_post = db.query(models.Post).filter(models.Post.id == id)

    if not update_post.first() :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id was not found")
    
    update_post.update(post.model_dump(),synchronize_session=False)

    db.commit()
    
    return update_post.first() 
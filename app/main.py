from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from typing import Optional
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models,schemas
from .database import engine,get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app=FastAPI()

# Dependency


#codigo para conectarse a la base datos,al usar el orm de sqlalchemy ya no se necesita
# while True:
#     try:
#         conn = psycopg2.connect(host="localhost",port=8080,dbname="Fastpi",user="admin",password="admin123",cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Database connection was successfull")
#         break
#     except Exception as error:
#         print("Connection failed")
#         print("Error: ",error)
#         time.sleep(2)






@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts",response_model=schemas.Post)
def get_all_post(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    
    post = db.query(models.Post).all()
    return post


@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(**post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    

@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id: int,db: Session = Depends(get_db)):

    # cursor.execute("""SELECT * FROM posts WHERE id=%s""",(id,))
    # post=cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id was not found")
    
    return post
    

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db)):
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
    
    
@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,db: Session = Depends(get_db)):
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
    
 
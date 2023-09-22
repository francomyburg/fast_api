from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app=FastAPI()


while True:
    try:
        conn = psycopg2.connect(host="localhost",port=8080,dbname="Fastpi",user="admin",password="admin123",cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print("Connection failed")
        print("Error: ",error)
        time.sleep(2)


class Post_model(BaseModel):
    title : str
    content : str
    published : bool = True



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_all_post():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"posts" : posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post_model = Body(...)):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"message":new_post}
    

@app.get("/posts/{id}")
def get_post(id: int):

    cursor.execute("""SELECT * FROM posts WHERE id=%s""",(id,))
    post=cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id was not found")
    
    return {"post_detail":post}
    

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    """eliminar un elemento buscando por el id"""
    
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *;""",(id,))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@app.put("/posts/{id}")
def update_post(id: int, post: Post_model):
    "Actualizar un elemento por el id especificado"
    cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s,created_at=now()
                   WHERE id=%s RETURNING *""",(post.title,post.content,post.published,id))
    post = cursor.fetchone()
    conn.commit()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id was not found")
    
    return {"Updated post":post}
    
 
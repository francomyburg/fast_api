from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange


app=FastAPI()

class Post_model(BaseModel):
    title : str
    content : str
    published : bool = True
    rating:Optional[int] = None


list_post=[  {"title": "title_1","content": "awesome_content","rating": 5,"id": 2},
           {"title": "no title","content": "content about the world cup","rating": 9,"id": 3},
            {"title": "title_3","content": "more content","rating": 5,"id": 4}]

def find_id(id):
    for item in list_post:
        if item["id"]==id:
            return item

def find_index(id):
     for index,element in enumerate(list_post):
        if element["id"]==id:
             return index

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_all_post():
    return list_post

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post: Post_model = Body(...)):
    dict_post=post.model_dump()
    dict_post["id"]=randrange(0,1000000)
    list_post.append(dict_post)
    return {"message":f"post {post.title} successfully created"}
    

@app.get("/posts/{id}")
def get_post(id: int):
    post=find_id(id)
    if post:
        return(post)
    else:
        # response.status_code = status.HTTP_404_NOT_FOUND 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id was not found")
    
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    """eliminar un elemento buscando por el id"""
    index = find_index(id)
    print(index)
    if index != None:
        del list_post[index]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id was not found")
    
@app.put("/posts/{id}")
def update_post(id: int, post: Post_model):
    "Actualizar un elemento por el id especificado"
    index = find_index(id)

    if index !=None:
        post_dict=post.model_dump()
        post_dict["id"]=id
        list_post[index]=post_dict
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id was not found")
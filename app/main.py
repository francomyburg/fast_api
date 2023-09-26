from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from typing import Optional,List
from . import models
from .database import engine,get_db
from sqlalchemy.orm import Session
from .routers import post,users,authentication




models.Base.metadata.create_all(bind=engine)

app=FastAPI()




app.include_router(post.router)
app.include_router(users.router)
app.include_router(authentication.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

    

from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,users,authentication,votes
from .config import settings


# print(settings.database_name)
models.Base.metadata.create_all(bind=engine)

app=FastAPI()




app.include_router(post.router)
app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(votes.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

    

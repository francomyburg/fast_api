from fastapi import Response,status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional,List


router = APIRouter(prefix="/posts",tags=["Posts"])



# ,response_model=list[schemas.PostOut]

@router.get("/",response_model=list[schemas.PostOut])
def get_all_post(db: Session = Depends(get_db),user: int = Depends(oauth2.get_current_user), limit: int= 10,skip:int=0,search: Optional[str]=""):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    
    
    results = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Post.id==models.Votes.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    response_data = []
    for post, vote_count in results:
       response_data.append({
            "post": {
            "id":post.id, 
            "title":post.title, 
            "content":post.content,
            "published":post.published,
            "created_at":post.created_at,
            "user_owner" :post.user_owner,
            "owner":post.owner
            },
            "votes": vote_count
        }) 
        
    return response_data


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db),user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.model_dump())
    new_post.user_owner = user.id


    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int,db: Session = Depends(get_db),user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""SELECT * FROM posts WHERE id=%s""",(id,))
    # post=cursor.fetchone()
    results = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Post.id==models.Votes.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if results:
        final_result={
            "post": {
                "id":results[0].id, 
                "title":results[0].title, 
                "content":results[0].content,
                "published":results[0].published,
                "created_at":results[0].created_at,
                "user_owner" :results[0].user_owner,
                "owner":results[0].owner
                },
                "votes": results[1]
             }
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id was not found")
    
    return final_result
    

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db),user: int = Depends(oauth2.get_current_user)):
    """eliminar un elemento buscando por el id"""
    
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *;""",(id,))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    post_user = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id was not found")
   

    if post_user.user_owner == user.id:
        
        post.delete(synchronize_session=False)
        db.commit()
    
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credential")
    
    
    

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,db: Session = Depends(get_db),user: int = Depends(oauth2.get_current_user)):
    "Actualizar un elemento por el id especificado"
    # cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s,created_at=now()
    #                WHERE id=%s RETURNING *""",(post.title,post.content,post.published,id))
    # post = cursor.fetchone()
    # conn.commit()
    update_post = db.query(models.Post).filter(models.Post.id == id)
    update_post_user = db.query(models.Post).filter(models.Post.id == id).first()
    if not update_post.first() :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id was not found")
    
    if update_post_user.user_owner == user.id:

        update_post.update(post.model_dump(),synchronize_session=False)
        db.commit()

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="invalid credential")
    
    
    return update_post.first() 
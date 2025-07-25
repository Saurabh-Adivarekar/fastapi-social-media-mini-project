from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
     prefix="/posts",
     tags=['Posts']
)

@router.get("/", response_model=list[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: str = ""
):
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return [{"post": post, "votes": votes} for post, votes in results]

# @router.get("/", response_model=List[schemas.PostOut])
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,search: Optional[str] = "" ):
    
       
# #     posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
# #     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
#     results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

#     return results



@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)


    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
     # post = db.query(models.Post).filter(models.Post.id == id).first()
     results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

     if not results:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail= f"post with id: {id} not found.")
     
     # if post.owner_id != current_user.id:
     #      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

     post, votes = results
     return {"post": post, "votes": votes}



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
     
     post_query = db.query(models.Post).filter(models.Post.id == id)

     post = post_query.first()

     if post == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found.")
     
     if post.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
     
     post_query.delete(synchronize_session=False)
     db.commit()

     return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_posts(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
     
     post_query = db.query(models.Post).filter(models.Post.id == id)
     post = post_query.first()

     if post == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found.")

     if post.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
     
     post_query.update(updated_post.dict(), synchronize_session=False)
     db.commit()
     return post_query.first()
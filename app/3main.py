#Path Operation

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()




while True:
     

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user="postgres", password="yoursecurepassword", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


my_posts = [{"title": "title 1", "content": "content2", "id": 1}, {"title": "favourite foods", "content": "I like pizza", "id": 2}]


def find_post(id):
    for i in my_posts:
        if i["id"] == id:
             return i
        

def find_index_post(id):
     for i, p in enumerate(my_posts):
          if p['id'] == id:
               return i

@app.get("/")
def root():
    return {"message": "Welcome to the api!"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"data": posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate,db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}



@app.get("/posts/latest")
def get_lastet_posts():
     post = my_posts[-1]
     return post
     


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
     post = db.query(models.Post).filter(models.Post.id == id).first()

     if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail= f"post with id: {id} not found.")
    #     #   response.status_code = status.HTTP_404_NOT_FOUND
    #     #   return {'message': f"post with id: {id} Not Found!"}
     return {"post_detail": post}




@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
     
     post = db.query(models.Post).filter(models.Post.id == id)

     if post.first() == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found.")
     
     post.delete(synchronize_session=False)
     db.commit()

     return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
def update_posts(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
     
     post_query = db.query(models.Post).filter(models.Post.id == id)
     post = post_query.first()

     if post == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found.")
     
     post_query.update(updated_post.dict(), synchronize_session=False)
     db.commit()
     return { "data" : post_query.first() }
#Path Operation

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time



app = FastAPI()


class Post(BaseModel):
        title: str
        content: str
        published: bool = True

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
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"new_post": f"title {payLoad['title']} content: {payLoad['content']}"}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/latest")
def get_lastet_posts():
     post = my_posts[-1]
     return post
     
@app.get("/posts/{id}")
def get_post(id: int):
     cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
     post = cursor.fetchone()
     post = find_post(id)
     if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail= f"post with id: {id} not found.")
    #     #   response.status_code = status.HTTP_404_NOT_FOUND
    #     #   return {'message': f"post with id: {id} Not Found!"}
     return {"post_detail": post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
     
     cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
     deleted_post = cursor.fetchone()
     conn.commit()

     if deleted_post == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found.")

     return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_posts(id: int, post: Post):

     cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
     updated_post = cursor.fetchone()
     conn.commit()

     if updated_post == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found.")
     
     return {"data" : updated_post }
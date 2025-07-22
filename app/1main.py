#Path Operation

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()


class Post(BaseModel):
        title: str
        content: str
        published: bool = True


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
    return {"data": my_posts}

# @app.post("/createposts")
# def create_posts(payLoad: dict = Body(...)):
#     print(payLoad)
#     return {"new_post": f"title {payLoad['title']} content: {payLoad['content']}"}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/latest")
def get_lastet_posts():
     post = my_posts[-1]
     return post
     
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
     post = find_post(id)
     if not post:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail= f"post with id: {id} not found.")
        #   response.status_code = status.HTTP_404_NOT_FOUND
        #   return {'message': f"post with id: {id} Not Found!"}
     return {"post_detail": post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
     index = find_index_post(id)

     if index == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found.")

     my_posts.pop(index)
     return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_posts(id: int, post: Post):
     index = find_index_post(id)

     if index == None:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id: {id} not found.")
     
     post_dict = post.dict()
     post_dict['id'] = id
     my_posts[index] = post_dict
     return {"data" : post_dict }
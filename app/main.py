from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)   #dont need if using alembic

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to the api!"}




# my_posts = [{"title": "title 1", "content": "content2", "id": 1}, {"title": "favourite foods", "content": "I like pizza", "id": 2}]


# def find_post(id):
#     for i in my_posts:
#         if i["id"] == id:
#              return i
        

# def find_index_post(id):
#      for i, p in enumerate(my_posts):
#           if p['id'] == id:
#                return i




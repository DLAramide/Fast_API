from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, conint
from typing import Optional
from random import randrange
app = FastAPI()

class Post(BaseModel):
    Title: str 
    Content: str
    Published: bool = True
    Rating: Optional[conint(ge=1, le=10)] = None
    


my_posts = [{
    "Title": "My First Post",
    "Content": "This is the content of my first post.",
    "Published": True,
    "Rating": 5, 
    "Id" : 1
}, {
    "Title": "My Second Post",
    "Content": "This is the content of my second post.",
    "Published": False,
    "Rating": 8,
    "Id": 2
}]

def find_post(id):
    for p in my_posts:
        if p['Id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['Id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Welcome"}

@app.get("/posts")
async def read_posts():
    return {"data": my_posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
async def create_post(new_post: Post):
    post_dict = new_post.dict()
    post_dict['Id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/latest")
async def get_latest_post():
    latest_post = my_posts[-1]
    return {"detail": latest_post}

@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    post = find_post(id)
    if post:
        return {"post_detail": post}
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": "Post not found"}
"""
@app.get("/posts/{id}")
async def get_post(id):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {"post_detail": post}
"""

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    #deleting post
    #find the index in the array that has the post required ID
    #my_posts.pop(index)
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    my_posts.pop(index)
    #return {'message': "Post has been deleted successfully."}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    post_dict = post.dict()
    post_dict['Id'] = id
    my_posts[index] = post_dict
    return {'message': post_dict}
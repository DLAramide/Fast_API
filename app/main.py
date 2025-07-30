from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel, conint
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    Title: str 
    Content: str
    Published: bool = True
while True:
    try:
        conn = psycopg2.connect(host= 'localhost', database ='postgres', user='postgres',
                                password='password',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was successful')
        break
    except Exception as error:
        

        print('Connecting to database failed')
        print("Error:",error)
        time.sleep(5)
        


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
    cursor.execute("""SELECT * FROM post""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
async def create_post(new_post: Post):
    cursor.execute(""" INSERT INTO public.post ("Title","Content","Published") VALUES (%s, %s ,%s) RETURNING
                   *  """,(new_post.Title,new_post.Content,new_post.Published))
    
    post = cursor.fetchone()
    conn.commit()
    return {"data":post}


@app.get("/posts/latest")
async def get_latest_post():
    latest_post = my_posts[-1]
    return {"detail": latest_post}

@app.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute("""SELECT * FROM post WHERE "Id" = %s """, (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post_detail": post}
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
    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (id,))
    deleted_post = cursor.fetchone()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")

    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    cursor.execute("""UPDATE post SET "Title"=%s,"Content"=%s,"Published"=%s WHERE id = %s RETURNING * """,
                    (post.Title,post.Content,post.Published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return {'message': updated_post}
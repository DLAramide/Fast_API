from fastapi import FastAPI, Response, status, HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel, conint
from typing import Optional,List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from . import models, schemas
from .users import router as user_router
from .database import get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user_router)




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



@app.get("/")
async def root():
    return {"message": "Welcome"}

@app.get("/posts",response_model=List[schemas.Post])
async def read_posts(db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM post""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts
    

@app.post("/posts", status_code = status.HTTP_201_CREATED,response_model=schemas.Post)
async def create_post(new_post: schemas.PostCreate,db: Session = Depends(get_db)):
    #cursor.execute(""" INSERT INTO public.post ("Title","Content","Published") VALUES (%s, %s ,%s) RETURNING
     #              *  """,(new_post.Title,new_post.Content,new_post.Published))
    
    #post = cursor.fetchone()
    #conn.commit()
    post = models.Post(**new_post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post



@app.get("/posts/{id}")
async def get_post(id: int,db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM post WHERE "Id" = %s """, (id,))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
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

#@app.get("/sqlalchemy")
#def test_posts(db: Session = Depends(get_db)):
#    posts = db.query(models.Post).all()
#    return{"data":posts}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int,db: Session = Depends(get_db)):
#    cursor.execute("""DELETE FROM post WHERE id = %s RETURNING *""", (id,))
#    deleted_post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    post.delete(synchronize_session = False)
    db.commit()

    #conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int,updated_post: schemas.PostCreate,db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    #cursor.execute("""UPDATE post SET "Title"=%s,"Content"=%s,"Published"=%s WHERE id = %s RETURNING * """,
    #                (post.Title,post.Content,post.Published,str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post


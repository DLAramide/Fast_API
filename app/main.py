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
from .routers.users import router as user_router
from .database import get_db
from .routers import post,users
from .routers.post import router as post_router
from .routers.auth import router as auth_router


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)




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




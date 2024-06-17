from fastapi import Response, FastAPI, status, HTTPException, Depends
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from sqlalchemy.orm import Session

from .database import engine, get_db
from .routers import post, users, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="greengoblin",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("DB connection success")
        break
    except Exception as error:
        print("Failed to connect to DB")
        print("Error : ", error)
        time.sleep(3)

my_posts = [
    {
        "title": "title of post 1 hardcode",
        "content": "Content of post 1 harcode",
        "published": False,
        "id": 1,
    },
    {
        "title": "favourite foods",
        "content": "I like chilly garlic noodles",
        "published": False,
        "id": 2,
    },
]


def find_post(posts, id):
    for post in posts:
        if post["id"] == id:
            return post


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Welcome to my API!!"}

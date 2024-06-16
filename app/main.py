from fastapi import Response, FastAPI, status, HTTPException, Depends
from typing import List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

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


@app.get("/")
def root():
    return {"message": "Welcome to my API!!"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(
        **post.model_dump()
    )  # convert the post to dictionary and unpack it so we get it in desired format

    db.add(new_post)  # Add a new post
    db.commit()  # Commit to DB
    db.refresh(new_post)  # retrieve the new post created to display
    return new_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_posts(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id : {id} not found",
        )
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = (
        db.query(models.Post)
        .filter(models.Post.id == id)
        .delete(synchronize_session=False)
    )  # this query returns the number of posts deleted
    if deleted_post == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID : {id} not found",
        )
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(
    id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id : {id} was not found",
        )
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()

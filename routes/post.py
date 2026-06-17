from models.post import AddPost, UpdatePost, PatchPost, PostResponse
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database.database_conf import Post, get_db

post_router = APIRouter(tags=["Posts"])

@post_router.get("/", response_model=List[PostResponse])
def get_posts(db:Session = Depends(get_db)) -> dict:
  return db.query(Post).all()

@post_router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id:int, db:Session = Depends(get_db)) -> dict:
  post = db.query(Post).filter(Post.id == post_id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
  return post

@post_router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post:AddPost, db:Session = Depends(get_db)) -> dict:
  new_post = Post(**post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

@post_router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id:int, post:UpdatePost, db:Session = Depends(get_db)) -> dict:
  db_post = db.query(Post).filter(Post.id == post_id).first()
  if not db_post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
  for field, value in post.model_dump().items():
    setattr(db_post, field, value)
  db.commit()
  db.refresh(db_post)
  return db_post

@post_router.patch("/{post_id}", response_model=PostResponse)
def patch_post(post_id:int, post: PatchPost, db: Session = Depends(get_db)) -> dict:
  db_post = db.query(Post).filter(Post.id == post_id).first()
  if not db_post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
  post_data = post.model_dump(exclude_unset=True)
  print(post_data)
  for field, value in post_data.items():
    setattr(db_post, field, value)
  db.commit()
  db.refresh(db_post)
  return db_post

@post_router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)) -> dict:
  db_post = db.query(Post).filter(Post.id == post_id).first()
  if not db_post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
  db.delete(db_post)
  db.commit()
  return {"message": "sucessfully"}

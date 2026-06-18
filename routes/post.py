from models.post import AddPost, UpdatePost, PatchPost, PostResponse
from utils.validate import validate_data
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Path
from sqlalchemy import or_
from sqlalchemy.orm import Session
from database.database_conf import Post, get_db

post_router = APIRouter(tags=["Posts"])

@post_router.get("/", response_model=List[PostResponse])
def get_posts(term:str | None = None, db:Session = Depends(get_db)) -> dict:
  query = db.query(Post)
  if term:
    pattern = f"%{term}%"
    query = query.filter(
      or_(
        Post.title.ilike(pattern),
        Post.content.ilike(pattern),
        Post.category.ilike(pattern)
      )
    )
  return query.all()

@post_router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id:int = Path(..., le=100, gt=0, description="Post ID to retrieve"), db:Session = Depends(get_db)) -> dict:
  post = db.query(Post).filter(Post.id == post_id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
  return post

@post_router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post:AddPost, db:Session = Depends(get_db)) -> dict:
  if validate_data(post) == False:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
  new_post = Post(**post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post

@post_router.put("/{post_id}", response_model=PostResponse)
def update_post(post:UpdatePost, db:Session = Depends(get_db), post_id:int = Path(..., le=100, gt=0, description="Post ID to update")) -> dict:
  db_post = db.query(Post).filter(Post.id == post_id).first()
  if not db_post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
  if validate_data(post) == False:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
  for field, value in post.model_dump().items():
    setattr(db_post, field, value)
  db.commit()
  db.refresh(db_post)
  return db_post

@post_router.patch("/{post_id}", response_model=PostResponse)
def patch_post(post: PatchPost, db: Session = Depends(get_db), post_id:int = Path(..., le=100, gt=0, description="Post ID to patch")) -> dict:
  db_post = db.query(Post).filter(Post.id == post_id).first()
  if not db_post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
  post_data = post.model_dump(exclude_unset=True)
  for field, value in post_data.items():
    setattr(db_post, field, value)
  db.commit()
  db.refresh(db_post)
  return db_post

@post_router.delete("/{post_id}")
def delete_post(db: Session = Depends(get_db), post_id:int = Path(..., le=100, gt=0, description="Post ID to delete")) -> dict:
  db_post = db.query(Post).filter(Post.id == post_id).first()
  if not db_post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found!")
  db.delete(db_post)
  db.commit()
  raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Post successfully deleted!")

from models.post import AddPost
from fastapi import APIRouter

post_router = APIRouter(tags=["Posts"])

@post_router.get("/")
def get_posts():
  return {"message": "posts sucessfully"}


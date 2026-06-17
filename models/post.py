from pydantic import BaseModel
from typing import Optional, List

class AddPost(BaseModel):
  title:str
  content:str
  category:str
  tags:List[str]

class UpdatePost(AddPost):
  pass

class PatchPost(BaseModel):
  title:Optional[str] = None
  content:Optional[str] = None
  category:Optional[str] = None
  tags:Optional[List[str]] = None

class PostResponse(AddPost):
  id:int

  class Config:
    from_attributes = True

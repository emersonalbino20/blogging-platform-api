from pydantic import BaseModel, field_serializer
from datetime import datetime
from typing import List

class AddPost(BaseModel):
  title:str
  content:str
  category:str
  tags:List[str]

class UpdatePost(AddPost):
  pass

class PatchPost(BaseModel):
  title:str | None = None
  content:str | None = None
  category:str | None = None
  tags:List[str] | None = None

class PostResponse(AddPost):
  id:int
  createdAt:datetime
  updatedAt:datetime

  class Config:
    from_attributes = True
  
  @field_serializer('createdAt', 'updatedAt')
  def serialize_dt(self, dt: datetime, _info):
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

from pydantic import BaseModel, Field, field_serializer
from datetime import datetime
from typing import List

class AddPost(BaseModel):
    title: str = Field(..., min_length=4, max_length=20, examples=["DevPost"])
    content: str = Field(..., min_length=10, max_length=100, examples=["In this event the dresscode..."])
    category: str = Field(..., min_length=2, max_length=10, examples=["T.I"])
    tags: List[str] = Field(..., min_length=2, max_length=10, examples=[["#computer", "#code"]])

class UpdatePost(AddPost):
  pass

class PatchPost(BaseModel):
  title: str = Field(None, min_length=4, max_length=100, examples=["DevPost"])
  content: str = Field(None, min_length=10, max_length=100, examples=["In this event the dressco    de..."])
  category: str = Field(None, min_length=2, max_length=10, examples=["T.I"])
  tags: List[str] = Field(None, min_length=2, max_length=10, examples=[["#computer", "#code"]])

class PostResponse(AddPost):
  id: int = Field(..., gt=0, examples=[1])
  createdAt: datetime
  updatedAt:datetime

  class Config:
    from_attributes = True
  
  @field_serializer('createdAt', 'updatedAt')
  def serialize_dt(self, dt: datetime, _info):
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

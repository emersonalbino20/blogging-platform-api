from pydantic import BaseModel, EmailStr
from typing import Optional, List

class AddPost(BaseModel):
  title:str
  content:str
  category:str
  tags:List[str]

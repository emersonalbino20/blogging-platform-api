from models.post import AddPost

def validate_data(post) -> bool:
  data = post.dict()
  for key, value in data.items():
    if key == 'tags':
      for tg in value:
        if len(tg.strip()) < 4:
          return False
      continue
    elif key == 'content' and len(value.strip()) < 10:
      return False
    else:
      if len(value.strip()) < 4:
        return False
  return True
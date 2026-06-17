from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_UR = "sqlite:///database/blog.db"
engine = create_engine(DATABASE_UR, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Post(Base):
  __tablename__ = "posts"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String(100), nullable=False)
  content = Column(String(100), nullable=False)
  category = Column(String(100), nullable=False)
  tags = Column(JSON, nullable=False)

Base.metadata.create_all(engine)

def get_db():
  try:
    db = SessionLocal()
    yield db
  finally:
    db.close()

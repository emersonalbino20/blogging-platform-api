from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database_conf import get_db
from routes.post import post_router
import uvicorn

app = FastAPI(title="Blogging Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Aceita qualquer origem
    allow_credentials=False,
    allow_methods=["*"],  # Aceita GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Aceita qualquer header
)

get_db()

@app.get("/")
def root() -> dict:
	return {"message": "wellcome to blog"}

app.include_router(post_router, prefix="/posts")

if __name__ == "__main__":
	uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

from fastapi import FastAPI
from routes.post import post_router
import uvicorn

app = FastAPI(title="Blogging Platform API")

@app.get("/")
def root() -> dict:
	return {"message": "wellcome to blog"}

app.include_router(post_router, prefix="/posts")

if __name__ == "__main__":
	uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

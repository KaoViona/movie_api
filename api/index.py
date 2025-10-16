from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from posts_data import posts
import os

app = FastAPI()

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "../static")
INDEX_FILE = os.path.join(STATIC_DIR, "index.html")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def read_index():
    if os.path.exists(INDEX_FILE):
        return FileResponse(INDEX_FILE)
    return {"message": "index.html not found"}

class Comment(BaseModel):
    user: str
    text: str

@app.get("/posts")
def get_posts():
    return posts

@app.post("/posts/{post_id}/like")
def like_post(post_id: int):
    if post_id in posts:
        posts[post_id]["likes"] += 1
        return {"likes": posts[post_id]["likes"]}
    return {"error": "post not found"}

@app.post("/posts/{post_id}/comment")
def comment_post(post_id: int, comment: Comment):
    if post_id in posts:
        posts[post_id]["comments"].append({
            "user": comment.user,
            "text": comment.text
        })
        return {"comments": posts[post_id]["comments"]}
    return {"error": "post not found"}

# 這一行是重點，讓 Vercel 入口認得 app
handler = app

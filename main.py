from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from posts_data import posts
import os

app = FastAPI()

# === CORS 設定 ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === 靜態資料夾設定 ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
INDEX_FILE = os.path.join(STATIC_DIR, "index.html")

# 掛載 static 資料夾 (讓 JS / CSS 可以正常讀)
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# === 首頁 route ===
@app.get("/")
def read_index():
    if os.path.exists(INDEX_FILE):
        return FileResponse(INDEX_FILE)
    else:
        raise HTTPException(status_code=404, detail=f"找不到檔案: {INDEX_FILE}")

# === 留言資料模型 ===
class Comment(BaseModel):
    user: str
    text: str

# === API routes ===
@app.get("/posts")
def get_posts():
    return posts

@app.post("/posts/{post_id}/like")
def like_post(post_id: int):
    if post_id in posts:
        posts[post_id]["likes"] += 1
        return {"likes": posts[post_id]["likes"]}
    raise HTTPException(status_code=404, detail="找不到貼文")

@app.post("/posts/{post_id}/comment")
def comment_post(post_id: int, comment: Comment):
    if post_id in posts:
        posts[post_id]["comments"].append({
            "user": comment.user,
            "text": comment.text
        })
        return {"comments": posts[post_id]["comments"]}
    raise HTTPException(status_code=404, detail="找不到貼文")

# === Vercel 專用 ===
handler = app

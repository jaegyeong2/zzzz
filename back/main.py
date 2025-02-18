from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users, posts, comments

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

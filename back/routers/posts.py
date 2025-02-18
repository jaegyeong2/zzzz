from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schema
import security
from model import Post, User

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

# 게시물 생성
@router.post("/Create", response_model=schema.Post)
def create_post(
    post: schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    db_post = Post(
        title=post.title,
        content=post.content,
        user_id=current_user.id
        
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# 게시물 수정
@router.put("/Update", response_model=schema.Post)
def update_post(
    post_id: int,
    post_update: schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다")
    
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="게시물을 수정할 권한이 없습니다")

    db_post.title = post_update.title
    db_post.content = post_update.content
    
    db.commit()
    db.refresh(db_post)
    
    return db_post

# 게시물 삭제
@router.delete("/Delete", response_model=schema.Post)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다")
    
    if db_post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="게시물을 삭제할 권한이 없습니다")

    db.delete(db_post)
    db.commit()
    
    return db_post

# 게시물 id로 특정 게시물 조회(조회수도 같이 조회) 
@router.get("/Read{post_id}", response_model=schema.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="게시물을 찾을 수 없습니다")

    db_post.view_count += 1
    db.commit()
    db.refresh(db_post)
    
    return db_post
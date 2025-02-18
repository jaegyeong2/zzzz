from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schema
import security
from model import Comment, Post, User

router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)

# 댓글 추가 
@router.post("/Create", response_model=schema.Comment)
def create_comment(
    comment: schema.CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_user)
):
    db_post = db.query(Post).filter(Post.id == comment.post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_comment = Comment(
        content=comment.content,
        post_id=comment.post_id,
        user_id=current_user.id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


# 사용자id로 댓글 조회
@router.get("/user/{user_id}", response_model=List[schema.Comment])
def read_comments_by_user(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_user) 
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only view your own comments"
        )
    
    comments = db.query(Comment).filter(Comment.user_id == user_id)\
        .offset(skip).limit(limit).all()
    
    return comments
# 댓글 수정
@router.put("/update", response_model=schema.Comment)
def update_comment(
    comment_id: int,  
    comment_update: schema.CommentCreate,  
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_user) 
):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")  

    if db_comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to edit this comment")  

    db_comment.content = comment_update.content
    db.commit()
    db.refresh(db_comment)
    
    return db_comment  

# 댓글 삭제
@router.delete("/delete", response_model=schema.Comment)
def delete_comment(
    comment_id: int,  
    db: Session = Depends(get_db),
    current_user: User = Depends(security.get_current_user)  
):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")  

    if db_comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this comment")  

    db.delete(db_comment)
    db.commit()
    
    return db_comment 
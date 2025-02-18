from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):  
    username: str
    email: EmailStr

# UserCreate와 User는 재사용을 하기 쉽게 하기위해서 UserBase를 상속받게끔 만듦
class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    content: str

# PostCreate와 Post도 PostBase 상속받음
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    user_id: int
    view_count: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    post_id: int

class Comment(CommentBase):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# 토큰 반환 모델
class Token(BaseModel):
    access_token: str
    token_type: str

# 토큰에서 추출된 데이터 모델
class TokenData(BaseModel):
    username: Optional[str] = None
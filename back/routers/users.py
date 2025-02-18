from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import schema
import security
from model import User
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# 회원가입
@router.post("/register", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    try:
        if db.query(User).filter(User.username == user.username).first():
            raise HTTPException(status_code=400, detail="이름 중복")

        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="이메일 중복")

        db_user = User(
            username=user.username,
            email=user.email,
            password_hash = security.get_password_hash(user.password)
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="회원가입 중 오류가 발생했습니다")
    
# 로그인
@router.post("/users/login", response_model=schema.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = security.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# 현재 로그인된 사용자 정보 반환
@router.get("/me", response_model=schema.User)
def read_user_me(current_user: User = Depends(security.get_current_user)):
    return current_user
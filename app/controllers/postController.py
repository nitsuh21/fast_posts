from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List
from ..schemas.post_schema import PostSchema, PostResponseSchema
from ..services.post_service import PostService
from ..utils.auth import verify_token
from ..main import SessionLocal

router = APIRouter()
post_service = PostService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Header(...)):
    email = verify_token(token)
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return email

@router.post("/posts", response_model=PostResponseSchema)
def add_post(post_data: PostSchema, db: Session = Depends(get_db), token: str = Header(...)):
    email = get_current_user(token)
    user_id = post_service.get_user_id_by_email(db, email)
    return post_service.add_post(db, post_data, user_id)

@router.get("/posts", response_model=List[PostResponseSchema])
def get_posts(db: Session = Depends(get_db), token: str = Header(...)):
    email = get_current_user(token)
    user_id = post_service.get_user_id_by_email(db, email)
    return post_service.get_posts(db, user_id)

@router.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), token: str = Header(...)):
    email = get_current_user(token)
    user_id = post_service.get_user_id_by_email(db, email)
    post_service.delete_post(db, post_id)
    return {"message": "Post deleted successfully"}

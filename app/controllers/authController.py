from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas.auth_schema import SignupSchema, LoginSchema, TokenSchema
from ..services.auth_service import AuthService
from ..main import SessionLocal

router = APIRouter()
auth_service = AuthService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model=TokenSchema)
def signup(signup_data: SignupSchema, db: Session = Depends(get_db)):
    user = auth_service.signup(db, signup_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    token = auth_service.login(db, signup_data)
    return {"token": token}

@router.post("/login", response_model=TokenSchema)
def login(login_data: LoginSchema, db: Session = Depends(get_db)):
    token = auth_service.login(db, login_data)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"token": token}

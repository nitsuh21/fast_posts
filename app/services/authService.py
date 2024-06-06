from sqlalchemy.orm import Session
from ..schemas.auth_schema import SignupSchema, LoginSchema
from ..models.user import User
from ..repositories.user_repository import UserRepository
from ..utils.auth import create_access_token
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_repository = UserRepository()

class AuthService:

    def signup(self, db: Session, signup_data: SignupSchema):
        hashed_password = pwd_context.hash(signup_data.password)
        new_user = User(email=signup_data.email, hashed_password=hashed_password)
        return user_repository.create_user(db, new_user)

    def login(self, db: Session, login_data: LoginSchema):
        user = user_repository.get_user_by_email(db, login_data.email)
        if user and pwd_context.verify(login_data.password, user.hashed_password):
            token = create_access_token(data={"sub": user.email})
            return token
        return None

from fastapi import FastAPI
from app.models import user, post
from .controllers import auth_controller, post_controller
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# Create the database tables
user.Base.metadata.create_all(bind=engine)
post.Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_controller.router, prefix="/auth")
app.include_router(post_controller.router, prefix="/posts")

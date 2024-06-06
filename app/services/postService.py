from sqlalchemy.orm import Session
from ..schemas.post_schema import PostSchema
from ..models.post import Post
from ..repositories.post_repository import PostRepository
from ..utils.cache import cache

post_repository = PostRepository()

class PostService:

    def add_post(self, db: Session, post_data: PostSchema, user_id: int):
        new_post = Post(text=post_data.text, user_id=user_id)
        return post_repository.create_post(db, new_post)

    def get_posts(self, db: Session, user_id: int):
        if user_id in cache:
            return cache[user_id]
        posts = post_repository.get_posts_by_user(db, user_id)
        cache[user_id] = posts
        return posts

    def delete_post(self, db: Session, post_id: int):
        post_repository.delete_post(db, post_id)

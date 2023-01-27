from db.models import DbComment
from sqlalchemy.orm.session import Session
from datetime import datetime
from routers.schemas import CommentBase


def create_comment(db: Session, request: CommentBase):
    new_comment = DbComment(
        text = request.text,
        username = request.username,
        post_id = request.post_id,
        timestamp = datetime.now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

def get_all_comments(db: Session, post_id: int):
    return db.query(DbComment).filter(DbComment.post_id == post_id).all()
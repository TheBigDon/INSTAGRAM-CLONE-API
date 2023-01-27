from fastapi import APIRouter, Depends, status, UploadFile, File
from routers.schemas import PostBase, PostDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from db import db_post
from fastapi.exceptions import HTTPException
from typing import List
import random
import string
import shutil

router = APIRouter(
    prefix='/post',
    tags=['post']
)

image_url_types = ['absolute', 'relative']

@router.post('', response_model=PostDisplay)
def create_post(request: PostBase, db: Session = Depends(get_db)):
    if not request.image_url_type in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
        detail="Параметр image_url_type принимает значение либо 'absolute', либо 'relative'.")
    return db_post.create_post(db, request)

@router.get('/all', response_model=List[PostDisplay])
def get_all_posts(db: Session = Depends(get_db)):
    return db_post.get_all_posts(db)

@router.post('/image')
def upload_image(image: UploadFile = File(...)):
    letters = string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(6))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.', 1))
    path = f'images/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {'filename': path}
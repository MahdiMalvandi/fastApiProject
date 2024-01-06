import datetime

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

import models.users as models
from schemas import schemas
from dependencies import get_db

router = APIRouter()


@router.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail='Username already exists')

    user = models.User(first_name=user.first_name, last_name=user.last_name, username=user.username,
                       password=user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get('/users/{user_id}/', response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    return db_user


@router.get('/users/', response_model=list[schemas.User])
def users(db: Session = Depends(get_db)):
    db_user = db.query(models.User).all()
    return db_user



@router.on_event('startup')
def change():
    with open('logs.log', 'a') as log:
        log.write(f'Starting Server {datetime.datetime.now()} \n')

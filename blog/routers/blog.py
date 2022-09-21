from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models
from typing import List
from sqlalchemy.orm import Session
from ..storage import repblog
from ..oaut2 import get_current_user, check_admin, check_writer, check_ban

router = APIRouter(prefix="/blog", tags=["For Blog"])

get_db = database.get_db


@router.get("/all", response_model=List[schemas.Show_Blog], dependencies=[Depends(check_ban)])
def all_blogs(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return repblog.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_writer)])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return repblog.create(request, db)


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(check_admin)])
def delete_blog(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return repblog.delete(id, db)


@router.put("/drawer/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(check_writer)])
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return repblog.update(id, request, db)


@router.put("/publish/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(check_writer)])
def publish_blog(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return repblog.publish(id, db)


@router.get("/{id}", status_code=200, dependencies=[Depends(check_ban)])
def get_blog(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return repblog.show(id, db)


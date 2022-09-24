from fastapi import APIRouter, Depends, status
from .. import schemas, database, models
from sqlalchemy.orm import Session
from ..storage import repblog
from ..oaut2 import get_current_user, check_admin, check_writer, check_ban, check_moder

router = APIRouter(prefix="/blog", tags=["For Blog"])

get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Show_Blog, dependencies=[Depends(check_writer)])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return repblog.create(request, db, current_user)


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(check_admin)])
def delete_blog(id: int, db: Session = Depends(get_db)):
    return repblog.delete(id, db)


@router.put("/drawer/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(check_writer)])
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    return repblog.update(id, request, db)


@router.put("/publish/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(check_writer)])
def publish_blog(id: int, db: Session = Depends(get_db)):
    return repblog.publish(id, db)


@router.get("/{id}", status_code=200, response_model=schemas.Show_Blog, dependencies=[Depends(check_ban)])
def get_blog(id: int, db: Session = Depends(get_db)):
    return repblog.show(id, db)


@router.get("/published/{id}", status_code=200, response_model=schemas.Show_Blog, dependencies=[Depends(check_moder)])
def get_published(id: int, db: Session = Depends(get_db)):
    return repblog.show_published(id, db)


@router.put("/accept/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(check_moder)])
def accept_blog(id: int, db: Session = Depends(get_db)):
    return repblog.accept(id, db)


@router.put("/reject/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(check_moder)])
def reject_blog(id: int, request: str, db: Session = Depends(get_db)):
    return repblog.reject(id, request, db)


@router.get("/rejected/{id}", status_code=200, response_model=schemas.ShowReject, dependencies=[Depends(check_writer)])
def get_rejected(id: int, db: Session = Depends(get_db)):
    return repblog.show_rejected(id, db)

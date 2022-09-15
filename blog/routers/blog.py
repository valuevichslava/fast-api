from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models
from typing import List
from sqlalchemy.orm import Session
from ..storage import repblog
from ..oaut2 import get_current_user

router = APIRouter(prefix="/blog", tags=["For Blog"])

get_db = database.get_db


@router.get("/all", response_model=List[schemas.Show_Blog])
def all_blogs(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return repblog.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return repblog.create(request, db)


@router.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    blog.delete(synchronize_session=False)
    db.commit()
    return repblog.delete(id, db)


@router.put("/upgrade/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return repblog.update(id, request, db)


@router.get("/{id}", status_code=200, response_model=schemas.Show_Blog)
def get_blog(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    return repblog.show(id, db)
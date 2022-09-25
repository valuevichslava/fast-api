from fastapi import APIRouter, Depends, status
from .. import schemas, database, models
from sqlalchemy.orm import Session
from ..storage import repblog
from ..oaut2 import get_current_user, check_admin, check_writer, check_ban, check_moder
from typing import List

router = APIRouter(prefix="/blog", tags=["For Blog"])

get_db = database.get_db


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Show_Blog, dependencies=[Depends(check_writer)])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return repblog.create(request, db, current_user)


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(check_admin)])
def delete_blog(id: int, db: Session = Depends(get_db)):
    return repblog.delete(id, db)


@router.put("/drawer/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(check_writer)])
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return repblog.update(id, request, db, current_user)


@router.put("/publish/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(check_writer)])
def publish_blog(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return repblog.publish(id, db, current_user)


@router.get("/{id}", status_code=200,
            dependencies=[Depends(check_ban)])
def get_blog(id: int, db: Session = Depends(get_db)):
    b = repblog.show(id, db)
    sb = schemas.Show_Blog.from_orm(b)
    asd: List[schemas.CommentResp] = []
    for comm in sb.comm:
        if comm.accepted:
            asd.append(comm)
    sb.comm = asd
    #print(sb.dict(include={'id': True, 'title': True, 'body': True, 'comm': {'__all__': {'id', 'author_email',' content'}}}))
    return sb.dict(include={'id': True, 'title': True, 'body': True, 'comm': {'__all__': {'id', 'author_email', 'content'}}})

@router.get("/published/{id}", status_code=200,
            response_model=schemas.Show_Blog,
            dependencies=[Depends(check_moder)])
def get_published(id: int, db: Session = Depends(get_db)):
    return repblog.show_published(id, db)


@router.put("/accept/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(check_moder)])
def accept_blog(id: int, db: Session = Depends(get_db)):
    return repblog.accept(id, db)


@router.put("/reject/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(check_moder)])
def reject_blog(id: int, request: str, db: Session = Depends(get_db)):
    return repblog.reject(id, request, db)


@router.get("/rejected/{id}", status_code=200, response_model=schemas.ShowReject, dependencies=[Depends(check_writer)])
def get_rejected(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return repblog.show_rejected(id, db, current_user)


@router.put("/backtodrawer/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(check_moder)])
def return_to_drawer(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return repblog.back_to_drawer(id, db, current_user)


@router.post("/addcomment/{id}", response_model=schemas.CommentResp, status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_ban)])
def add_comment(id: int, request: schemas.CommentForm, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return repblog.comment_blog(id, request, db, current_user)


@router.get("/shownewcomments/{id}", status_code=200, dependencies=[Depends(check_moder)])
def get_new_comments(id: int, db: Session = Depends(get_db)):
    return repblog.show_new_comments(id, db)


@router.put("/acceptcomment/{id}", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(check_moder)])
def accept_new_comment(blog_index: int, id: int, db: Session = Depends(get_db)):
    return repblog.accept_comment(blog_index, id, db)
from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status


def create(request: schemas.Blog, db: Session, current_user: models.User):
    new_blog = models.Blog(title=request.title, body=request.body, email_id=current_user.email, drawer=True)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    else:
        blog.delete(synchronize_session=False)
        db.commit()
        return "done"


def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.drawer==True)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    blog.update(request.dict(), synchronize_session=False)
    db.commit()
    return "Blog updated"


def show(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.accepted == True).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    return blog


def publish(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    blog.update({models.Blog.published: True, models.Blog.drawer: False}, synchronize_session=False)
    db.commit()
    return "Blog published"


def show_published(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.published == True).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    return blog


def accept(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.published == True)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    blog.update({models.Blog.accepted: True, models.Blog.published: False}, synchronize_session=False)
    db.commit()
    return "Blog accepted"


def reject(id: int, request: str, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.published == True)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    blog.update({models.Blog.moder_comm: request, models.Blog.rejected: True, models.Blog.published: False}, synchronize_session=False)
    db.commit()
    return "Blog rejected"


def show_rejected(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.rejected == True).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    return blog



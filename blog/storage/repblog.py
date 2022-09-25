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


def update(id: int, request: schemas.Blog, db: Session, current_user: models.User):
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.drawer==True, models.Blog.email_id == current_user.email)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    blog.update(request.dict(), synchronize_session=False)
    db.commit()
    return "Blog updated"


def show(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.accepted == True).first()
    #comment = db.query(models.Comment).filter(models.Comment.blog_id == id, models.Comment.accepted == True).all()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    return blog


def publish(id: int, db: Session, current_user: models.User):
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.email_id == current_user.email)
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


def show_rejected(id: int, db: Session, current_user: models.User):
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.rejected == True, models.Blog.email_id == current_user.email).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    return blog


def back_to_drawer(id: int, db: Session, current_user: models.User):
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.accepted == True, models.Blog.email_id == current_user.email)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    blog.update({models.Blog.accepted: False, models.Blog.drawer: True}, synchronize_session=False)
    db.commit()
    return "Blog return to drawer"


def comment_blog(id: int, request: schemas.CommentForm, db: Session, current_user: models.User):
    new_comment = models.Comment(content=request.body, author_email=current_user.email, blog_id=id, consideration=True)
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.accepted == True).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} does not exist")
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def show_new_comments(id: int, db: Session):
    comment = db.query(models.Comment).filter(models.Comment.blog_id == id, models.Comment.consideration == True).all()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comments do not exist")
    return comment


def accept_comment(blog_index: int, id:int, db: Session):
    comment = db.query(models.Comment).filter(models.Comment.blog_id == blog_index, models.Comment.id == id, models.Comment.consideration == True)
    if not comment.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with id {id} does not exist")
    comment.update({models.Comment.accepted: True, models.Comment.consideration: False}, synchronize_session=False)
    db.commit()
    return "Comment accepted"
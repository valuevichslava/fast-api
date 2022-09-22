from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status
from ..hashing import Hash


def ucreate(request: schemas.User, db: Session):
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.bcrypt(request.password),
        is_banned=False, adm=request.role.adm, moder=request.role.moder, writer=request.role.writer, user=request.role.user
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def ushow(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    return user


def u_get_ban(id: int, request: schemas.UserAdmin, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    user.update(request.dict(), synchronize_session=False)
    db.commit()
    return "Settings for User updated"


def u_get_role(id: int, request: schemas.Roles, db: Session):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    user.update(request.dict(), synchronize_session=False)
    db.commit()
    return "Settings for User updated"


'''''
def get_role(request: schemas.Roles, db: Session):
    new_role = models.Roles(role=request.role, user_index=1)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role
'''
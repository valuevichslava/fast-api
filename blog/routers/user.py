from fastapi import APIRouter, Depends
from .. import schemas, database
from sqlalchemy.orm import Session
from ..storage import reuser
from ..oaut2 import check_admin, check_ban

router = APIRouter(prefix="/user", tags=["For User"])

get_db = database.get_db


@router.post("/")
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return reuser.ucreate(request, db)


@router.put("/giveban/{id}", dependencies=[Depends(check_admin)])
def give_ban(id, request: schemas.UserAdmin, db: Session = Depends(get_db)):
    return reuser.u_get_ban(id, request, db)


@router.put("/giverole/{id}", dependencies=[Depends(check_admin)])
def give_role(id, request: schemas.Roles, db: Session = Depends(get_db)):
    return reuser.u_get_role(id, request, db)


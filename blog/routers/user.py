from fastapi import APIRouter, Depends
from .. import schemas, database
from sqlalchemy.orm import Session
from ..storage import reuser
from ..oaut2 import get_current_user, check_admin, check_ban

router = APIRouter(prefix="/user", tags=["For User"])

get_db = database.get_db


@router.post("/")
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return reuser.ucreate(request, db)


@router.get("/{id}", response_model=schemas.Show_User, dependencies=[Depends(check_ban)])
def get_user(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return reuser.ushow(id, db)


@router.put("/adminConsole/{id}", dependencies=[Depends(check_admin)])
def give_role(id, request: schemas.UserAdmin, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return reuser.u_get_ban(id, request, db)

'''''
@router.post("/addroles")
def add_role(request: schemas.Roles, db: Session = Depends(get_db)):
    print("Hello")
    return reuser.get_role(request, db)
'''

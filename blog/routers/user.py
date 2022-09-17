from fastapi import APIRouter, Depends
from .. import schemas, database
from sqlalchemy.orm import Session
from ..storage import reuser
from ..oaut2 import get_current_user, check_active, check_admin

router = APIRouter(prefix="/user", tags=["For User"])

get_db = database.get_db


@router.post("/", response_model=schemas.Show_User)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return reuser.ucreate(request, db)


@router.get("/{id}", response_model=schemas.Show_User, dependencies=[Depends(check_active)])
def get_user(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return reuser.ushow(id, db)


@router.put("/giverole/[id]", dependencies=[Depends(check_admin)])
def give_role(id, request: schemas.UserRole, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return reuser.u_get_role(id, request, db)



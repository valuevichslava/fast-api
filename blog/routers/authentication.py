from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .. import database, models, JWToken
from sqlalchemy.orm import Session
from ..hashing import Hash


router = APIRouter(tags=["Authentication"])


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if user.is_banned:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=f"You have got ban!")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Incorrect Password")

    access_token = JWToken.create_access_token(data={"sub": user.email, "adm": user.adm, "moder": user.moder, "writer": user.writer, "ban": user.is_banned})
    return {"access_token": access_token, "token_type": "bearer"}
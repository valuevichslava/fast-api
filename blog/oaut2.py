from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import JWToken, database
from jose import jwt, JWTError
from . import schemas, models, database
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
get_db = database.get_db

# def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     return JWToken.verify_token(token, credentials_exception, db)


def get_current_user(indb: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    print("===enter in get_current_user")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWToken.SECRET_KEY, algorithms=[JWToken.ALGORITHM])
        email: str = payload.get("sub")
        print("==email: " +email)
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
        print("==token_data: "+token_data.email)
    except JWTError:
        raise credentials_exception

    user = models.get_user(username=token_data.email, db=indb)
    if user is None:
        raise credentials_exception
    return user


def check_ban(token: str = Depends(oauth2_scheme)):
    claims = JWToken.decode_token(token)
    if not claims.get("ban"):
        return claims
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You have got ban!", headers={"WWW-Authenticate": "Bearer"})


def check_admin(claims:dict = Depends(check_ban)):
    role = claims.get("adm")
    if not role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Allow only for admins", headers={"WWW-Authenticate": "Bearer"})
    return claims


def check_moder(claims:dict = Depends(check_ban)):
    role = claims.get("moder")
    if not role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Allow only for moderators", headers={"WWW-Authenticate": "Bearer"})
    return claims


def check_writer(claims:dict = Depends(check_ban)):
    role = claims.get("writer")
    if not role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Allow only for writers", headers={"WWW-Authenticate": "Bearer"})
    return claims

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import JWToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return JWToken.verify_token(token, credentials_exception)


def check_active(token: str = Depends(oauth2_scheme)):
    claims = JWToken.decode_token(token)
    if claims.get("active"):
        return claims
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Please activate your account", headers={"WWW-Authenticate": "Bearer"})


def check_admin(claims:dict = Depends(check_active)):
    role = claims.get("role")
    if role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Allow only for admins", headers={"WWW-Authenticate": "Bearer"})
    return claims


def check_moder(claims:dict = Depends(check_active)):
    role = claims.get("role")
    if role != "moderator":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Allow only for moderators", headers={"WWW-Authenticate": "Bearer"})
    return claims


def check_writer(claims:dict = Depends(check_active)):
    role = claims.get("role")
    if role != "writer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Allow only for writers", headers={"WWW-Authenticate": "Bearer"})
    return claims

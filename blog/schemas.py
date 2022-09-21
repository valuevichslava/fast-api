from typing import List, Union
from pydantic import BaseModel, EmailStr
from aenum import Enum


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):

    class Config():
        orm_mode = True


class BlogDrawer(BlogBase):
    status: str = "Drawer"

    class Config():
        orm_mode = True


class Roles(str, Enum):
    user = "user"
    admin = "admin"
    moderator = "moderator"
    writer = "writer"

    class Config():
        orm_mode = True


class UserAdmin(BaseModel):
    password: str
    role: Roles
    is_banned: bool = False


class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    #is_banned: bool = False
    role: Roles

    class Config():
        orm_mode = True


class Show_User(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config():
        orm_mode = True


class Show_Blog(BaseModel):
    title: str
    body: str
    creator: Show_User

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None







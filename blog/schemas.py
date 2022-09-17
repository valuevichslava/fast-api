from typing import List, Union
from pydantic import BaseModel, EmailStr
from aenum import Enum


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BaseModel):
    title: str
    body:  str

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


class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    is_active: bool = True
    role: Roles

    class Config():
        orm_mode = True


class UserRole(BaseModel):
    password: str
    role: Roles


class Show_User(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config():
        orm_mode = True


class Commentator(BaseModel):
    name: str
    email: str

    class Config():
        orm_mode = True


class Comments(BaseModel):
    author: Commentator
    body: str

    class Config():
        orm_mode = True


class Show_Blog(BaseModel):
    title: str
    body: str
    creator: Show_User
    comments: List[Comments] = []

    class Config():
        orm_mode = True


class SingleComment(BaseModel):
    body: str

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







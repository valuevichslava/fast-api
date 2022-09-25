from typing import List, Union
from pydantic import BaseModel, EmailStr
from aenum import Enum


class BlogBase(BaseModel):
    title: str
    body: str


class Blog(BlogBase):

    class Config():
        orm_mode = True


class Roles(BaseModel):
    user: bool = True
    adm: bool = False
    moder: bool = False
    writer: bool = False

    class Config():
        orm_mode = True


class UserAdmin(BaseModel):
    password: str
    #role: Roles
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


class CommentResp(BaseModel):
    id: int
    author_email: str
    content: str
    accepted: bool

    class Config():
        orm_mode = True


class Show_Blog(BaseModel):
    id: int
    title: str
    body: str
    comm: List[CommentResp] = []

    class Config():
        orm_mode = True


class ShowReject(BaseModel):
    title: str
    body: str
    moder_comm: str

    class Config():
        orm_mode = True


class CommentForm(BaseModel):
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







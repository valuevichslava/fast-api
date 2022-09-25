from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Session


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    adm = Column(Boolean)
    moder = Column(Boolean)
    writer = Column(Boolean)
    user = Column(Boolean)
    is_banned = Column(Boolean)


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    drawer = Column(Boolean)
    published = Column(Boolean, default=False)
    accepted = Column(Boolean, default=False)
    rejected = Column(Boolean, default=False)
    moder_comm = Column(String)
    email_id = Column(String)
    comm = relationship("Comment", back_populates="blog")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    content = Column(String)
    blog_id = Column(Integer, ForeignKey("blogs.id"))
    author_email = Column(String)
    accepted = Column(Boolean, default=False)
    consideration = Column(Boolean)
    #rejected = Column(Boolean, default=False)

    blog = relationship("Blog", back_populates="comm")


def get_user(username: str, db: Session):
    return db.query(User).filter(User.email == username).first()

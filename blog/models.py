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

    blogs = relationship("Blog", back_populates="creator")


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
    user_id = Column(Integer, ForeignKey(User.id))

    creator = relationship("User", back_populates="blogs")


def get_user(username: str, db: Session):
    return db.query(User).filter(User.email == username).first()

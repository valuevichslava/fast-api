from .database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship


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
    user_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="blogs")


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
    #roles = relationship("Roles", back_populates="human")

'''
class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)
    user_index = Column(Integer, ForeignKey("users.id"))

    human = relationship("User", back_populates="roles")
'''
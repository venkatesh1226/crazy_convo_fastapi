from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(50), unique=True, index=False)


class Message(Base):
    __tablename__ = "messages"
    msg_id = Column(Integer, primary_key=True, index=True)
    message = Column(String(100), index=False)
    time = Column(String(50), index=False)
    sender_id = Column(Integer, ForeignKey("users.user_id"))
    receiver_id = Column(Integer, ForeignKey("users.user_id"))

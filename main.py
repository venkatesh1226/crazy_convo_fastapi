from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class User(BaseModel):
    user_name: str


class Message(BaseModel):
    message: str
    time: str
    sender_id: int
    receiver_id: int


class Chat(BaseModel):
    sender_id: int
    receiver_id: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: User, db: db_dependency):
    db_user = models.User(user_name=user.user_name)
    db.add(db_user)
    db.commit()


@app.get("/get-msg-list", status_code=status.HTTP_200_OK)
async def get_msg_list(sender_id: int, receiver_id: int, db: db_dependency):
    msg_list = (
        db.query(models.Message)
        .filter(
            (
                (models.Message.sender_id == sender_id)
                & (models.Message.receiver_id == receiver_id)
            )
            | (
                (models.Message.sender_id == receiver_id)
                & (models.Message.receiver_id == sender_id)
            )
        )
        .all()
    )
    return msg_list


@app.post("/send-msg/", status_code=status.HTTP_201_CREATED)
async def send_msg(message: Message, db: db_dependency):
    db_msg = models.Message(
        message=message.message,
        time=message.time,
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
    )
    db.add(db_msg)
    db.commit()
    return db_msg

from datetime import datetime

from sqlalchemy import Column, String, Sequence, Boolean, Integer, Float, DateTime
from db import db
from db.utils import CreatedModel

db.init()


class User(CreatedModel):
    __tablename__ = 'users'
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    chat_id = Column(String(30))
    fullname = Column(String(255))
    username = Column(String(255))

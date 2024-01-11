import json
from sqlalchemy import Column, DateTime, delete as sqlalchemy_delete, update as sqlalchemy_update, Float, func, text
from sqlalchemy.future import select
from db import Base, db
import datetime
import pytz
from sqlalchemy import Column, DateTime
import re


db.init()


class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def set_status_true(cls, database, number):
        query = text(f"UPDATE {database} SET status = :status WHERE contact = :number")
        await db.execute(query, {'status': True, 'number': number})
        await db.commit()

    @classmethod
    async def update(cls, database, column, value, condition_column, condition_value):
        query = text(f"UPDATE {database} SET {column} = :value WHERE {condition_column} = :condition_value")
        await db.execute(query, {'value': value, 'condition_value': condition_value})
        await db.commit()

    @classmethod
    async def update_leave_time(cls, worker_id, w_date, leave_time):
        w_date = datetime.datetime.strptime(w_date, "%Y-%m-%d")
        leave_time = datetime.datetime.strptime(leave_time, "%H:%M:%S")

        database = "daily"
        column_to_update = "leave_time"
        column_to_update_status = "status"
        condition_column1 = "worker_id"
        condition_value1 = worker_id
        condition_column2 = "w_date"
        condition_value2 = w_date

        query = text(
            f"UPDATE {database} "
            f"SET {column_to_update} = :leave_time, {column_to_update_status} = FALSE "
            f"WHERE {condition_column1} = :condition_value1 AND {condition_column2} = :condition_value2"
        )

        await db.execute(
            query,
            {
                "leave_time": leave_time,
                "condition_value1": condition_value1,
                "condition_value2": condition_value2,
            },
        )
        await db.commit()

    async def insert_into(cls, database, column, value):
        query = text(f"INSERT INTO {database} ({column}) VALUES (:column_value)")
        await db.execute(query, {'column_value': value})
        await db.commit()

    @classmethod
    async def insert_into_to_daily(cls, database, w_date, worker_id, come_time, status, late_min):
        query = text(f"INSERT INTO {database} (w_date, worker_id, come_time, status, late_min) VALUES (:w_date, :worker_id, :come_time, :status, :late_min)")
        w_date = datetime.datetime.strptime(w_date, "%Y-%m-%d")
        come_time = datetime.datetime.strptime(come_time, "%H:%M:%S")
        await db.execute(query, {'w_date': w_date, 'worker_id': worker_id, 'come_time': come_time, 'status': status, 'late_min': late_min})
        await db.commit()

    @classmethod
    async def get_phone(cls, database, number):
        query = text(f"SELECT * FROM {database} WHERE contact = :number")
        objects = await db.execute(query, {'number': number})
        return objects.all()

    @classmethod
    async def get_chat_id(cls, database, chat_id):
        query = text(f"SELECT * FROM {database} WHERE chat_id = :chat_id")
        objects = await db.execute(query, {'chat_id': str(chat_id)})
        return objects.all()

    @classmethod
    async def get_all_users(cls, database):
        query = text(f"SELECT * FROM {database}")
        objects = await db.execute(query)
        return objects.all()

    @classmethod
    async def get_by_userID(cls, database, user_id):
        query = text(f"SELECT * FROM {database} WHERE worker_id = :user_id")
        objects = await db.execute(query, {'user_id': user_id})
        return objects.all()

    @classmethod
    async def delete_user(cls, database, condition):
        query = text(f"DELETE * FROM {database} WHERE")
        result = await db.execute(query)
        return result.fetchall()


class CreatedModel(Base, AbstractClass):
    __abstract__ = True
    tz = pytz.timezone('Asia/Tashkent')  # Set the timezone to Uzbekistan's timezone

    created_at = Column(DateTime(timezone=True), default=datetime.datetime.now(tz), server_default="now()")
    updated_at = Column(DateTime(timezone=True), default=datetime.datetime.now(tz), onupdate=datetime.datetime.now(tz),
                        server_default="now()")


async def format_phone_number(phone_number):
    digits = re.sub(r"\D", "", phone_number)
    if len(digits) == 12 and digits.startswith("998"):
        formatted_number = f"+{digits[:3]}({digits[3:5]}) {digits[5:8]}-{digits[8:10]}-{digits[10:]}"
        return formatted_number
    else:
        return "Invalid phone number"


import asyncio
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.ext.asyncio import create_async_engine
import os
from dotenv import load_dotenv

load_dotenv()

# Retrieve database parameters from environment variables
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
dbname = os.getenv("DB_NAME")

connection_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"
engine = create_async_engine(connection_url)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(Session)

Base = declarative_base()
Base.query = db_session.query_property()


class Foo(Base):
    __tablename__ = "foo"
    id = Column(String, primary_key=True)
    name = Column(String)


class Store:
    def __init__(self):
        super().__init__()
        self.connection = None

    async def connect(self):
        self.connection = await engine.begin()
        metadata = MetaData(bind=engine)
        await self.connection.run_sync(metadata.create_all())


async def main():
    store = Store()
    await store.connect()


if __name__ == '__main__':
    asyncio.run(main())

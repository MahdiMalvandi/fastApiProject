from settings.db import base
from sqlalchemy import Column, String, Integer


class User(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True)
    password = Column(String)

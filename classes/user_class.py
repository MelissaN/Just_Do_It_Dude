#!/usr/bin/python3
"""
Class User
"""
from sqlalchemy import Column, String, Date
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash

Base = declarative_base()


class User(Base):
    """Class User is a blueprint to create user objects"""

    __tablename__ = "users"

    first_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, primary_key=True)
    password = Column(String(100), nullable=False)

    def __init__(self, *args, **kwargs):
        """
        instantiates user object
        """
        self.first_name = ""
        self.email = ""
        self.password = ""

        for k, v in kwargs.items():
            if k is 'password':
                User.__set_password(self, k)
            else:
                setattr(self, k, v)

    def __set_password(self, password):
        """
            Encrypts password
        """
        secure_pw = generate_password_hash(password)
        print(secure_pw)
        setattr(self, 'password', secure_pw)

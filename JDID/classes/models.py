#!/usr/bin/python3
"""
Class User
"""
from datetime import date
from JDID import login_user
from sqlalchemy import Column, String, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm.session import object_session


Base = declarative_base()


@login_user.user_loader
def find_user(user):
    from JDID.classes import storage
    return storage.get_user_by_id(user)


class User(Base, UserMixin):
    """Class User is a blueprint to create user objects"""

    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    first_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    # goals = relationship('Goal', backref='users', cascade='delete')

    def __init__(self, *args, **kwargs):
        """
        instantiates user object
        """
        self.first_name = ""
        self.email = ""
        self.password = ""

        for k, v in kwargs.items():
            if k is 'password':
                User.__set_password(self, v)
            else:
                setattr(self, k, v)

    def __set_password(self, password):
        """
            Encrypts password
        """
        secure_pw = generate_password_hash(password)
        setattr(self, 'password', secure_pw)


class Goal(Base):
    """Class Goal is a blueprint to create goal objects"""

    __tablename__ = "goals"

    id = Column(Integer, nullable=False, primary_key=True)
    goal = Column(String(500), nullable=False)
    deadline = Column(Date(), nullable=False)
    accountability_partner = Column(String(255), nullable=False)
    partner_email = Column(String(255), nullable=False)
    pledge = Column(String(500), nullable=False)
    start_date = Column(Date(), nullable=False)
    # start_date = date.today()
    # user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __init__(self, **kwargs):
        """Initialize instance attributes"""
        self.goal = ""
        self.deadline = ""
        self.accountability_partner = ""
        self.partner_email = ""
        self.pledge = ""
        self.start_date = date.today()
        for k, v in kwargs.items():
            setattr(self, k, v)

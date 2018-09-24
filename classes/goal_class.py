#!/usr/bin/python3
"""
Class Goal
"""
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Goal(Base):
    """Class Goal is a blueprint to create goal objects"""

    __tablename__ = "goals"

    goal = Column(String(500), nullable=False)
    deadline = Column(String(255), nullable=False)
    friends_email = Column(String(255), nullable=False)
    pledge = Column(String(500), nullable=False)
    username = Column(String(50), nullable=False, primary_key=True)
    password = Column(String(50))

    def __init__(self, **kwargs):
        """Initialize instance attributes"""
        self.goal = ""
        self.deadline = ""
        self.friends_email = ""
        self.pledge = ""
        self.username = ""
        self.password = ""
        for k, v in kwargs.items():
            setattr(self, k, v)

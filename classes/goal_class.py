#!/usr/bin/python3
"""
Class Goal
"""
from sqlalchemy import Column, String, Date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Goal(Base):
    """Class Goal is a blueprint to create goal objects"""

    __tablename__ = "goals"

    goal = Column(String(500), nullable=False, primary_key=True)
    deadline = Column(Date(), nullable=False)
    accountability_partner = Column(String(255), nullable=False)
    partner_email = Column(String(255), nullable=False)
    pledge = Column(String(500), nullable=False)

    def __init__(self, **kwargs):
        """Initialize instance attributes"""
        self.goal = ""
        self.deadline = ""
        self.accountability_partner = ""
        self.partner_email = ""
        self.pledge = ""
        for k, v in kwargs.items():
            setattr(self, k, v)

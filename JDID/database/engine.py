#!/usr/bin/python3
"""
DATABASE ENGINE FOR STORAGE
"""
from JDID.classes.models import Goal, User
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
Base = declarative_base()


class DBStorage():
    """
       database engine to store urls
    """
    __engine = None
    __session = None

    def __init__(self):
        """
           create engine and link to database
        """
        user = "root"
        pw = ""
        host = "localhost"
        db = "justdoitdude_dev_db"
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pw, host, db), pool_pre_ping=True)
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def save(self, obj):
        """
           create new obj and save entry to db
        """
        try:
            self.__session.add(obj)
            self.__session.commit()
        except:
            self.__session.rollback()

    def all(self):
        """
           return all entries in db
        """
        goal_dic = {}
        for obj in self.__session.query(Goal).all():
            key = obj.id
            goal_dic[key] = obj
        return goal_dic

    def get(self, username):
        """
           return goal if username given
        """
        try:
            obj = self.__session.query(Goal).get(username)
            return obj.goal
        except (IndexError, TypeError):
            return ""

    def get_user_by_email(self, email):
        """
            return user info
        """
        try:
            obj = self.__session.query(User).filter_by(email=email).first()
            return obj
        except TypeError:
            print('Error at engine.get_user_by_email X____X')
            return None

    def get_user_by_id(self, user_id):
        """
            return user info
        """
        try:
            obj = self.__session.query(User).filter_by(id=user_id).first()
            return obj
        except TypeError:
            print('Error at engine.get_user_by_id X____X')
            return None

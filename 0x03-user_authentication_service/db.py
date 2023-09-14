#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the database
        args:
            email - email value of user
            hashed_password - password value of user
        """
        user1 = User(email=email, hashed_password=hashed_password)
        self._session.add(user1)
        self._session.commit()
        return user1

    def find_user_by(self, **search_by):
        """
        Filters a new user according to search_by keyword"""
        if not search_by:
            raise InvalidRequestError
        result = self._session.query(User).filter_by(**search_by).first()
        if not result:
            raise NoResultFound
        return result

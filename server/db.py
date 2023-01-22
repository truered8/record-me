import os
from typing import Callable
from dotenv import load_dotenv
from sqlalchemy import create_engine, update
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from models import *


class CockroachService:
    @staticmethod
    def connect(callback: Callable[[Engine], None]) -> None:
        """Connects to the database."""
        engine = create_engine(os.getenv("DATABASE_URL"), connect_args={'sslmode': 'verify-ca'})
        Base.metadata.create_all(engine)
        print("Connected to database.")
        callback(engine)

    @staticmethod
    def get_user(session: Session, user_id: str) -> User:
        """Returns the reviews for the given product."""
        return session.query(User).filter_by(id=user_id).first()

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> User:
        """Returns the reviews for the given product."""
        return session.query(User).filter_by(email=email).first()
    
    @staticmethod
    def get_users(session: Session, group_id: str) -> "list[User]":
        """Returns the users in a given group."""
        return session.query(User).filter_by(group_id=group_id).all()

    @staticmethod
    def get_group(session: Session, group_id: str) -> Group:
        """Returns the reviews for the given product."""
        return session.query(Group).filter_by(id=group_id).first()

    @staticmethod
    def get_groups(session: Session) -> "list[Group]":
        """Returns the reviews for the given product."""
        return session.query(Group).all()


load_dotenv()

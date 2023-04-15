import os
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DB_URI = os.environ.get("DATABASE_URI")

engine = create_engine(DB_URI, pool_pre_ping=True)


@lru_cache
def create_session():
    Session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    return Session


def get_session():
    Session = create_session()
    try:
        yield Session
    finally:
        Session.remove()

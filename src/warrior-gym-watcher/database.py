from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base

SQLALCHEMY_DB_URL = "sqlite:///./ticket_tracker.db"

engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    # create physical tables in the .db file
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

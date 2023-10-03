from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from .config import settings

hostname = settings.database_hostname
port = settings.database_port
database_name = settings.database_name
user = settings.user_db
password = settings.password_db


SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@{hostname}:{port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base( )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
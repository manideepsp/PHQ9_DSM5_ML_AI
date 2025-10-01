# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/postgres')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def init_db(app):
    # Import all models here so Base.metadata.create_all works
    from .models import User, PHQ9Assessment, DSM5Assessment
    Base.metadata.create_all(bind=engine)

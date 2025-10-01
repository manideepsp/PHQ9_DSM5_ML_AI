# app/models.py
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from .db import Base

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    emailid = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    profession = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PHQ9Assessment(Base):
    __tablename__ = 'phq9_assessment'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'))
    responses = Column(JSON)
    total_score = Column(Integer)
    doctors_notes = Column(String)
    patients_notes = Column(String)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

class DSM5Assessment(Base):
    __tablename__ = 'dsm_5_assessment'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'))
    severity = Column(String(50), nullable=False)
    q9_flag = Column(String(5), nullable=False)
    mdd_assessment = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

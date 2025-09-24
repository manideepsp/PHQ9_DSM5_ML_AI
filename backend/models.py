from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy import Integer, ForeignKey, JSON, DateTime
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    emailid = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    age = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    profession = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PHQ9Assessment(Base):
    __tablename__ = 'phq9_assessment'
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.user_id', ondelete='CASCADE'))
    responses = Column(JSON)
    total_score = Column(Integer)
    doctors_notes = Column(String)
    patients_notes = Column(String)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())

# DSM-5 Assessment table
class DSM5Assessment(Base):
    __tablename__ = 'dsm_5_assessment'
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.user_id', ondelete='CASCADE'))
    severity = Column(String(50), nullable=False)
    q9_flag = Column(String(5), nullable=False)  # Store as 'true'/'false' string or use Boolean if preferred
    mdd_assessment = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

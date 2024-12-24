from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from app.db.config_sql import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(5), nullable=True)
    birth_year = Column(Integer, nullable=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hash_password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=func.now())

    # Relationships
    interview_scripts = relationship("InterviewScript", back_populates="user")
    interview_sessions = relationship("InterviewSession", back_populates="user")


class InterviewScript(Base):
    __tablename__ = "interview_script"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill = Column(String(100), nullable=False)
    industry = Column(String(100), nullable=False)
    experience = Column(String(50), nullable=False)
    target_position = Column(String(100), nullable=False)
    JD_file = Column(String(255), nullable=True)
    CV_file = Column(String(255), nullable=True)
    script = Column(Text, nullable=True)

    # Relationship
    user = relationship("User", back_populates="interview_scripts")


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=func.now())
    conversation = Column(JSON, nullable=True)  # Dùng JSONB nếu PostgreSQL
    feedback = Column(JSON, nullable=True)  # Dùng JSONB nếu PostgreSQL

    # Relationship
    user = relationship("User", back_populates="interview_sessions")


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Created all tables successfully!")

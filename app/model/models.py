from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from app.db.config_sql import engine

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    industry = Column(String(100))
    experience = Column(String(50))
    target_position = Column(String(100))
    created_at = Column(DateTime, default=func.now())

    # Relationships
    skills = relationship("UserSkill", back_populates="user")
    interviews = relationship("InterviewSession", back_populates="user")


class UserSkill(Base):
    __tablename__ = "user_skills"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    skill = Column(String(100), nullable=False)

    # Relationship
    user = relationship("User", back_populates="skills")


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    position = Column(String(100))
    date = Column(DateTime, default=func.now())
    conversation = Column(JSON)  # hoặc Column(JSONB) nếu dùng PostgreSQL
    overall_score = Column(DECIMAL(3, 2))
    overall_feedback = Column(JSON)  # hoặc Column(JSONB) nếu dùng PostgreSQL
    status = Column(String(20))

    # Relationship
    user = relationship("User", back_populates="interviews")


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Created all tables successfully!")

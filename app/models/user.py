from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    wallet = Column(String, unique=True, index=True)
    chat_id = Column(Integer, unique=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    is_welcomed = Column(Boolean, default=False)
    is_onboarded = Column(Boolean, default=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

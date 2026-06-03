from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import os

# Use PostgreSQL if DATABASE_URL is set, else default to SQLite (for local testing without docker)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./farms.db")

connect_args = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="farmer") # "farmer", "authority", "admin"

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    farmer_name = Column(String, index=True, nullable=False)
    farm_size = Column(Float, nullable=False)
    crop_type = Column(String, nullable=False)
    tree_count = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)


# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

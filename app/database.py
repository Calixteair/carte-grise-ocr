from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# Base class for declarative models
Base = declarative_base()

# Function to get a configured engine and session for a given database URL
def get_engine(database_url: str):
    return create_engine(database_url)

def get_session_local(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Global variables for the application's engine and session, to be initialized once
# in the application startup.
# In tests, these will be overridden.
engine = get_engine(settings.DATABASE_URL)
SessionLocal = get_session_local(engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

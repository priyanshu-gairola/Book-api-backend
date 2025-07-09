#CONNECTING SQLite database

# Import the necessary function to create a connection to the database
from sqlalchemy import create_engine

# Import the base class for creating ORM models
from sqlalchemy.orm import declarative_base

# Import sessionmaker to create DB sessions (used for interacting with DB)
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL=os.getenv("SQLALCHEMY_DATABASE_URL")
# Create the database engine that will handle connections
# connect_args is required for SQLite to allow multi-thread access
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create a SessionLocal class which we will use to create session objects
# autocommit=False: changes won't be saved unless we explicitly commit
# autoflush=False: don't automatically push changes to DB until commit
# bind=engine: use the engine we just created
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class that our models (e.g., Book, User) will inherit from
# All tables in DB are created from classes that inherit from this Base
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

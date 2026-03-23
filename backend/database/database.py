from backend.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.schema import Base, UsertableSchema

POSTGRES_USER = settings.POSTGRES_USER
POSTGRES_PASSWORD = settings.POSTGRES_PASSWORD
POSTGRES_SERVER = settings.POSTGRES_SERVER
POSTGRES_PORT = settings.POSTGRES_PORT
POSTGRES_DB = settings.POSTGRES_DB

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Create a helper function for DB connection

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base.metadata.create_all(bind=engine)

def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

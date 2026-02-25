from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from backend.database.schema import Base, UsertableSchema
# Creating a database connection URL
load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

POSTGRES_DB = os.getenv("POSTGRES_DB", "testdb")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
print(DATABASE_URL)

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

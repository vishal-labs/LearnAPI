from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from sqlalchemy import text

Base = declarative_base()

class UsertableSchema(Base):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False, unique=False)
    isAdmin = db.Column(db.Boolean, nullable=False,server_default=text('false'))
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from sqlalchemy import text
from sqlalchemy.orm import relationship

Base = declarative_base()

class UsertableSchema(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False, unique=False)
    isAdmin = db.Column(db.Boolean, nullable=False,server_default=text('false'))

from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID  # for PostgreSQL
import uuid

class PaymentHistorySchema(Base):
    __tablename__ = 'paymenthistory'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    from_userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    to_userid = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    transactionid = db.Column(UUID(as_uuid=True), nullable=False, unique=True, default=lambda: uuid.uuid4())  # AUTO-GENERATED
    transactionamt = db.Column(db.Numeric(15, 2), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False, server_default=text('NOW()'))
    ipaddress = db.Column(db.String, nullable=True)
    
    # ENUM constraint - only allows: transfer, deposit, withdrawal
    type = db.Column(db.Enum('transfer', 'deposit', 'withdrawal', name='txn_type'), 
                     nullable=False, server_default='transfer')

    from_user = relationship('UsertableSchema', foreign_keys=[from_userid])
    to_user = relationship('UsertableSchema', foreign_keys=[to_userid])


class UserAccountBalanceSchema(Base):
    __tablename__ = 'useraccountbalance'

    userid = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    accountbalance = db.Column(db.Numeric(15, 2), nullable=False, server_default=text('0'))
    lastupdated = db.Column(db.TIMESTAMP, nullable=False, server_default=text('NOW()'))

    user = relationship('UsertableSchema', foreign_keys=[userid])


import jwt
import datetime
from datetime import timezone, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from backend.database.database import getDB
from sqlalchemy.orm import Session
from backend.database.schema import UsertableSchema
from backend.config import settings

key = settings.KEY
refresh_key = settings.REFRESH_KEY
tokenExpirationMinutes = 4
refreshTokenExpirationDays = 7

def createToken(email: str) -> str:
    expire = datetime.datetime.now(timezone.utc) + timedelta(minutes=tokenExpirationMinutes)
    payload = {
        "email" : email, 
        "exp" : expire
    }
    encoded = jwt.encode(payload=payload, key=key, algorithm="HS256")
    return encoded

def createRefreshToken(email: str) -> str:
    expire = datetime.datetime.now(timezone.utc) + timedelta(days=refreshTokenExpirationDays)
    payload = {
        "email": email,
        "exp": expire,
        "type": "refresh"
    }
    encoded = jwt.encode(payload=payload, key=refresh_key, algorithm="HS256")
    return encoded

def createPasswordResetToken(email: str) -> str:
    expire = datetime.datetime.now(timezone.utc) + timedelta(minutes=15)
    payload = {
        "email": email,
        "exp": expire,
        "type": "reset"
    }
    encoded = jwt.encode(payload=payload, key=key, algorithm="HS256")
    return encoded

def validateUserSession(token: str):
    jwt.decode(token, key=key, algorithms=["HS256"])

security = HTTPBearer()

def RequireAuth(creds: HTTPAuthorizationCredentials = Depends(security)) -> str:
    # returns the decoded email
    validateUserSession(creds.credentials)
    decoded = jwt.decode(creds.credentials, key=key, algorithms=["HS256"])
    return decoded["email"]
        
def validateAdminStatus(token: str, db: Session):
    validateUserSession(token)
    decoded = jwt.decode(token, key=key, algorithms=["HS256"])
    email = decoded["email"]
    checkAdminStatus  = db.query(UsertableSchema).filter(UsertableSchema.email == email).first().isAdmin
    if checkAdminStatus:
        return True
    else:
        return False

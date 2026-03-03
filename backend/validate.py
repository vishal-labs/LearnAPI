import jwt
import os
import datetime
from datetime import timezone, timedelta
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from backend.database.database import getDB
from sqlalchemy.orm import Session
from backend.database.schema import UsertableSchema

load_dotenv()

key = os.getenv("KEY")
tokenExpirationMinutes = 4

def createToken(email: str) -> str:
    expire = datetime.datetime.now(timezone.utc) + timedelta(minutes=tokenExpirationMinutes)
    payload = {
        "email" : email, 
        "exp" : expire
    }
    encoded = jwt.encode(payload=payload, key=key, algorithm="HS256")
    return encoded

def validateUserSession(token: str):
    try:
        jwt.decode(token, key=key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session Expired, Login Again")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid User authentication")   

        
def validateAdminStatus(token: str, db: Session):
    try:
        validateUserSession(token)
    except HTTPException as e:
        raise e
    decoded = jwt.decode(token, key=key, algorithms=["HS256"])
    email = decoded["email"]
    checkAdminStatus  = db.query(UsertableSchema).filter(UsertableSchema.email == email).first().isAdmin
    if checkAdminStatus:
        return True
    else:
        return False

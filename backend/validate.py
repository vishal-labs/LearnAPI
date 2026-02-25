import jwt
import os
import datetime
from datetime import timezone, timedelta
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

key = os.getenv("KEY")
tokenExpirationMinutes = 1

def createToken(username: str) -> str:
    expire = datetime.datetime.now(timezone.utc) + timedelta(minutes=tokenExpirationMinutes)
    payload = {
        "user" : username, 
        "exp" : expire
    }
    encoded = jwt.encode(payload=payload, key=key, algorithm="HS256")
    return encoded

def validateUserSession(token: str):
    try:
        jwt.decode(token, key=key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Session Expired, Login Again")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid User authentication")   

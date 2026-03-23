# This file is for user signup and signin
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from backend.database.database import getDB
from sqlalchemy.orm import Session
from backend.models import loginUser, onBoardUser
from backend.database.schema import UserAccountBalanceSchema, UsertableSchema, PaymentHistorySchema
from backend.auth.validate import validateUserSession, createToken
from prometheus_client import Counter, Gauge, Histogram
from passlib.context import CryptContext
from passlib.hash import pbkdf2_sha256

router = APIRouter()
security = HTTPBearer()

loginCounter = Counter(
    "app_logins_total",
    "total Login attempts",
    ["status"]
)
active_users = Gauge(
    "app_active_users",
    "Number of currently active users"
)

db_query_duration = Histogram(
    "app_db_query_duration_seconds",
    "Time spent on database queries",
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]  # custom buckets
)


@router.post('/auth/login')
async def loginUser(user: loginUser,db: Session = Depends(getDB)):
# Aim of this function is to verify if the user already exists, and if yes, return a bearer token meaning, logging him in
    # Verify if the user exists
    user_record = db.query(UsertableSchema).filter(UsertableSchema.email == user.email).first()
    #print(user_record.password)
    if user_record == None:
        raise HTTPException(status_code=404, detail="User not found")
    # verify password:
    
    if pbkdf2_sha256.verify( user.password, user_record.password): # verify(enteredpass, db_stored_hash )
        token = createToken(user.email)
        payload = {
            "token" : token,
            "token_type" : "bearer",
            "msg" : "User created"
        }
        loginCounter.labels(status="success").inc()
        return payload
    else:
        loginCounter.labels(status="failure").inc()
        raise HTTPException(status_code=401, detail="invalid login credentials")

@router.post("/auth/signup")
async def OnBoardUser(
    user: onBoardUser, 
    db: Session = Depends(getDB)
):
    #check if the user already exists
    checkEmail = db.query(UsertableSchema).filter(UsertableSchema.email == user.email).first()
    if checkEmail != None:
        raise HTTPException(status_code=409, detail="User already exists")
    else:
        #hashed_password = pwd_context.hash(user.password)
        hashed_password = pbkdf2_sha256.hash(user.password)
        newUser = UsertableSchema(email = user.email, password = hashed_password, username = user.username)
        
        db.add(newUser)
        db.flush()
        newUserforAccount = UserAccountBalanceSchema(userid = newUser.id)
        db.add(newUserforAccount)
        db.commit()
        return {"msg" : "Account created"}

@router.get("/auth/me")
async def me(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    validateUserSession(token)
    return {"msg" : "User is valid"}

# This file is for user signup and signin
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from backend.database.database import getDB
from sqlalchemy.orm import Session
from backend.models import loginUser, onBoardUser
from backend.database.schema import UsertableSchema
from backend.validate import validateUserSession, createToken

router = APIRouter()
security = HTTPBearer()



@router.post('/auth/login')
async def loginUser(user: loginUser,db: Session = Depends(getDB)):
# Aim of this function is to verify if the user already exists, and if yes, return a bearer token meaning, logging him in
    # Verify if the user exists
    userPassword = db.query(UsertableSchema).filter(UsertableSchema.email == user.email).first()
    #print(userPassword.password)
    if userPassword == None:
        raise HTTPException(status_code=404, detail="User not found")
    if userPassword.password == user.password:
        token = createToken(user.email)
        payload = {
            "token" : token,
            "token_type" : "bearer",
            "msg" : "User created"
        }
        return payload
    else:
        raise HTTPException(status_code=404, detail="invalid login credentials")

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
        newUser = UsertableSchema(email = user.email, password = user.password, username = user.username)
        db.add(newUser)
        db.commit()
        db.refresh(newUser)
        return {"msg" : "User created"}

@router.get("/auth/me")
async def me(creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    validateUserSession(token)
    return {"msg" : "User is valid"}

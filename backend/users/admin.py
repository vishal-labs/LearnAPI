from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database.schema import UsertableSchema
from backend.database.database import getDB
from backend.auth.validate import validateAdminStatus
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from dotenv import load_dotenv
from backend.models import makeUserAdmin
from backend.database.schema import UsertableSchema

load_dotenv()
adminKey = os.getenv("ADMINKEY")


security = HTTPBearer()

router = APIRouter()
@router.get("/admin/users")
async def getAllUsers(db: Session = Depends(getDB), creds : HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    if validateAdminStatus(token, db):
        users = db.query(UsertableSchema).all()
        return users
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")
@router.post("/admin/promote")
async def updateAdminStatus(
    user: makeUserAdmin, 
    db: Session = Depends(getDB)
):
    if user.adminKey == adminKey:
        user_record = db.query(UsertableSchema).filter(UsertableSchema.email == user.email).first()
        if user_record.email != None:
            user_record.isAdmin = True
            db.commit()
            db.refresh(user_record)
        else:
            raise HTTPException(status_code=404, detail="User doesn't exist")
    elif user.adminKey != adminKey:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid admin key")
    return {"message": "User promoted to admin", "email": user_record.email}
            





from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.schema import UsertableSchema
from backend.database.database import getDB
from backend.validate import validateAdminStatus
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

router = APIRouter()
@router.get("/admin/users")
async def getAllUsers(db: Session = Depends(getDB), creds : HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    if validateAdminStatus(token, db):
        users = db.query(UsertableSchema).all()
        return users
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

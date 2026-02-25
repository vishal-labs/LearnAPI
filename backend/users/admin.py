from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database.schema import UsertableSchema
from backend.database.database import getDB

router = APIRouter()
@router.get("/admin/users")
async def getAllUsers(db: Session = Depends(getDB)):
    users = db.query(UsertableSchema).all()
    return users

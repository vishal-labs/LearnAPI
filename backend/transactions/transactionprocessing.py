from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone
from backend.database.database import getDB
from sqlalchemy.orm import Session
from backend.models import * 
from backend.database.schema import * 

router = APIRouter()

@router.post("/user/balance")
async def get_user_balance(
    user: onlyEmail,
    db: Session = Depends(getDB)
):
    try:
        user_record = db.query(UsertableSchema).filter(UsertableSchema.email == user.email).first()
        user_balance = db.query(UserAccountBalanceSchema).filter(UserAccountBalanceSchema.userid == user_record.id).order_by(UserAccountBalanceSchema.lastupdated).first()
        payload = {
            "user" : user_record.username,
            "email" : user_record.email,
            "accountBalance" : user_balance.accountbalance
        }
        return payload
    except:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not found")

@router.post("/user/deposit")
async def deposit_user_amount(
    user: transactionDeposit,
    db: Session = Depends(getDB)
):
    try:
        user_record = db.query(UsertableSchema).filter(UsertableSchema.email == user.toUserEmail).first() # get user details
        user_balance = db.query(UserAccountBalanceSchema).filter(UserAccountBalanceSchema.userid == user_record.id).first()
        user_balance.accountbalance += user.transactionAmount
        user_balance.lastupdated = datetime.now(timezone.utc)
        payment_record = PaymentHistorySchema(
            to_userid=user_record.id,
            transactionamt=user.transactionAmount,
            type='deposit'
        )
        db.add(payment_record)
        db.commit()
        db.refresh(user_record)
        payload = {
            "userEmail" : user_record.email,
            "DepositedAmt" : user.transactionAmount,
            "depositStatus" : "Deposited.."
        }
        return payload
    except:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not found")
    

@router.post("/user/withdrawal")
async def withdraw_user_amount(
    user: transactionWithdrawal,
    db: Session = Depends(getDB)
):
    try:
        user_record = db.query(UsertableSchema).filter(UsertableSchema.email == user.fromUserEmail).first() # get user details
        user_balance = db.query(UserAccountBalanceSchema).filter(UserAccountBalanceSchema.userid == user_record.id).first()
        user_balance.accountbalance -= user.transactionAmount
        user_balance.lastupdated = datetime.now(timezone.utc)
        payment_record = PaymentHistorySchema(
            from_userid=user_record.id,
            transactionamt=user.transactionAmount,
            type='withdrawal'
        )
        db.add(payment_record)
        db.commit()
        db.refresh(user_record)
        payload = {
            "userEmail" : user_record.email,
            "DepositedAmt" : user.transactionAmount,
            "depositStatus" : "Withdrawed.."
        }
        return payload
    except:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not found")

@router.post("/user/send")
async def send_user_amount(
    user: transactionTransfer,
    db: Session = Depends(getDB)
):
    try:
        from_user = db.query(UsertableSchema).filter(UsertableSchema.email == user.fromUserEmail).first()
        to_user = db.query(UsertableSchema).filter(UsertableSchema.email == user.toUserEmail).first()
        
        if not from_user or not to_user:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not found")
            
        from_balance = db.query(UserAccountBalanceSchema).filter(UserAccountBalanceSchema.userid == from_user.id).first()
        to_balance = db.query(UserAccountBalanceSchema).filter(UserAccountBalanceSchema.userid == to_user.id).first()
        
        if from_balance.accountbalance < user.transactionAmount:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")

        from_balance.accountbalance -= user.transactionAmount
        to_balance.accountbalance += user.transactionAmount
        
        from_balance.lastupdated = datetime.now(timezone.utc)
        to_balance.lastupdated = datetime.now(timezone.utc)
        
        payment_record = PaymentHistorySchema(
            from_userid=from_user.id,
            to_userid=to_user.id,
            transactionamt=user.transactionAmount,
            type='transfer'
        )
        db.add(payment_record)
        db.commit()
        db.refresh(from_user)
        
        payload = {
            "fromUserEmail" : from_user.email,
            "toUserEmail" : to_user.email,
            "TransferredAmt" : user.transactionAmount,
            "transferStatus" : "Transferred.."
        }
        return payload
    except Exception as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

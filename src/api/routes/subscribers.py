from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.core.database import get_db
from src.models.subscriber import Subscriber
import json

router = APIRouter()

@router.post("/subscribe")
async def subscribe(email: str, db: Session = Depends(get_db)):
    # 이메일 형식 검증
    if not "@" in email or not "." in email:
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # 이미 구독 중인지 확인
    existing = db.query(Subscriber).filter(Subscriber.email == email).first()
    if existing:
        if not existing.is_active:
            existing.is_active = True
            db.add(existing)
            db.commit()
            return {"message": "Subscription reactivated"}
        raise HTTPException(status_code=400, detail="Email already subscribed")
    
    # 새 구독자 추가
    subscriber = Subscriber(email=email)
    db.add(subscriber)
    db.commit()
    return {"message": "Successfully subscribed"}

@router.post("/unsubscribe")
async def unsubscribe(email: str, db: Session = Depends(get_db)):
    subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    
    subscriber.is_active = False
    db.add(subscriber)
    db.commit()
    return {"message": "Successfully unsubscribed"}

@router.get("/subscribers")
async def get_subscribers(db: Session = Depends(get_db)):
    subscribers = db.query(Subscriber).filter(Subscriber.is_active == True).all()
    return [{"email": s.email, "created_at": s.created_at} for s in subscribers]

@router.put("/preferences/{email}")
async def update_preferences(
    email: str,
    preferences: dict,
    db: Session = Depends(get_db)
):
    subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    
    subscriber.preferences = json.dumps(preferences)
    db.add(subscriber)
    db.commit()
    return {"message": "Preferences updated successfully"} 
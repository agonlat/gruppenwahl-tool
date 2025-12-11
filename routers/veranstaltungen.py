from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import Veranstaltung, get_db
from datetime import datetime

router = APIRouter()

@router.post("/")
def create_event(titel: str, start: datetime, ende: datetime, db: Session = Depends(get_db)):
    v = Veranstaltung(titel=titel, start=start, ende=ende)
    db.add(v)
    db.commit()
    db.refresh(v)
    return v

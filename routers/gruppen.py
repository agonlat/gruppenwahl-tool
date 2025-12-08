# gruppen.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

# Import DB setup and SQLAlchemy models from the new file
from database import Gruppe, GruppeAnmeldung, Student, SessionLocal 

router = APIRouter()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{gruppe_id}/anmelden/{student_id}")
def anmelden(gruppe_id: int, student_id: int, db: Session = Depends(get_db)):
    gruppe = db.query(Gruppe).filter(Gruppe.id == gruppe_id).first()
    
    if not gruppe:
        raise HTTPException(status_code=404, detail="Gruppe not found")
        
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Check for existing Anmeldung
    existing_anmeldung = db.query(GruppeAnmeldung).filter(
        GruppeAnmeldung.gruppe_id == gruppe_id, 
        GruppeAnmeldung.student_id == student_id
    ).first()
    
    if existing_anmeldung:
        return {"message": f"Student {student_id} is already on the {existing_anmeldung.status} list for Gruppe {gruppe_id}."}

    # Count currently registered students
    angemeldet_count = db.query(GruppeAnmeldung).filter(
        GruppeAnmeldung.gruppe_id == gruppe_id, 
        GruppeAnmeldung.status == "angemeldet"
    ).count()

    # Determine status
    status = "angemeldet" if angemeldet_count < gruppe.max_teilnehmer else "warteliste"
    
    # Create new Anmeldung
    anmeld = GruppeAnmeldung(
        gruppe_id=gruppe_id, 
        student_id=student_id, 
        status=status,
        created_at=datetime.now() # Add timestamp
    )
    db.add(anmeld)
    db.commit()
    
    return {"message": f"Student {student_id} wurde {status}."}
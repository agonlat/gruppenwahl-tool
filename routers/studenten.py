# fileName: routers/studenten.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Korrekter Import der Modelle aus dem Hauptverzeichnis
from database import get_db
from models import Student

router = APIRouter()


class StudentCreate(BaseModel):
    name: str
    matrikelnummer: str
    studiengang: str
    semester: int
    email: str


@router.post("/register")
def register_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Registriert einen Studenten oder loggt ihn per Matrikelnummer ein."""
    existing = db.query(Student).filter_by(
        matrikelnummer=student.matrikelnummer
    ).first()

    if existing:
        # Update der Daten falls vorhanden (funktioniert als Login/Update)
        existing.name = student.name
        existing.studiengang = student.studiengang
        existing.semester = student.semester
        existing.email = student.email
        db.commit()
        db.refresh(existing)
        return {
            "message": "Student erfolgreich angemeldet und Daten aktualisiert.",
            "student_id": existing.id,
            "student_name": existing.name
        }

    # Neu registrieren
    s = Student(**student.dict())
    db.add(s)
    db.commit()
    db.refresh(s)

    return {
        "message": "Registrierung erfolgreich.",
        "student_id": s.id,
        "student_name": s.name
    }
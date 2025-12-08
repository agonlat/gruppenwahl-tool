# studenten.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

# Import DB setup and SQLAlchemy models from the new file
from database import Student, SessionLocal 
# Import Pydantic schemas from models.py
from models import StudentCreate 

router = APIRouter()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# The POST route now uses the Pydantic model for validation
@router.post("/register")
def register_student(student: StudentCreate, db: Session = Depends(get_db)):
    # 1. Check if student already exists (using unique matrikelnummer)
    existing_student = db.query(Student).filter(Student.matrikelnummer == student.matrikelnummer).first()
    if existing_student:
        return {"message": f"Student with Matrikelnummer {student.matrikelnummer} is already registered!"}

    # 2. Create the SQLAlchemy model instance from Pydantic data
    db_student = Student(
        name=student.name,
        matrikelnummer=student.matrikelnummer,
        studiengang=student.studiengang,
        semester=student.semester,
        email=student.email
    )
    
    # 3. Add to DB and commit
    db.add(db_student)
    db.commit()
    db.refresh(db_student) # To get the generated 'id'

    return {"message": f"Student {student.name} registriert!", "student_id": db_student.id}
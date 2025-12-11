from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import Student, get_db
from models import StudentCreate

router = APIRouter()

@router.post("/register")
def register_student(student: StudentCreate, db: Session = Depends(get_db)):
    existing = db.query(Student).filter(Student.matrikelnummer == student.matrikelnummer).first()

    if existing:
        return {
            "message": f"Student {existing.name} ist bereits registriert.",
            "student_id": existing.id,
            "student_name": existing.name
        }

    new_student = Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": f"Student {new_student.name} wurde registriert.",
        "student_id": new_student.id,
        "student_name": new_student.name
    }

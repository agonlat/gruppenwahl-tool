# fileName: routers/studenten.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Student
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------- Hilfsfunktionen ----------
def hash_password(password: str):
    return pwd_context.hash(password[:72])

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password[:72], hashed_password)


# ---------- Pydantic-Modelle ----------
class StudentBase(BaseModel):
    name: str
    studiengang: str
    semester: int
    email: EmailStr


class StudentRegister(StudentBase):
    matrikelnummer: str
    password: str
    password_repeat: str


class StudentLogin(BaseModel):
    matrikelnummer: str
    password: str


# ---------- Registrierung ----------
@router.post("/register")
def register_student(student_data: StudentRegister, db: Session = Depends(get_db)):

    if student_data.password != student_data.password_repeat:
        raise HTTPException(status_code=400, detail="Passwörter stimmen nicht überein.")

    if len(student_data.password) < 8:
        raise HTTPException(status_code=400, detail="Passwort muss mindestens 8 Zeichen lang sein.")

    existing = db.query(Student).filter(
        (Student.matrikelnummer == student_data.matrikelnummer) |
        (Student.email == student_data.email)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Matrikelnummer oder E-Mail existiert bereits.")

    hashed_pw = hash_password(student_data.password)

    student = Student(
        name=student_data.name,
        matrikelnummer=student_data.matrikelnummer,
        studiengang=student_data.studiengang,
        semester=student_data.semester,
        email=student_data.email,
        hashed_password=hashed_pw
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    # Rückgabe mit Matrikelnummer für sofortigen Login
    return {
        "message": "Registrierung erfolgreich.",
        "student_id": student.id,
        "student_name": student.name,
        "matrikelnummer": student.matrikelnummer 
    }


# ---------- Login ----------
@router.post("/login")
def login_student(login_data: StudentLogin, db: Session = Depends(get_db)):

    student = db.query(Student).filter_by(
        matrikelnummer=login_data.matrikelnummer
    ).first()

    if not student or not verify_password(login_data.password, student.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Matrikelnummer oder Passwort ungültig."
        )

    return {
        "message": "Login erfolgreich.",
        "student_id": student.id,
        "student_name": student.name,
        "matrikelnummer": student.matrikelnummer 
    }
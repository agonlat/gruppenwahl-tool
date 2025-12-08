# models.py
from pydantic import BaseModel
# Remove: from models import Student, SessionLocal (this caused the error)

# Pydantic Schema for Student registration input
class StudentCreate(BaseModel):
    name: str
    matrikelnummer: str
    studiengang: str
    semester: int
    email: str

# You can add other Pydantic schemas here (e.g., GruppeBase, GruppeRead, etc.)

# NOTE: The database connection setup and SQLAlchemy models are moved to database.py
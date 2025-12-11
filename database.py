from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# =======================
# MODELS
# =======================

class Veranstaltung(Base):
    __tablename__ = "veranstaltungen"

    id = Column(Integer, primary_key=True)
    titel = Column(String)
    start = Column(DateTime)
    ende = Column(DateTime)

    gruppen = relationship("Gruppe", back_populates="veranstaltung")


class Gruppe(Base):
    __tablename__ = "gruppen"

    id = Column(Integer, primary_key=True)
    veranstaltung_id = Column(Integer, ForeignKey("veranstaltungen.id"))
    name = Column(String)
    max_teilnehmer = Column(Integer)

    veranstaltung = relationship("Veranstaltung", back_populates="gruppen")
    anmeldungen = relationship("GruppeAnmeldung", back_populates="gruppe")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    matrikelnummer = Column(String, unique=True)
    studiengang = Column(String)
    semester = Column(Integer)
    email = Column(String)

    anmeldungen = relationship("GruppeAnmeldung", back_populates="student")


class GruppeAnmeldung(Base):
    __tablename__ = "gruppe_anmeldungen"

    id = Column(Integer, primary_key=True)
    gruppe_id = Column(Integer, ForeignKey("gruppen.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    status = Column(String)
    created_at = Column(DateTime)

    gruppe = relationship("Gruppe", back_populates="anmeldungen")
    student = relationship("Student", back_populates="anmeldungen")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

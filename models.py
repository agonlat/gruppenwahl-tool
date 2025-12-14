# fileName: models.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base # Importiert Base von database.py

class Student(Base):
    __tablename__ = "studenten"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    matrikelnummer = Column(String, unique=True, index=True)
    studiengang = Column(String)
    semester = Column(Integer)
    email = Column(String)
    
    anmeldungen = relationship("GruppeAnmeldung", back_populates="student")

class Veranstaltung(Base):
    __tablename__ = "veranstaltungen"
    id = Column(Integer, primary_key=True, index=True)
    titel = Column(String)
    start = Column(DateTime)
    ende = Column(DateTime) # Einschreibefrist

    gruppen = relationship("Gruppe", back_populates="veranstaltung")
    zielgruppen = relationship("VeranstaltungZielgruppe", back_populates="veranstaltung")

class Gruppe(Base):
    __tablename__ = "gruppen"
    id = Column(Integer, primary_key=True, index=True)
    veranstaltung_id = Column(Integer, ForeignKey("veranstaltungen.id"))
    name = Column(String)
    max_teilnehmer = Column(Integer)

    veranstaltung = relationship("Veranstaltung", back_populates="gruppen")
    anmeldungen = relationship("GruppeAnmeldung", back_populates="gruppe")

class GruppeAnmeldung(Base):
    __tablename__ = "gruppen_anmeldungen"
    id = Column(Integer, primary_key=True, index=True)
    gruppe_id = Column(Integer, ForeignKey("gruppen.id"))
    student_id = Column(Integer, ForeignKey("studenten.id"))
    status = Column(String) # 'angemeldet', 'warteliste'
    created_at = Column(DateTime)

    gruppe = relationship("Gruppe", back_populates="anmeldungen")
    student = relationship("Student", back_populates="anmeldungen")
    
class VeranstaltungZielgruppe(Base):
    __tablename__ = "veranstaltung_zielgruppen"
    id = Column(Integer, primary_key=True, index=True)
    veranstaltung_id = Column(Integer, ForeignKey("veranstaltungen.id"))
    studiengang = Column(String)
    semester = Column(Integer)

    veranstaltung = relationship("Veranstaltung", back_populates="zielgruppen")
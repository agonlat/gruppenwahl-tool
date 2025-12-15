# file: models.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# -----------------------------
# Student
# -----------------------------
class Student(Base):
    __tablename__ = "studenten"

    id = Column(Integer, primary_key=True, index=True)
    matrikelnummer = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    studiengang = Column(String, nullable=False)
    semester = Column(Integer, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    anmeldungen = relationship("GruppeAnmeldung", back_populates="student")


# -----------------------------
# Veranstaltung
# -----------------------------
class Veranstaltung(Base):
    __tablename__ = "veranstaltungen"

    id = Column(Integer, primary_key=True, index=True)
    titel = Column(String, nullable=False)

    gruppen = relationship("Gruppe", back_populates="veranstaltung")
    zielgruppen = relationship("VeranstaltungZielgruppe", back_populates="veranstaltung")


# -----------------------------
# Gruppe
# -----------------------------
class Gruppe(Base):
    __tablename__ = "gruppen"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    veranstaltung_id = Column(Integer, ForeignKey("veranstaltungen.id"))
    max_teilnehmer = Column(Integer, nullable=False)

    start_datum = Column(DateTime, default=datetime.utcnow)  # Einschreibestart
    end_datum = Column(DateTime, default=datetime.utcnow)    # Einschreibeschluss

    veranstaltung = relationship("Veranstaltung", back_populates="gruppen")
    anmeldungen = relationship("GruppeAnmeldung", back_populates="gruppe")

    @property
    def belegte_plaetze(self):
        """Anzahl angemeldeter Studenten (aktiv + warteliste)"""
        return len(self.anmeldungen)

    @property
    def freie_plaetze(self):
        """Berechnet freie Plätze für die UI"""
        return max(self.max_teilnehmer - len([a for a in self.anmeldungen if a.status == "aktiv"]), 0)

    @property
    def einschreibung_offen(self):
        """Prüft, ob die Einschreibung aktuell offen ist"""
        now = datetime.utcnow()
        return self.start_datum <= now <= self.end_datum


# -----------------------------
# GruppeAnmeldung (Student → Gruppe)
# -----------------------------
class GruppeAnmeldung(Base):
    __tablename__ = "gruppe_anmeldungen"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("studenten.id"))
    gruppe_id = Column(Integer, ForeignKey("gruppen.id"))
    status = Column(String, default="aktiv")  # aktiv | warteliste
    zeitpunkt = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="anmeldungen")
    gruppe = relationship("Gruppe", back_populates="anmeldungen")


# -----------------------------
# Veranstaltung Zielgruppe (Studiengang + Semester)
# -----------------------------
class VeranstaltungZielgruppe(Base):
    __tablename__ = "veranstaltung_zielgruppen"

    id = Column(Integer, primary_key=True)
    veranstaltung_id = Column(Integer, ForeignKey("veranstaltungen.id"))
    studiengang = Column(String, nullable=False)
    semester = Column(Integer, nullable=False)

    veranstaltung = relationship("Veranstaltung", back_populates="zielgruppen")

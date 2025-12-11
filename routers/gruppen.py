from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime

from database import Gruppe, GruppeAnmeldung, Student, Veranstaltung, get_db
from models import GruppeReadWithSpots
from utils.excel_export import export_gruppe_excel
from typing import List

router = APIRouter()


@router.get("/", response_model=List[GruppeReadWithSpots])
def group_list(db: Session = Depends(get_db)):
    groups = db.query(Gruppe).all()
    result = []

    for g in groups:
        belegte = db.query(GruppeAnmeldung).filter(
            GruppeAnmeldung.gruppe_id == g.id,
            GruppeAnmeldung.status == "angemeldet"
        ).count()

        v = db.query(Veranstaltung).filter(
            Veranstaltung.id == g.veranstaltung_id
        ).first()

        result.append(GruppeReadWithSpots(
            id=g.id,
            name=g.name,
            max_teilnehmer=g.max_teilnehmer,
            veranstaltung_titel=v.titel if v else "Unbekannt",
            belegte_plaetze=belegte,
            freie_plaetze=max(0, g.max_teilnehmer - belegte)
        ))

    return result


@router.post("/{gruppe_id}/register/{student_id}")
def register_to_group(gruppe_id: int, student_id: int, db: Session = Depends(get_db)):
    gruppe = db.query(Gruppe).filter(Gruppe.id == gruppe_id).first()
    if not gruppe:
        raise HTTPException(404, "Gruppe nicht gefunden")

    event = db.query(Veranstaltung).filter(
        Veranstaltung.id == gruppe.veranstaltung_id
    ).first()

    # Deadline check (Python 3.8 safe)
    if event and event.ende:
        event_end = event.ende.replace(tzinfo=None)
        if datetime.now() > event_end:
            raise HTTPException(403, "Einschreibefrist ist abgelaufen")

    # Duplicate check
    existing = db.query(GruppeAnmeldung).filter(
        GruppeAnmeldung.gruppe_id == gruppe_id,
        GruppeAnmeldung.student_id == student_id
    ).first()

    if existing:
        return {"message": f"Schon registriert: {existing.status}"}

    belegte = db.query(GruppeAnmeldung).filter(
        GruppeAnmeldung.gruppe_id == gruppe_id,
        GruppeAnmeldung.status == "angemeldet"
    ).count()

    status = "angemeldet" if belegte < gruppe.max_teilnehmer else "warteliste"
    msg = "Erfolgreich angemeldet!" if status == "angemeldet" else "Auf Warteliste gesetzt."

    entry = GruppeAnmeldung(
        gruppe_id=gruppe_id,
        student_id=student_id,
        status=status,
        created_at=datetime.now()
    )
    db.add(entry)
    db.commit()

    return {"message": msg, "status": status}


@router.get("/{gruppe_id}/export")
def export_group(gruppe_id: int, db: Session = Depends(get_db)):
    gruppe = db.query(Gruppe).filter(Gruppe.id == gruppe_id).first()
    if not gruppe:
        raise HTTPException(404, "Gruppe nicht gefunden")

    anmeldungen = db.query(GruppeAnmeldung).filter(
        GruppeAnmeldung.gruppe_id == gruppe_id
    ).all()

    if not anmeldungen:
        raise HTTPException(404, "Keine Anmeldungen")

    export_data = []
    for a in anmeldungen:
        student = db.query(Student).filter(Student.id == a.student_id).first()
        if student:
            export_data.append((student, a.status, a.created_at))

    filename = f"gruppe_{gruppe.name}_{datetime.now().strftime('%Y%m%d')}.xlsx"
    path = export_gruppe_excel(export_data, filename)

    return FileResponse(path, filename=filename)

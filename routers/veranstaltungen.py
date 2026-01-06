# fileName: veranstaltungen.py (KORRIGIERT)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel

from database import get_db 
from models import Veranstaltung, VeranstaltungZielgruppe

router = APIRouter()

# --- Pydantic Modelle ---

class VeranstaltungCreate(BaseModel):
    titel: str
    start: str  # Als String vom Frontend
    ende: str   # Als String vom Frontend

class ZielgruppeCreate(BaseModel):
    studiengang: str
    semester: int

# --- API Endpunkte ---

@router.get("/")
def list_events(db: Session = Depends(get_db)):
    """Gibt alle Veranstaltungen zurück (wird von Admin-Frontend für Dropdowns benötigt)."""
    events = db.query(Veranstaltung).all()
    # Wandelt datetime-Objekte in ISO-Strings für JSON um
    return [{
        "id": v.id, 
        "titel": v.titel,
        "start": v.start.isoformat() if v.start else None,
        "ende": v.ende.isoformat() if v.ende else None
    } for v in events]


@router.post("/")
def create_event(
    event: VeranstaltungCreate,
    db: Session = Depends(get_db)
):
    """Erstellt eine neue Veranstaltung (Admin-Funktion)."""
    v = Veranstaltung(
        titel=event.titel,
        # Konvertiere ISO-Strings in datetime-Objekte
        start=datetime.fromisoformat(event.start),
        ende=datetime.fromisoformat(event.ende) 
    )
    db.add(v)
    db.commit()
    db.refresh(v)
    return v


@router.post("/{event_id}/target_group")
def add_target_group(
    event_id: int,
    target: ZielgruppeCreate,
    db: Session = Depends(get_db)
):
    """Fügt eine Zielgruppe (Studiengang/Semester) zur Veranstaltung hinzu."""
    if not db.query(Veranstaltung).get(event_id):
        raise HTTPException(404, "Veranstaltung nicht gefunden")
        
    zg = VeranstaltungZielgruppe(
        veranstaltung_id=event_id,
        studiengang=target.studiengang,
        semester=target.semester
    )
    db.add(zg)
    db.commit()
    db.refresh(zg)

    return {"message": "Zielgruppe erfolgreich hinzugefügt", "id": zg.id}

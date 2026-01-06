# fileName: routers/gruppen.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel 


from database import get_db
from models import (
    Gruppe, GruppeAnmeldung, Veranstaltung,
    VeranstaltungZielgruppe, Student
)


from utils.excel_export import export_gruppe_excel 
# from utils.excel_export import export_gruppe_excel

from fastapi.responses import FileResponse

router = APIRouter()

# --- Pydantic Modelle ---

class GruppeCreate(BaseModel):
    name: str
    veranstaltung_id: int
    max_teilnehmer: int

# --- API Endpunkte ---

# ... (Rest des Codes von gruppen.py mit allen Funktionen (list_groups, register_group, export_group) 
# bleibt wie in meiner letzten umfassenden Antwort, da er bereits vollständig war)

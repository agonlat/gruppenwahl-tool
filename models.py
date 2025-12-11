from pydantic import BaseModel
from typing import Optional

class StudentCreate(BaseModel):
    name: str
    matrikelnummer: str
    studiengang: str
    semester: int
    email: str


class GruppeReadWithSpots(BaseModel):
    id: int
    name: str
    max_teilnehmer: int
    veranstaltung_titel: str
    belegte_plaetze: int
    freie_plaetze: int

    class Config:
        orm_mode = True

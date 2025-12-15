# fileName: main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import Base, engine #

# Samit SQLAlchemy alle Tabellen kennt
import models 

from routers import studenten, gruppen, veranstaltungen #

# Erstellt alle Tabellen, die in 'models.py' definiert sind
Base.metadata.create_all(bind=engine) #

app = FastAPI(title="Gruppenwahlsystem")

app.include_router(studenten.router, prefix="/students") #
app.include_router(gruppen.router, prefix="/groups") #
app.include_router(veranstaltungen.router, prefix="/events") #

# Stellt sicher, dass das Frontend aus dem 'static' Ordner geladen wird
app.mount("/", StaticFiles(directory="static", html=True), name="static") #
# main.py
from fastapi import FastAPI
# Assuming 'routers' is the package name (e.g., a directory)
from routers import studenten, gruppen
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Gruppenwahlsystem")
app.mount("/", StaticFiles(directory="static", html=True), name="static")
# Router einbinden
app.include_router(studenten.router, prefix="/studenten", tags=["Studenten"])
app.include_router(gruppen.router, prefix="/gruppen", tags=["Gruppen"])

@app.get("/")
def root():
    return {"message": "Gruppenwahlsystem läuft!"}
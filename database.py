# database.py
# Diese Datei kümmert sich um die Verbindung zur Datenbank
# und stellt FastAPI eine saubere Datenbank-Session pro Request bereit.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --------------------------------------------------
# Datenbank-URL
# SQLite-Datenbank als Datei im Projektverzeichnis
# --------------------------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

# --------------------------------------------------
# Engine = zentrale Verbindung zur Datenbank
# check_same_thread=False ist notwendig für SQLite + FastAPI,
# da FastAPI mit mehreren Threads arbeitet
# --------------------------------------------------
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# --------------------------------------------------
# SessionLocal ist eine "Session-Fabrik"
# Jede Anfrage bekommt ihre eigene DB-Session
# --------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,   # Commit nur manuell (db.commit())
    autoflush=False,    # Kein automatisches Schreiben in die DB
    bind=engine
)

# --------------------------------------------------
# Base-Klasse für alle SQLAlchemy-Modelle
# Jedes Model (z.B. Student) erbt von Base
# --------------------------------------------------
Base = declarative_base()

# --------------------------------------------------
# Dependency für FastAPI
# Stellt einer Route eine Datenbank-Session zur Verfügung
# und schließt sie nach dem Request automatisch
# --------------------------------------------------
def get_db():
    db = SessionLocal()  # Neue Datenbank-Session öffnen
    try:
        yield db          # Session an die Route übergeben
    finally:
        db.close()        # Session nach Request schließen

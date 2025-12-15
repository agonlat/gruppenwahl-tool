# file: test_dummy_groups.py

from fastapi.testclient import TestClient
from main import app
from database import get_db
from models import Student, Veranstaltung, Gruppe
import random

client = TestClient(app)

# --------------------------
# 1. Dummy-Veranstaltung und Gruppe in der DB anlegen
# --------------------------
db = next(get_db())

# Prüfen, ob Dummy-Gruppe schon existiert
if not db.query(Veranstaltung).filter_by(titel="Testvorlesung").first():
    veranstaltung = Veranstaltung(titel="Testvorlesung", semester=1)
    db.add(veranstaltung)
    db.commit()
    db.refresh(veranstaltung)

    gruppe = Gruppe(
        name="Testgruppe",
        max_teilnehmer=5,
        belegte_plaetze=0,
        einschreibung_offen=True,
        veranstaltung_id=veranstaltung.id
    )
    db.add(gruppe)
    db.commit()
    print("Dummy-Veranstaltung und Gruppe erstellt.")
else:
    veranstaltung = db.query(Veranstaltung).filter_by(titel="Testvorlesung").first()
    gruppe = db.query(Gruppe).filter_by(name="Testgruppe").first()
    print("Dummy-Gruppe existiert bereits.")

# --------------------------
# 2. Test-Student registrieren
# --------------------------
matrikelnummer = str(random.randint(10000, 99999))  # zufällige Matrikelnummer

register_res = client.post("/students/register", json={
    "name": "Test Student",
    "matrikelnummer": matrikelnummer,
    "studiengang": "Informatik",
    "semester": 1,
    "email": f"test{matrikelnummer}@uni.de",
    "password": "Test1234!",
    "password_repeat": "Test1234!"
})

if register_res.status_code == 200:
    student_id = register_res.json()["student_id"]
    print(f"Student registriert: ID={student_id}, Matrikel={matrikelnummer}")
else:
    print("Student konnte nicht registriert werden:", register_res.json())
    # Login versuchen, falls schon existiert
    login_res = client.post("/students/login", json={
        "matrikelnummer": matrikelnummer,
        "password": "Test1234!"
    })
    student_id = login_res.json().get("student_id")
    print(f"Student eingeloggt: ID={student_id}")

# --------------------------
# 3. Gruppenanmeldung testen
# --------------------------
group_id = gruppe.id

register_group_res = client.post(f"/groups/{group_id}/register/{student_id}")
if register_group_res.status_code == 200:
    print("Gruppenanmeldung erfolgreich:", register_group_res.json())
else:
    print("Gruppenanmeldung fehlgeschlagen:", register_group_res.json())

# --------------------------
# 4. Kontrolle in DB
# --------------------------
updated_group = db.query(Gruppe).filter_by(id=group_id).first()
print(f"Belegte Plätze nach Anmeldung: {updated_group.belegte_plaetze}")

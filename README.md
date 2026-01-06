# Gruppenwahlsystem – FastAPI Projekt

Dieses Projekt ist eine Webanwendung zur **Gruppenwahl für Studierende**.  
Studierende können sich registrieren, einloggen und sich in Gruppen einschreiben.  
Sachbearbeiter (Admin) können Gruppen und Veranstaltungen verwalten.

⚠️ **WICHTIG:**  
Dieses Projekt ist ein **Lern- / Hochschulprojekt** und erfüllt **nicht alle Sicherheitsanforderungen für den Produktiveinsatz**.

---

## Technologien

- **Backend:** FastAPI (Python)
- **Datenbank:** SQLite + SQLAlchemy
- **Authentifizierung:** Benutzername + Passwort (bcrypt)
- **Frontend:** HTML, CSS, JavaScript (ohne Framework)
- **Server:** Uvicorn

---


## ▶️ Anwendung starten

### 1️⃣ Abhängigkeiten installieren
```bash
pip install fastapi uvicorn sqlalchemy passlib bcrypt email-validator
(empfohlene Versionen für Stabilität)

bash
Copy code
pip install passlib==1.7.4 bcrypt==3.2.2
2️⃣ Server starten
bash
Copy code
uvicorn main:app --reload
Der Server läuft standardmäßig unter:

cpp
Copy code
http://127.0.0.1:8000
Benutzeroberflächen (UI)
👨Studierenden-UI
arduino
Copy code
http://127.0.0.1:8000/student.html
Funktionen:

Registrierung

Login

Anzeige verfügbarer Gruppen

Anmeldung / Warteliste

Logout

Admin-UI (Sachbearbeiter)


http://127.0.0.1:8000/admin.html
Funktionen:

Anlegen von Veranstaltungen

Erstellen und Verwalten von Gruppen

Übersicht über Teilnehmer

Sicherheitshinweis (SEHR WICHTIG)
Diese Anwendung ist NICHT vollständig abgesichert.

Aktueller Stand:

❌ Admin-UI ist ohne Passwort erreichbar

❌ Keine Rollen-/Rechteprüfung

❌ Kein JWT / Session-Token

❌ Kein HTTPS

❌ Kein CSRF-Schutz

Jeder kann admin.html direkt aufrufen, wenn er die URL kennt.

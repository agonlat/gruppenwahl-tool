// fileName: static/student.js

// Lade Daten aus dem lokalen Speicher
let studentId = localStorage.getItem('studentId') || null;
let studentMatrikel = localStorage.getItem('studentMatrikel') || null;
let studentName = localStorage.getItem('studentName') || null;


// --- Hilfsfunktionen und UI-Updates ---

/**
 * Zeigt eine Nachricht an.
 */
function displayMessage(message, isSuccess) {
    const element = document.getElementById("authMessage");
    if (!element) return;
    
    element.textContent = message;
    element.style.color = isSuccess ? "green" : "red";
    // Nachricht nach 5 Sekunden ausblenden
    setTimeout(() => { element.textContent = ''; }, 5000); 
}

/**
 * Steuert die Sichtbarkeit von Login vs Dashboard basierend auf dem Login-Status.
 * Wird nach Login/Logout/Registrierung aufgerufen.
 */
function updateUIState() {
    const authSection = document.getElementById("authSection");
    const dashboardSection = document.getElementById("dashboardSection");
    const nameDisplay = document.getElementById("studentNameDisplay");
    const matrDisplay = document.getElementById("currentMatrikelDisplay");

    if (studentId) {
        // User ist eingeloggt: Zeige Dashboard
        if (authSection) authSection.style.display = 'none';
        if (dashboardSection) dashboardSection.style.display = 'block';
        
        // Matrikelnummer und Name anzeigen
        if (nameDisplay) nameDisplay.textContent = studentName || 'N/A';
        if (matrDisplay) matrDisplay.textContent = studentMatrikel || 'N/A';
        
        loadGroups(); // Gruppen laden, wenn eingeloggt
    } else {
        // User ist ausgeloggt: Zeige Auth-Formulare
        if (authSection) authSection.style.display = 'block';
        if (dashboardSection) dashboardSection.style.display = 'none';
    }
}

/**
 * Logout Funktion
 */
function logout() {
    studentId = null;
    studentMatrikel = null;
    studentName = null;
    localStorage.removeItem('studentId');
    localStorage.removeItem('studentMatrikel');
    localStorage.removeItem('studentName');
    resetAuthForms();
    displayMessage("Erfolgreich abgemeldet.", true);
    updateUIState();
}


// --- Gruppen- und Anmelde-Logik ---

async function registerGroup(groupId, button) {
    if (!studentId) {
        displayMessage("Bitte zuerst einloggen!", false);
        return;
    }
    
    button.disabled = true;
    button.textContent = "...";

    try {
        const res = await fetch(`/groups/${groupId}/register/${studentId}`, { method: "POST" });
        const result = await res.json();
        
        if (res.ok) {
            displayMessage(`Anmeldung erfolgreich! Status: ${result.status.toUpperCase()}`, true);
        } else {
            displayMessage(`Fehler: ${result.detail || result.message}`, false);
        }
    } catch (e) {
        displayMessage("Netzwerkfehler bei der Anmeldung.", false);
    }
    
    loadGroups(); 
}

async function loadGroups() {
    const groupsTableBody = document.getElementById("groupsTableBody");
    if (!groupsTableBody) return;
    
    const res = await fetch("/groups/");
    if (!res.ok) {
        groupsTableBody.innerHTML = "<tr><td colspan='6'>Gruppen konnten nicht geladen werden (Serverfehler oder keine Gruppen).</td></tr>";
        return; 
    }
    
    const groups = await res.json();
    groupsTableBody.innerHTML = "";

    groups.forEach(g => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${g.veranstaltung_titel}</td>
            <td>${g.name}</td>
            <td>${g.max_teilnehmer}</td>
            <td><span class="badge green">${g.belegte_plaetze}</span></td>
            <td>${g.freie_plaetze > 0 ? `<span class="badge green">${g.freie_plaetze}</span>` : `<span class="badge red">0</span>`}</td>
        `;

        const action = document.createElement("td");
        const btn = document.createElement("button");
        btn.className = "primary";
        
        // Logik für den Anmelde-Button
        if (!studentId) {
            btn.textContent = "Anmelden (Login nötig)";
            btn.disabled = true;
        } else if (!g.einschreibung_offen) {
            btn.textContent = "Frist abgelaufen";
            btn.disabled = true;
            btn.classList.add("secondary");
        } else {
            btn.textContent = g.freie_plaetze > 0 ? "Anmelden" : "Warteliste";
            btn.disabled = false;
            btn.onclick = () => registerGroup(g.id, btn);
        }
        action.appendChild(btn);
        tr.appendChild(action);
        groupsTableBody.appendChild(tr);
    });
}

function resetAuthForms() {
    document.getElementById("simpleLoginForm")?.reset();
    document.getElementById("fullRegisterForm")?.reset();
}

// --- Haupt-Authentifizierungslogik ---

/**
 * Sendet die Anmelde-/Registrierungsdaten an den Server und speichert den Zustand.
 */
async function handleAuthSubmit(url, data) {
    try {
        const res = await fetch(url, { 
            method: "POST", 
            headers: { "Content-Type": "application/json" }, 
            body: JSON.stringify(data) 
        });
        const result = await res.json();
        
        if (res.ok) {
            // Speichern der Daten
            studentId = result.student_id;
            studentName = result.student_name;
            studentMatrikel = result.matrikelnummer; // Matrikelnummer speichern

            localStorage.setItem('studentId', studentId);
            localStorage.setItem('studentName', studentName);
            localStorage.setItem('studentMatrikel', studentMatrikel);
            resetAuthForms();
            displayMessage(`Erfolg: ${result.message}`, true);
            updateUIState(); // UI sofort umschalten
        } else {
            displayMessage(`Fehler: ${result.detail || result.message}`, false);
        }
    } catch (error) {
        displayMessage("Verbindungsfehler zum Server.", false);
    }
}


// --- Formular-Umschaltung und Listener ---

function setupAuthForms() {
    const simpleForm = document.getElementById("simpleLoginForm");
    const fullForm = document.getElementById("fullRegisterForm");
    const showLogin = document.getElementById("showLogin");
    const showRegister = document.getElementById("showRegister");
    const logoutBtn = document.getElementById("logoutBtn");

    // Logout Button Listener
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }


    // Tabs umschalten (wie gehabt)
    if (showLogin && showRegister) {
        showLogin.addEventListener('click', () => {
            simpleForm.style.display = 'block';
            fullForm.style.display = 'none';
            showLogin.classList.add('primary');
            showRegister.classList.remove('primary');
            showRegister.classList.add('secondary');
            document.getElementById("authMessage").textContent = '';
        });
        showRegister.addEventListener('click', () => {
            simpleForm.style.display = 'none';
            fullForm.style.display = 'block';
            showRegister.classList.add('primary');
            showLogin.classList.remove('primary');
            showLogin.classList.add('secondary');
            document.getElementById("authMessage").textContent = '';
        });
    }

    // 1. Login-Listener
    if (simpleForm) {
        simpleForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const matNr = document.getElementById("login_matrikelnummer").value;
            const pass = document.getElementById("login_password").value;

            // Manuelle Validierung für leere Felder 
            if (!matNr || !pass) {
                displayMessage("Bitte Matrikelnummer und Passwort eingeben.", false);
                return;
            }

            const data = { matrikelnummer: matNr, password: pass };
            handleAuthSubmit("/students/login", data);
        });
    }

    // 2. Registrierung-Listener
    if (fullForm) {
        fullForm.addEventListener("submit", (e) => {
            e.preventDefault();

            const password = document.getElementById("reg_password").value;
            const passwordRepeat = document.getElementById("reg_password_repeat").value;

            // Einfache Validierung
            if (password !== passwordRepeat) {
                displayMessage("Passwörter stimmen nicht überein!", false);
                return;
            }

            const data = {
                name: document.getElementById("reg_name").value,
                matrikelnummer: document.getElementById("reg_matrikelnummer").value,
                studiengang: document.getElementById("reg_studiengang").value,
                semester: Number(document.getElementById("reg_semester").value),
                email: document.getElementById("reg_email").value,
                password: password,
                password_repeat: passwordRepeat
            };

            // Hier wird die Server-Validierung (Länge, leere Felder) ausgelöst
            handleAuthSubmit("/students/register", data);
            
            // Wenn der Server mit Erfolg antwortet, wird die UI umgeschaltet.
            // Das Formular nur bei Erfolg zurücksetzen
            // (Wir resetten es hier nicht, damit der Nutzer die Daten bei Fehler korrigieren kann.)
        });
    }
}


// --- INITIALISIERUNG ---
document.addEventListener('DOMContentLoaded', () => {
    setupAuthForms();
    updateUIState(); // Prüft beim Laden, ob schon eingeloggt ist und schaltet die Ansicht um
});
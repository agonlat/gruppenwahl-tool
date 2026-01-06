// fileName: static/script.js (KORRIGIERT UND GETRENNT)

let studentId = localStorage.getItem('studentId') || null;

// --- Helfer-Funktionen ---
function updateStudentDisplay() {
    const studentIdSpan = document.getElementById("currentStudentId");
    if (studentIdSpan) {
        studentIdSpan.textContent = studentId ? studentId : "N/A";
    }
}
function displayMessage(elementId, message, isSuccess) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    element.textContent = message;
    element.style.color = isSuccess ? "green" : "red";
    // Deaktiviert das Auto-Hide, damit die ID sichtbar bleibt
    // setTimeout(() => { element.textContent = ''; }, 5000); 
}

// --- Gruppenanzeige (Shared) ---
async function loadGroups(isAdminView) {
    const groupsTableBody = document.getElementById("groupsTableBody");
    if (!groupsTableBody) return;
    
    const res = await fetch("/groups/");
    // Wichtig: Bei HTTP-Fehlern (404, 500) wird 'groups' nicht zum Array, daher wird das try/catch benötigt.
    if (!res.ok) {
        // Bei Fehlern leere Tabelle anzeigen und Fehlermeldung loggen.
        console.error("Fehler beim Laden der Gruppen:", await res.text());
        groupsTableBody.innerHTML = "<tr><td colspan='6'>Gruppen konnten nicht geladen werden.</td></tr>";
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
        if (isAdminView) {
             // ADMIN AKTION: Export Link
            const exportLink = document.createElement("a");
            exportLink.textContent = "Export (Excel)";
            exportLink.href = `/groups/${g.id}/export`;
            exportLink.target = "_blank"; 
            action.appendChild(exportLink);
        } else {
            // STUDENT AKTION: Anmelde-Button
            const btn = document.createElement("button");
            btn.className = "primary";
            
            if (!studentId) {
                btn.textContent = "Anmelden (Login nötig)";
                btn.disabled = true;
            } else if (!g.einschreibung_offen) {
                btn.textContent = "Frist abgelaufen";
                btn.disabled = true;
            } else {
                btn.textContent = g.freie_plaetze > 0 ? "Anmelden" : "Warteliste";
                btn.disabled = false;
                btn.onclick = () => registerGroup(g.id);
            }
            action.appendChild(btn);
        }
        
        tr.appendChild(action);
        groupsTableBody.appendChild(tr);
    });
}

async function registerGroup(groupId) {
    const res = await fetch(`/groups/${groupId}/register/${studentId}`, {
        method: "POST"
    });
    const result = await res.json();
    alert(result.message);
    loadGroups(document.getElementById("eventForm") != null); // Lade Gruppen neu
}


// --- Studenten-Funktionen ---
function setupStudentListener() {
    const studentForm = document.getElementById("studentForm");
    if (!studentForm) return;

    studentForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
            name: document.getElementById("name").value,
            matrikelnummer: document.getElementById("matrikelnummer").value,
            studiengang: document.getElementById("studiengang").value,
            semester: Number(document.getElementById("semester").value),
            email: document.getElementById("email").value
        };

        const res = await fetch("/students/register", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
        const result = await res.json();
        
        studentId = result.student_id;
        localStorage.setItem('studentId', studentId);
        
        if (res.ok) {
            displayMessage("registrationMessage", `${result.message}. Ihre ID ist gespeichert.`, true);
        } else {
            displayMessage("registrationMessage", `Fehler: ${result.message}`, false);
        }

        updateStudentDisplay();
        loadGroups(false); // Lade Gruppen für Studenten-Sicht neu
    });
}


// --- Admin-Funktionen (Management und Dropdowns) ---
async function loadEventsForAdmin() {
    // Wird nur auf admin.html aufgerufen
    if (!document.getElementById("group_event_id")) return; 
    
    const res = await fetch("/events/");
    if (!res.ok) return;

    const events = await res.json();
    
    const eventDropdowns = [
        document.getElementById("group_event_id"),
        document.getElementById("target_group_event_id")
    ];

    eventDropdowns.forEach(dropdown => {
        dropdown.innerHTML = '<option value="">-- 1. Veranstaltung wählen --</option>';

        events.forEach(event => {
            const option = document.createElement('option');
            option.value = event.id;
            const date = new Date(event.ende).toLocaleString('de-DE');
            option.textContent = `${event.titel} (Frist: ${date})`; 
            dropdown.appendChild(option);
        });
    });
}

function setupAdminListeners() {
    const eventForm = document.getElementById("eventForm");
    
    if (eventForm) { // Prüft, ob es die Admin-Seite ist
        loadEventsForAdmin();
        loadGroups(true); // Lade Gruppen in der Admin-Ansicht
        
    }
}


// --- INITIALISIERUNG ---
document.addEventListener('DOMContentLoaded', () => {
    // Lese studentId aus dem Speicher
    updateStudentDisplay(); 
    
    const isStudentPage = document.getElementById("studentForm") != null;
    const isAdminPage = document.getElementById("eventForm") != null;

    if (isStudentPage) {
        setupStudentListener();
        loadGroups(false); 
    }
    
    if (isAdminPage) {
        setupAdminListeners();
    }
    
    // Falls die ursprüngliche index.html geladen wird
    if (!isStudentPage && !isAdminPage) {
        console.warn("Weder student.html noch admin.html erkannt. Lade Standard-Gruppenansicht.");
        setupStudentListener();
        loadGroups(false);
    }
});

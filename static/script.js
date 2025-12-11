let studentId = null;

const studentForm = document.getElementById("studentForm");
const registrationMessage = document.getElementById("registrationMessage");
const studentInfo = document.getElementById("studentInfo");
const currentStudentId = document.getElementById("currentStudentId");
const currentStudentName = document.getElementById("currentStudentName");
const groupsTableBody = document.getElementById("groupsTableBody");
const groupMessage = document.getElementById("groupMessage");

studentForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        name: name.value,
        matrikelnummer: matrikelnummer.value,
        studiengang: studiengang.value,
        semester: Number(semester.value),
        email: email.value
    };

    const res = await fetch("/students/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await res.json();
    registrationMessage.textContent = result.message;

    studentId = result.student_id;
    currentStudentId.textContent = studentId;
    currentStudentName.textContent = result.student_name;

    studentInfo.style.display = "block";

    loadGroups();
});

async function loadGroups() {
    const res = await fetch("/groups/");
    const groups = await res.json();

    groupsTableBody.innerHTML = "";

    groups.forEach(g => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${g.veranstaltung_titel}</td>
            <td>${g.name}</td>
            <td>${g.max_teilnehmer}</td>
            <td>${g.belegte_plaetze}</td>
            <td>${g.freie_plaetze}</td>
        `;

        const action = document.createElement("td");
        const btn = document.createElement("button");

        btn.textContent = g.freie_plaetze > 0 ? "Anmelden" : "Warteliste";
        btn.disabled = !studentId;

        btn.addEventListener("click", () => registerGroup(g.id));

        action.appendChild(btn);
        tr.appendChild(action);

        groupsTableBody.appendChild(tr);
    });
}

async function registerGroup(groupId) {
    const res = await fetch(`/groups/${groupId}/register/${studentId}`, { method: "POST" });
    const result = await res.json();

    groupMessage.textContent = result.message;
    loadGroups();
}

document.addEventListener("DOMContentLoaded", loadGroups);

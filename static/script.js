const form = document.getElementById("studentForm");
const message = document.getElementById("message");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        name: document.getElementById("name").value,
        matrikelnummer: document.getElementById("matrikelnummer").value,
        studiengang: document.getElementById("studiengang").value,
        semester: parseInt(document.getElementById("semester").value),
        email: document.getElementById("email").value
    };

    const response = await fetch("/studenten/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await response.json();
    message.textContent = result.message;
});

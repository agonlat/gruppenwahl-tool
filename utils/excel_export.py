from openpyxl import Workbook
import os

def export_gruppe_excel(student_entries, filename):
    wb = Workbook()
    ws = wb.active
    ws.title = "Gruppe"

    ws.append(["Name", "Matrikelnummer", "Studiengang", "Semester", "Email", "Status", "Anmeldedatum"])

    for student, status, created_at in student_entries:
        ws.append([
            student.name,
            student.matrikelnummer,
            student.studiengang,
            student.semester,
            student.email,
            status,
            created_at.strftime("%Y-%m-%d %H:%M")
        ])

    filepath = f"./exports/{filename}"
    os.makedirs("./exports", exist_ok=True)
    wb.save(filepath)

    return filepath

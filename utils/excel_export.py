from openpyxl import Workbook

def export_gruppe_excel(students_list, filename="gruppen_export.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.append(["Name", "Matrikelnummer", "Studiengang", "Semester", "Email"])

    for s in students_list:
        ws.append([s.name, s.matrikelnummer, s.studiengang, s.semester, s.email])

    wb.save(filename)
    return filename

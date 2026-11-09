"""One-tab lead sheet from a signal_pipeline run. Usage: python build_xlsx.py <state.json> <out.xlsx>"""
import json, sys
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
d = json.load(open(sys.argv[1], encoding="utf-8"))
wb = Workbook(); ws = wb.active; ws.title = "Leads"
ws.append(["Name", "Title", "Company", "Work email", "Why now (job post)", "Job link", "LinkedIn"])
for c in ws[1]:
    c.fill, c.font = PatternFill("solid", fgColor="1D4ED8"), Font(bold=True, color="FFFFFF")
for w in sorted(d["leads"], key=lambda w: (w["tier"] != "high", w["company"])):
    ws.append([w["name"], w["title"], w["company"], w["email"], f'Hiring: {w["job"]} (posted {w["job_posted"]})', w["job_url"], w["linkedin"]])
for col, wd in zip("ABCDEFG", [22, 46, 26, 34, 52, 30, 30]):
    ws.column_dimensions[col].width = wd
ws.freeze_panes = "A2"; ws.auto_filter.ref = ws.dimensions
wb.save(sys.argv[2]); print("wrote", len(d["leads"]), "leads")

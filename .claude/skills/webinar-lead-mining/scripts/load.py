import openpyxl
def load():
    wb=openpyxl.load_workbook(__import__('os').environ.get('SHEET_XLSX','webinar/sheet.xlsx'),read_only=True)
    out={}
    for ws in wb:
        if ws.title.startswith('4'): continue
        rows=[tuple(r) for r in ws.iter_rows(values_only=True)]
        h=rows[0]; recs=[]
        for n,r in enumerate(rows[1:],start=2):
            r=tuple(r)+(None,)*(len(h)-len(r))
            d=dict(zip(h,r)); d['_row']=n; d['_tab']=ws.title
            if any(v not in (None,'') for v in r): recs.append(d)
        out[ws.title]=recs
    return out

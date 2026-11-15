from pypdf import PdfReader
r=PdfReader(r"C:\Users\madlyn\Downloads\RecSys Final Project\report\Madlyn_Manneh_session1_report.pdf")
print("pages:", len(r.pages))
for i,p in enumerate(r.pages,1):
    t=p.extract_text() or ""
    print("=== PAGE",i,"chars",len(t))
    print(t[:300].replace("\n"," | "))
PY
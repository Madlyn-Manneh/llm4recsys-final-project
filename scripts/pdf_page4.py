from pypdf import PdfReader
r=PdfReader(r"C:\Users\madlyn\Downloads\RecSys Final Project\report\Madlyn_Manneh_session1_report.pdf")
p=r.pages[3]
print(p.extract_text())
PY
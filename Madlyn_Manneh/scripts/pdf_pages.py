import re, zlib
data=open(r"C:\Users\madlyn\Downloads\RecSys Final Project\report\Madlyn_Manneh_session1_report.pdf","rb").read()
# map object number -> stream bytes
objs={}
for m in re.finditer(rb'(\d+)\s+0\s+obj(.*?)endobj', data, re.S):
    num=m.group(1).decode()
    body=m.group(2)
    objs[num]=body

# find pages
pages=[]
for num,body in objs.items():
    if b'/Type' in body and b'/Page' in body and b'/Pages' not in body:
        pages.append((num,body))
print("num pages:", len(pages))
for num,body in pages:
    # contents ref
    m=re.search(rb'/Contents\s+(\d+)\s+0\s+R', body)
    cref=m.group(1).decode() if m else None
    text=""
    if cref and cref in objs:
        cbody=objs[cref]
        # stream
        sm=re.search(rb'stream\r?\n(.*?)endstream', cbody, re.S)
        if sm:
            raw=sm.group(1)
            try:
                d=zlib.decompress(raw)
            except Exception:
                d=raw
            # extract text inside parentheses (Tj/TJ)
            text_parts=re.findall(rb'\((?:\\.|[^()\\])*\)', d)
            text=" ".join(p.decode('latin1') for p in text_parts)
    print("=== PAGE", num, "contents", cref, "===")
    print(text[:1500])
    print()
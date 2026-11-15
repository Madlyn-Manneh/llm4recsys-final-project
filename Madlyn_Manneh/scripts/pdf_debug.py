import re, zlib
data=open(r"C:\Users\madlyn\Downloads\RecSys Final Project\report\Madlyn_Manneh_session1_report.pdf","rb").read()
objs={}
for m in re.finditer(rb'(\d+)\s+0\s+obj(.*?)endobj', data, re.S):
    objs[m.group(1).decode()]=m.group(2)
body=objs["7"]
print("OBJ7 HEAD:", body[:300])
sm=re.search(rb'stream\r?\n(.*?)endstream', body, re.S)
print("stream found:", bool(sm))
if sm:
    raw=sm.group(1)
    print("raw len", len(raw))
    try:
        d=zlib.decompress(raw)
        print("decompressed len", len(d))
        print(d[:1000])
    except Exception as e:
        print("decompress err", e)
        print(raw[:500])
PY
import re, html, sys
src=sys.argv[1]; out=sys.argv[2]
text=open(src,encoding='utf-8').read()
title="Report"
for line in text.splitlines():
    if line.startswith("# "):
        title=line[2:].strip()
        break
def inline(s):
    s=html.escape(s)
    s=re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s=re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s
lines=text.split('\n')
parts=['<!DOCTYPE html><html><head><meta charset="utf-8"><title>'+html.escape(title)+'</title>',
'<style>',
'body{font-family:"Times New Roman",serif;font-size:11pt;line-height:1.35;margin:1in;}',
'h1{font-size:14pt;text-align:center;margin:12pt 0;}',
'h2{font-size:12pt;margin:10pt 0 4pt;}',
'h3{font-size:11pt;margin:8pt 0 3pt;}',
'p{margin:6pt 0;text-align:justify;}',
'blockquote{margin:6pt 0 6pt 18pt;font-style:italic;}',
'code{font-family:Consolas,monospace;font-size:9.5pt;}',
'pre{background:#f4f4f4;padding:8pt;border:1px solid #ccc;font-family:Consolas,monospace;font-size:9pt;white-space:pre-wrap;}',
'table{border-collapse:collapse;width:100%;margin:8pt 0;font-size:9.5pt;}',
'th,td{border:1px solid #333;padding:4pt;vertical-align:top;}',
'th{background:#eee;}',
'hr{border:none;border-top:1px solid #999;margin:10pt 0;}',
'ul{margin:4pt 0 4pt 18pt;}',
'li{margin:2pt 0;}',
'</style></head><body>']
i=0;n=len(lines)
while i<n:
    line=lines[i]
    if line.strip()=='':
        i+=1; continue
    if line.startswith('```'):
        code=[]; i+=1
        while i<n and not lines[i].startswith('```'):
            code.append(lines[i]); i+=1
        i+=1; parts.append('<pre>'+html.escape('\n'.join(code))+'</pre>'); continue
    if line.startswith('# '):
        parts.append('<h1>'+inline(line[2:])+'</h1>'); i+=1; continue
    if line.startswith('## '):
        parts.append('<h2>'+inline(line[3:])+'</h2>'); i+=1; continue
    if line.startswith('### '):
        parts.append('<h3>'+inline(line[4:])+'</h3>'); i+=1; continue
    if line.startswith('> '):
        parts.append('<blockquote>'+inline(line[2:])+'</blockquote>'); i+=1; continue
    if line.strip()=='---':
        parts.append('<hr>'); i+=1; continue
    if line.strip().startswith('|'):
        tbl=[]
        while i<n and lines[i].strip().startswith('|'):
            tbl.append(lines[i].strip()); i+=1
        rows=[]
        for tl in tbl:
            rows.append([c.strip() for c in tl.strip('|').split('|')])
        if len(rows)>1 and all(re.fullmatch(r'[-: ]+', c) for c in rows[1]):
            rows.pop(1)
        parts.append('<table>')
        for ridx,row in enumerate(rows):
            tag='th' if ridx==0 else 'td'
            parts.append('<tr>'+ ''.join(f'<{tag}>{inline(c)}</{tag}>' for c in row)+'</tr>')
        parts.append('</table>'); continue
    if line.strip().startswith('- '):
        items=[]
        while i<n and lines[i].strip().startswith('- '):
            items.append(lines[i].strip()[2:]); i+=1
        parts.append('<ul>'+ ''.join('<li>'+inline(it)+'</li>' for it in items)+'</ul>'); continue
    para=[]
    while i<n and lines[i].strip()!='' and not lines[i].startswith('#') and not lines[i].startswith('```') and not lines[i].strip().startswith('|') and not lines[i].strip().startswith('- ') and lines[i].strip()!='---' and not lines[i].startswith('> '):
        para.append(lines[i]); i+=1
    if para:
        parts.append('<p>'+inline(' '.join(para))+'</p>')
    else:
        i+=1
parts.append('</body></html>')
open(out,'w',encoding='utf-8').write('\n'.join(parts))
print('done')
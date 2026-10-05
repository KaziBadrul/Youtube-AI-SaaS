"""Explicitly download small OFL font assets, never AI/model weights."""
import hashlib,json,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/architecture/evidence/rendering-feasibility/S6'
TEMP=Path('/private/tmp/s6-render-fonts');TEMP.mkdir(exist_ok=True)
entries=[]
for family,directory,filename in [('Noto Sans','notosans','NotoSans[wdth,wght].ttf'),('Noto Sans Bengali','notosansbengali','NotoSansBengali[wdth,wght].ttf'),('Noto Sans Devanagari','notosansdevanagari','NotoSansDevanagari[wdth,wght].ttf')]:
 base=f'https://raw.githubusercontent.com/google/fonts/main/ofl/{directory}/'
 url=base+urllib.parse.quote(filename)
 data=urllib.request.urlopen(url,timeout=30).read()
 license_text=urllib.request.urlopen(base+'OFL.txt',timeout=30).read().decode()
 path=TEMP/(directory+'.ttf');path.write_bytes(data)
 (OUT/(directory+'-OFL.txt')).write_text(license_text)
 entries.append(dict(family=family,path=str(path),source=url,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),license='SIL Open Font License 1.1',license_source=base+'OFL.txt',redistributed_binary=False))
(OUT/'fonts.json').write_text(json.dumps(entries,indent=2)+'\n')
print(json.dumps([{k:v for k,v in x.items() if k in ('family','bytes','sha256')} for x in entries]))

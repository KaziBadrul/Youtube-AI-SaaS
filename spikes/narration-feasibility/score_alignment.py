"""Offline scoring of human-reviewed/ASR word records; does not transcribe audio.
Usage: python3 score_alignment.py approved.txt observed.json
JSON: {words:[{word,start,end}], duration:float, boundaries:[{observed,reference}]}
"""
import json,re,sys,unicodedata
from pathlib import Path
def tokens(text):
 return re.findall(r"\b[\w'-]+\b",unicodedata.normalize('NFKC',text).lower().replace('’',"'"))
def score(approved,observed):
 expected=tokens(approved); got=[t for r in observed['words'] for t in tokens(r['word'])]
 matrix=list(range(len(got)+1))
 for i,a in enumerate(expected,1):
  nxt=[i]
  for j,b in enumerate(got,1):nxt.append(min(nxt[-1]+1,matrix[j]+1,matrix[j-1]+(a!=b)))
  matrix=nxt
 errors=matrix[-1]; timings=observed['words'];duration=observed['duration']
 valid=all(0<=r['start']<r['end']<=duration for r in timings) and all(a['end']<=b['start'] for a,b in zip(timings,timings[1:]))
 boundaries=[round(abs(r['observed']-r['reference']),6) for r in observed.get('boundaries',[])]
 return {'approved_word_count':len(expected),'observed_word_count':len(got),'edit_distance':errors,'word_error_rate':errors/max(1,len(expected)),'sample_range_order_valid':valid,'boundary_absolute_errors_seconds':boundaries,'max_boundary_error_seconds':max(boundaries,default=None),'export_candidate':errors==0 and valid,'human_review_still_required':True}
if __name__=='__main__': print(json.dumps(score(Path(sys.argv[1]).read_text(),json.loads(Path(sys.argv[2]).read_text())),indent=2))

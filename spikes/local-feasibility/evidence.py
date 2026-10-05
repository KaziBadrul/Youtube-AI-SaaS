import datetime,hashlib,json,platform,sqlite3,sys,time,traceback
from pathlib import Path
BASE=Path(__file__).resolve().parent;REPO=BASE.parents[1];EVIDENCE=REPO/'docs/architecture/evidence/local-feasibility'
def run(gate,experiment):
 start=time.perf_counter();data={'gate':gate,'timestamp_utc':datetime.datetime.now(datetime.UTC).isoformat(),'python':sys.version,'platform':platform.platform(),'sqlite':sqlite3.sqlite_version,'plan_sha256':hashlib.sha256((EVIDENCE/'PLAN.md').read_bytes()).hexdigest()}
 try:data.update(experiment());data['verdict']='PASS'
 except Exception as e:data.update(verdict='FAIL',error=str(e),traceback=traceback.format_exc())
 data['elapsed_seconds']=round(time.perf_counter()-start,3)
 data['scaffold_hashes']={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in BASE.rglob('*') if p.suffix in ['.py','.js','.html']}
 (EVIDENCE/(gate+'.json')).write_text(json.dumps(data,indent=2)+'\n');print(json.dumps({k:data[k] for k in ['gate','verdict','elapsed_seconds']}))
 if data['verdict']!='PASS':print(data['traceback']);sys.exit(1)

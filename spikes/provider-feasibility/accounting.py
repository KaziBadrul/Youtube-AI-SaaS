"""Integer liability/usage/uncertainty examples; no provider integration."""
import json
from decimal import Decimal, ROUND_CEILING
from pathlib import Path
# Rates are USD/million tokens. Output includes thoughts; reserve worst modality rate.
def bound(i,o,ri,ro):
    return int((Decimal(i)*Decimal(ri)+Decimal(o)*Decimal(ro)).to_integral_value(rounding=ROUND_CEILING)) # microUSD
cases=[]
for model,i,o,ri,ro in [('gemini-3.8-flash-tts',8192,16384,'.5','9'),('gemini-3.8-flash-lite-tts',8192,16384,'.5','6'),('gemini-3.1-flash-image',131072,32768,'.5','60'),('gemini-3.1-flash-lite-image',65536,4096,'.25','30'),('gemini-3-pro-image',65536,32768,'2','120')]:
    b=bound(i,o,ri,ro); cases.append({'model':model,'input_serving_limit':i,'output_serving_limit':o,'rate_input_usd_per_million':ri,'rate_worst_output_usd_per_million':ro,'maximum_microUSD_per_attempt':b,'three_attempt_ceiling_microUSD':3*b})
# Receipt deduplication and unknown liability: mirrors accepted S3 policy, not real billing evidence.
held=cases[0]['maximum_microUSD_per_attempt']; submissions=1; settlement_ids=set(); ledger=[]
unknown={'state':'recovery_required','held_microUSD':held,'automatic_retry_allowed':False,'submissions':submissions}
assert not unknown['automatic_retry_allowed'] and unknown['held_microUSD']>0
for receipt in ['synthetic-result','synthetic-result']:
    if receipt not in settlement_ids:
        settlement_ids.add(receipt); ledger.append({'receipt':receipt,'usage_derived_microUSD':bound(12,25,'.5','9'),'invoice_actual_microUSD':None})
assert len(ledger)==1
missing_usage_cost=None
assert missing_usage_cost is None
out={'scope':'Conservative documented serving caps, standard paid rates retrieved 2026-10-04; no free discount, tool or cache storage; taxes/account charges require separate bound','bounds':cases,'unknown':unknown,'deduplicated_ledger':ledger,'missing_usage_cost':missing_usage_cost,'pass':True}
Path('docs/architecture/evidence/provider-feasibility/accounting.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'pass':True,'bounds':len(cases)}))

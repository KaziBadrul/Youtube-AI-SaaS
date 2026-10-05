"""Disposable S5 B+B closure using retained owner review; no network/audio writes."""
import hashlib
import json
import re
import sys
import wave
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
RUN=ROOT/'docs/architecture/evidence/narration-feasibility/runs/approved-lite-v1'
OUT=RUN/'b-mapping-final-v1'
sys.path.insert(0,str(Path(__file__).resolve().parent))
from check_mapping_closure import check
from validate_mapping_evidence import fixtures


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(exist_ok=True)
    sheet=RUN/'boundary-validation-v1/BOUNDARY_REVIEW.md'
    owner=RUN/'boundary-validation-v1/OWNER-BOUNDARY-REVIEW.md'
    assert 'every supplied transition clip and finding all OK' in owner.read_text()
    rows={};call=None
    for line in sheet.read_text().splitlines():
        if line.startswith('## Call '):call=int(line.split()[-1])
        if re.match(r'^\| \d+ → \d+ \|',line):
            parts=[p.strip() for p in line.split('|')[1:-1]]
            left,right=map(int,parts[0].split(' → '))
            rows[(call,left,right)]=dict(proposed=float(parts[1].split('s')[0]),finding=parts[4])
    assert len(rows)==62
    baseline=json.loads((RUN/'boundary-validation-v1/validation-results.json').read_text())
    report=dict(status='PASS_AT_EXISTING_B_PLUS_B_MAPPING_SCOPE',
                sheet_sha256=sha(sheet),owner_review_sha256=sha(owner),
                limits='owner-reviewed mappings for these recordings; not general unattended alignment or audio extraction certification',sources=[],boundaries=[])
    for old in baseline['calls']:
        call=old['call']
        path=RUN/'mapping-closure-v2'/f'call-{call:02d}-mapping.json'
        d=json.loads(path.read_text())
        initial=json.loads((RUN/'alignment-closure-v1'/f'call-{call:02d}-alignment.json').read_text())
        digest=sha(Path(d['source_audio']))
        check(d,(len(initial['expected_tokens']),len(initial['recognized_words'])),initial['transcription_info']['duration'],digest)
        for t in old['transitions']:
            row=rows[(call,t['left_scene'],t['right_scene'])]
            assert abs(row['proposed']-t['candidate_transition'])<.001
            finding=row['finding']; adjusted=None
            if not finding:
                state='OK';evidence='owner blanket approval in retained session record; sheet cell blank'
            elif finding.lower()=='ok':
                state='OK';evidence='owner sheet row'
            elif 'uncertain' in finding.lower():
                state='UNCERTAIN';evidence='owner sheet row'
            else:
                match=re.fullmatch(r'(?:adjusted\s*[:=]?\s*)?(\d+(?:\.\d+)?)\s*s?',finding,re.I)
                assert match, ('unrecognized_review_finding',finding)
                adjusted=float(match.group(1));state='ADJUSTED';evidence='owner sheet row'
            right=d['scene_mappings'][t['right_scene']-1]
            if adjusted is not None:
                assert t['clip_start_frame']/24000<=adjusted<=t['clip_end_frame']/24000
                assert d['scene_mappings'][t['left_scene']-1]['visual_start']<adjusted<right['visual_end']
                right['visual_start']=adjusted
                d['scene_mappings'][t['left_scene']-1]['visual_end']=adjusted
            if state=='UNCERTAIN':report['status']='READY_FOR_OWNER_BOUNDARY_REVIEW'
            report['boundaries'].append(dict(call=call,left_scene=t['left_scene'],right_scene=t['right_scene'],
                sheet_finding=finding,review_state=state,review_evidence=evidence,
                reviewed_proposed_boundary=row['proposed'] if state=='OK' else adjusted,
                image_transition=right['visual_start'] if state!='UNCERTAIN' else None,
                timing_rule='next_scene_start; owner-approved region and explicit timing clarification',
                source_audio_version=digest,source_scene_text_version=right['scene_text_version'],
                uncertainty=None if state!='UNCERTAIN' else 'owner marked uncertain'))
        d['status']='OWNER_REVIEWED_CONTINUOUS_B_SCENE_MAPPING'
        d['owner_review_version']=sha(owner)
        (OUT/f'call-{call:02d}-reviewed-mapping.json').write_text(json.dumps(d,indent=2)+'\n')
        report['sources'].append(dict(call=call,sha256=digest,approved_tokens=len(initial['expected_tokens']),recognized_tokens=len(initial['recognized_words']),scene_count=32,source_mapping_sha256=sha(path),derived_mapping_sha256=sha(OUT/f'call-{call:02d}-reviewed-mapping.json')))
    integrity=[]
    results=json.loads((RUN.parents[1]/'S5-GENERATION-RESULTS.json').read_text())
    for c in results['calls']:
        path=ROOT/c['audio'];assert sha(path)==c['hash']
        with wave.open(str(path),'rb') as w:
            raw=w.readframes(w.getnframes());assert len(raw)==w.getnframes()*w.getnchannels()*w.getsampwidth()
            integrity.append(dict(call=c['call'],sha256=c['hash'],duration=w.getnframes()/w.getframerate(),sample_rate=w.getframerate(),channels=w.getnchannels(),decode='PASS'))
    report['integrity']=integrity
    report['sequence_failure_tests']=fixtures()
    report['retained_mapping_gate_results']=json.loads((RUN/'mapping-closure-v2/gate-results.json').read_text())
    (OUT/'closure-results.json').write_text(json.dumps(report,indent=2)+'\n')
    composition=dict(initial=dict(source_call=4,mapping='call-04-reviewed-mapping.json'),
                     correction=dict(source_call=6,mapping='call-06-reviewed-mapping.json',affected_scenes=list(range(1,33)),preserved_previous_source=report['sources'][0]['sha256'],
                     behavior='select entire Call 6 source; retain Call 4 and mappings as history; no scene-level cuts'),
                     no_audio_created=True)
    (OUT/'b-composition.json').write_text(json.dumps(composition,indent=2)+'\n')
    print(report['status'],'62 boundary reviews; 8 unchanged decoded source WAVs')


if __name__=='__main__':main()

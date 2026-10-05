"""S5 disposable, offline evidence only. Preserves reviewed transcript distinctions."""
import hashlib
import json
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / 'docs/architecture/evidence/narration-feasibility/runs/approved-lite-v1'
OUT = RUN / 'mapping-closure-v2'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    OUT.mkdir(exist_ok=True)
    fixtures = json.loads((RUN.parents[1]/'fixture-manifest.json').read_text())
    scenes = {s['id']: s for s in fixtures['scenes']}
    summaries = []
    for call in (4, 6):
        source = RUN/'alignment-closure-v1'/f'call-{call:02d}-alignment.json'
        d = json.loads(source.read_text())
        assert sha(Path(d['audio_path'])) == d['audio_sha256']
        expected, recognized = d['expected_tokens'], d['recognized_words']
        probe_path = OUT/'scene18-probe-recognition.json'
        probe = json.loads(probe_path.read_text())['words'] if call==4 and probe_path.exists() else []
        # Retain full-source ASR unchanged. Use the cropped observation explicitly
        # for the local phrase; all overlapping old ranges are replaced together.
        if probe:
            assert [w['text'].strip('.,').lower() for w in probe] == ['i','actually','looked','this','up','down','a','rabbit','hole','earlier']
            old_start = next(i for i,w in enumerate(recognized) if w['text']=='Actually' and w['start']==92.7)
            for old,new in zip(recognized[old_start:old_start+9],probe[1:]):
                old['start'],old['end'] = new['start'],new['end']
        correspondences = []
        missing = []
        for tag,a,b,c,e in d['alignment']['opcodes']:
            if tag == 'equal':
                groups = [(i,i+1,j,j+1,'ASR_EXACT') for i,j in zip(range(a,b),range(c,e))]
            else:
                approved = ' '.join(t['text'] for t in expected[a:b])
                # Every original disagreement was resolved in the retained owner
                # review; this whitelist pins specific findings, not generic tolerance.
                allowed = {'AM','twelve','twenty-two','all-knowing','lightbulbs','twenties','rabbithole','de-idealization','middle-aged','thirties','twenty-four'}
                if approved in allowed:
                    status = 'OWNER_CONFIRMED_EQUIVALENT'
                elif call == 4 and approved in {'is','in'}:
                    status = 'OWNER_CONFIRMED_ASR_SUBSTITUTION'
                elif call == 4 and approved == 'I' and c == e:
                    status = 'OWNER_CONFIRMED_PRESENT_TIMESTAMP_UNRESOLVED'
                elif tag == 'insert' and [t['norm'] for t in recognized[c:e]] == ['a']:
                    # Pin insertion context rather than accepting arbitrary articles.
                    assert [t['norm'] for t in expected[max(0,a-2):a+1]] == ['out','of','mug']
                    status = 'OWNER_ACCEPTED_MINOR_VARIATION'
                else:
                    raise AssertionError(('unreviewed_difference',call,tag,approved))
                groups = [(a,b,c,e,status)]
            for a1,b1,c1,e1,status in groups:
                interval = [recognized[c1]['start'],recognized[e1-1]['end']] if c1<e1 else None
                if status=='OWNER_CONFIRMED_PRESENT_TIMESTAMP_UNRESOLVED' and probe:
                    interval=[probe[0]['start'],probe[0]['end']]
                    status='OWNER_CONFIRMED_PRESENT_CROP_ASR_TIMESTAMP'
                record = dict(expected_indexes=list(range(a1,b1)), recognized_indexes=list(range(c1,e1)),
                              approved_tokens=[t['text'] for t in expected[a1:b1]],
                              recognized_tokens=[t['text'] for t in recognized[c1:e1]],
                              source_interval=interval, correspondence_state=status,
                              timestamp_precision='ASR_GROUP_ESTIMATE' if interval else 'UNRESOLVED',
                              review_evidence='../b-only-review-v1/FIDELITY-POLICY-AMENDMENT.md' if status!='ASR_EXACT' else None)
                if status=='OWNER_CONFIRMED_PRESENT_CROP_ASR_TIMESTAMP':
                    record['secondary_observation']='scene18-probe-recognition.json:words[0]'
                correspondences.append(record)
                if interval is None:
                    missing.append(record)
        assert sorted(i for x in correspondences for i in x['expected_indexes']) == list(range(len(expected)))
        assert sorted(i for x in correspondences for i in x['recognized_indexes']) == list(range(len(recognized)))
        mappings = []
        offset = 0
        for i,m in enumerate(d['scene_mappings']):
            text = fixtures['edit']['edited'] if call==6 and m['scene_id']==20 else scenes[m['scene_id']]['text']
            import re
            count = len(re.findall(r"\b[\w’'-]+\b",text))
            indexes = set(range(offset,offset+count))
            assigned = [j for j,x in enumerate(correspondences) if indexes.intersection(x['expected_indexes'])]
            for j,x in enumerate(correspondences):
                if not x['expected_indexes']:
                    oi = x['recognized_indexes'][0]
                    if m['first_word_index'] <= oi <= m['last_word_index']:
                        assigned.append(j)
            speech_start = probe[0]['start'] if probe and m['scene_id']==18 else m['start_time']
            mappings.append(dict(scene_id=m['scene_id'], scene_text_version=hashlib.sha256(text.encode()).hexdigest(),
                                 source_audio_version=d['audio_sha256'], source_speech_start=speech_start, source_speech_end=m['end_time'],
                                 visual_start=0.0 if i==0 else speech_start,
                                 visual_end=d['scene_mappings'][i+1]['start_time'] if i+1<len(d['scene_mappings']) else d['transcription_info']['duration'],
                                 alignment_version='mapping-closure-v2', correspondence_indexes=sorted(assigned),
                                 visual_validation='OWNER_REVIEWED_TRANSITION_REGION',
                                 exact_extraction_validation='NOT_ESTABLISHED',
                                 confidence=m['confidence'], confidence_kind='ASR_MEAN_NOT_CALIBRATED_BOUNDARY_CONFIDENCE'))
            offset += count
        for left,right in zip(mappings,mappings[1:]):
            left['visual_end']=right['visual_start']
        assert offset == len(expected)
        assert all(a['visual_end']==b['visual_start'] for a,b in zip(mappings,mappings[1:]))
        payload = dict(call=call, source_audio=d['audio_path'], source_audio_version=d['audio_sha256'],
                       approved_text_version=d['approved_text_sha256'], source_alignment_sha256=sha(source),
                       correspondence_coverage=1., recognized_token_accounting=1.,
                       unresolved_individual_token_ranges=missing, correspondences=correspondences, scene_mappings=mappings,
                       owner_boundary_evidence='../boundary-validation-v1/OWNER-BOUNDARY-REVIEW.md',
                       status='REVIEWED_VISUAL_MAPPING_ONLY_NOT_EXACT_EXTRACTION')
        (OUT/f'call-{call:02d}-mapping.json').write_text(json.dumps(payload,indent=2)+'\n')
        summaries.append(dict(call=call, approved_tokens=len(expected), recognized_tokens=len(recognized),
                              scene_count=len(mappings), unresolved_timestamp_groups=len(missing), audio_sha256=d['audio_sha256']))
    (OUT/'summary.json').write_text(json.dumps(dict(status='NOT_YET_PASS',calls=summaries),indent=2)+'\n')
    # Additional recognition uses a derived crop only; original source is untouched.
    d=json.loads((RUN/'alignment-closure-v1/call-04-alignment.json').read_text())
    with wave.open(d['audio_path'],'rb') as w:
        params=w.getparams(); start=round(92.1*params.framerate); end=round(94.9*params.framerate)
        w.setpos(start); raw=w.readframes(end-start)
    with wave.open(str(OUT/'call-04-scene18-probe.wav'),'wb') as w:
        w.setparams(params); w.writeframes(raw)
    (OUT/'probe-recipe.json').write_text(json.dumps(dict(source_sha256=d['audio_sha256'],start_frame=start,end_frame=end,
                            sample_rate=params.framerate,derived_sha256=sha(OUT/'call-04-scene18-probe.wav'),processing='sample-exact copy; no normalization'),indent=2)+'\n')
    print(json.dumps(summaries))


if __name__ == '__main__':
    build()

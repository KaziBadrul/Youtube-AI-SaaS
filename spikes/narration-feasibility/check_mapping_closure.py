"""Validate the disposable S5 correspondence representation; no ASR or network."""
import copy
import hashlib
import json
import math
from pathlib import Path
from local_mapping_closure import OUT, RUN
from validate_mapping_evidence import fixtures


def check(d, counts, duration, source_hash):
    assert d['source_audio_version']==source_hash, 'source_version_mismatch'
    groups=d['correspondences']
    for key,n in [('expected_indexes',counts[0]),('recognized_indexes',counts[1])]:
        assert sorted(i for g in groups for i in g[key])==list(range(n)), 'incomplete_or_repeated_accounting'
    previous=0.
    for g in groups:
        a,b=g['source_interval'] or (float('nan'),float('nan'))
        assert math.isfinite(a) and math.isfinite(b) and previous<=a<b<=duration, 'untrusted_or_invalid_token_range'
        assert g['correspondence_state'] in {'ASR_EXACT','OWNER_CONFIRMED_EQUIVALENT','OWNER_CONFIRMED_ASR_SUBSTITUTION','OWNER_ACCEPTED_MINOR_VARIATION','OWNER_CONFIRMED_PRESENT_CROP_ASR_TIMESTAMP'}, 'unreviewed_difference'
        previous=b
    mappings=d['scene_mappings']
    assert [m['scene_id'] for m in mappings]==list(range(1,33)), 'missing_or_reordered_scene'
    assert mappings[0]['visual_start']==0 and mappings[-1]['visual_end']==duration, 'visual_duration_mismatch'
    for i,m in enumerate(mappings):
        assert m['source_audio_version']==source_hash and m['scene_text_version'], 'mapping_provenance_mismatch'
        assert 0<=m['source_speech_start']<m['source_speech_end']<=duration, 'invalid_scene_range'
        assert m['visual_start']<m['visual_end'], 'invalid_visual_range'
        if i:
            assert mappings[i-1]['visual_end']==m['visual_start']==m['source_speech_start'], 'wrong_visual_transition'
    assigned=[i for m in mappings for i in m['correspondence_indexes']]
    assert sorted(assigned)==list(range(len(groups))), 'ambiguous_scene_membership'
    return 'VALID_AT_REVIEWED_FIXTURE_SCOPE'


def main():
    results=[]
    for call in (4,6):
        d=json.loads((OUT/f'call-{call:02d}-mapping.json').read_text())
        source=json.loads((RUN/'alignment-closure-v1'/f'call-{call:02d}-alignment.json').read_text())
        digest=hashlib.sha256(Path(d['source_audio']).read_bytes()).hexdigest()
        counts=(len(source['expected_tokens']),len(source['recognized_words']));duration=source['transcription_info']['duration']
        verdict=check(d,counts,duration,digest)
        mutations={
            'omission':lambda x:x['correspondences'].pop(),
            'repetition':lambda x:x['correspondences'].append(copy.deepcopy(x['correspondences'][0])),
            'unresolved_timestamp':lambda x:x['correspondences'][0].update(source_interval=None),
            'truncation':lambda x:x['correspondences'][-1].update(source_interval=[duration,duration+1]),
            'unreviewed_substitution':lambda x:x['correspondences'][0].update(correspondence_state='UNREVIEWED'),
            'version_mismatch':lambda x:x.update(source_audio_version='wrong'),
            'ambiguous_scene':lambda x:x['scene_mappings'][1]['correspondence_indexes'].append(0),
            'wrong_image_transition':lambda x:x['scene_mappings'][1].update(visual_start=x['scene_mappings'][0]['source_speech_end']-.1),
        }
        rejected=[]
        for name, mutate in mutations.items():
            bad=copy.deepcopy(d);mutate(bad)
            try:
                check(bad,counts,duration,digest)
            except AssertionError as err:
                rejected.append(dict(case=name,reason=str(err)))
            else:
                raise AssertionError(('failed_to_reject',name))
        results.append(dict(call=call,status=verdict,negative_cases=rejected))
    (OUT/'gate-results.json').write_text(json.dumps(dict(real_mapping_checks=results,sequence_fixture_results=fixtures(),limits='structural acceptance of owner-reviewed fixtures; not automated acoustic verification'),indent=2)+'\n')
    print('2 reviewed mappings passed; 16 mutated mappings rejected; 13 sequence fixtures passed')


if __name__=='__main__':
    main()

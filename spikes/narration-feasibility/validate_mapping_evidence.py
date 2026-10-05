"""Disposable S5 evidence audit. Offline, stdlib only; never certifies ASR acoustics."""
import array
import hashlib
import json
import math
import re
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / 'docs/architecture/evidence/narration-feasibility/runs/approved-lite-v1'
OUT = RUN / 'boundary-validation-v1'


def tokens(text):
    return re.findall(r"[\w']+", text.lower().replace('’', "'"))


def gate(scene_texts, words, duration, reviewed_reference=False):
    """Enumerate exact, exhaustive ordered scene matches; ambiguity fails closed.

    Fixtures use one token per word record. Real reviewed variations need explicit
    token correspondences and an acoustic reference before this gate is usable.
    """
    if not words or not math.isfinite(duration) or duration <= 0:
        return {'status': 'INVALID', 'reason': 'empty_or_invalid_duration'}
    for i, w in enumerate(words):
        if not all(math.isfinite(w[k]) for k in ('start', 'end')) or not 0 <= w['start'] < w['end'] <= duration:
            return {'status': 'INVALID', 'reason': 'invalid_word_range'}
        if i and words[i-1]['end'] > w['start']:
            return {'status': 'INVALID', 'reason': 'overlap'}
    observed = [tokens(w['text']) for w in words]
    if any(len(x) != 1 for x in observed):
        return {'status': 'REVIEW_REQUIRED', 'reason': 'token_correspondence_required'}
    observed = [x[0] for x in observed]
    offsets = []
    for text in scene_texts:
        expected = tokens(text)
        if not expected:
            return {'status': 'INVALID', 'reason': 'empty_scene'}
        matches = [i for i in range(len(observed)-len(expected)+1) if observed[i:i+len(expected)] == expected]
        if len(matches) != 1:
            return {'status': 'REVIEW_REQUIRED' if matches else 'INVALID', 'reason': 'ambiguous_match' if matches else 'missing_scene'}
        offsets.append((matches[0], matches[0]+len(expected)))
    if offsets[0][0] != 0 or offsets[-1][1] != len(observed) or any(a[1] != b[0] for a,b in zip(offsets,offsets[1:])):
        return {'status': 'INVALID', 'reason': 'unexpected_or_repeated_or_reordered_speech'}
    return {'status': 'VALID' if reviewed_reference else 'REVIEW_REQUIRED', 'reason': 'reviewed_reference' if reviewed_reference else 'no_acoustic_reference'}


def fixtures():
    def words(text):
        return [dict(text=t, start=i*0.4, end=i*0.4+0.2) for i,t in enumerate(text.split())]
    cases = [
        ('normal', ['hello world', 'next scene'], words('hello world next scene'), True, 'VALID'),
        ('very_short_scene', ['hello', 'world'], words('hello world'), True, 'VALID'),
        ('punctuation', ['Hello, world!', 'Next scene.'], words('hello world next scene'), True, 'VALID'),
        ('natural_pause', ['hello', 'world'], [dict(text='hello',start=0.,end=.2),dict(text='world',start=1.5,end=1.7)], True, 'VALID'),
        ('asr_substitution', ['hello world'], words('hello earth'), True, 'INVALID'),
        ('omitted_word', ['hello big world'], words('hello world'), True, 'INVALID'),
        ('repeated_word', ['hello world'], words('hello hello world'), True, 'INVALID'),
        ('repeated_phrase_boundary', ['hello world', 'hello world'], words('hello world hello world'), True, 'REVIEW_REQUIRED'),
        ('ambiguous_boundary', ['hello', 'hello world'], words('hello hello world'), True, 'REVIEW_REQUIRED'),
        ('truncated_audio', ['hello world'], words('hello'), True, 'INVALID'),
        ('overlap', ['hello world'], [dict(text='hello',start=0.,end=.5),dict(text='world',start=.4,end=.7)], True, 'INVALID'),
        ('no_reference', ['hello world'], words('hello world'), False, 'REVIEW_REQUIRED'),
        ('scene_order_error', ['hello world', 'next scene'], words('next scene hello world'), True, 'INVALID'),
    ]
    result = []
    for name, scenes, w, ref, expected in cases:
        actual = gate(scenes, w, 3., ref)
        assert actual['status'] == expected, (name, actual)
        result.append(dict(name=name, expected=expected, result=actual, passed=True))
    return result


def main():
    OUT.mkdir(exist_ok=True)
    clips = OUT / 'clips'
    clips.mkdir(exist_ok=True)
    report = {'status': 'NOT_YET_PASS', 'method': 'existing ASR structural audit plus sample-exact transition clips; no independent acoustic reference', 'calls': [], 'failure_cases': fixtures()}
    sheet = ['# Scene-boundary review', '', 'Source audio remains continuous. Each clip is an unprocessed source excerpt.',
             'Listen for the last words of the left scene and first words of the right scene.',
             'Check the proposed transition against actual speech. Record OK, adjusted time, or uncertain.',
             'These are candidate timing markers, not audio splice points or independently validated word boundaries.', '']
    fixture = json.loads((RUN.parents[1] / 'fixture-manifest.json').read_text())
    by_id = {s['id']: s['text'] for s in fixture['scenes']}
    for call in (4, 6):
        d = json.loads((RUN/'alignment-closure-v1'/f'call-{call:02d}-alignment.json').read_text())
        path = Path(d['audio_path'])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == d['audio_sha256']
        with wave.open(str(path), 'rb') as wav:
            params = wav.getparams()
            raw = wav.readframes(params.nframes)
        assert params.nchannels == 1 and params.sampwidth == 2
        samples = array.array('h', raw)
        if sys.byteorder != 'little':
            samples.byteswap()
        duration = params.nframes/params.framerate
        w = d['recognized_words']
        structural = all(math.isfinite(x['start']) and math.isfinite(x['end']) and 0 <= x['start'] < x['end'] <= duration for x in w) and all(a['end'] <= b['start'] for a,b in zip(w,w[1:]))
        assert structural
        record = dict(call=call, source_audio_version=d['audio_sha256'], alignment_source=f'../alignment-closure-v1/call-{call:02d}-alignment.json', structurally_valid=True, independent_reference=False, scene_mappings=[], transitions=[])
        for m in d['scene_mappings']:
            record['scene_mappings'].append({**m, 'historical_asr_status': m['boundary_status'], 'boundary_status':'REVIEW_REQUIRED', 'source_audio_version': d['audio_sha256'], 'alignment_version':'boundary-validation-v1', 'validation_reason':'no_independent_acoustic_reference', 'provenance':record['alignment_source']})
        sheet += [f'## Call {call}', '', '| Scenes | Candidate transition | Clip | Last → first approved words | Finding / adjusted time |', '|---|---:|---|---|---|']
        texts = dict(by_id)
        if call == 6:
            texts[20] = fixture['edit']['edited']
        for left,right in zip(d['scene_mappings'],d['scene_mappings'][1:]):
            lo,hi = left['end_time'],right['start_time']
            center = (lo+hi)/2
            a = max(0, round((lo-1.5)*params.framerate))
            b = min(params.nframes, round((hi+1.5)*params.framerate))
            clip = clips/f'call-{call:02d}-scenes-{left["scene_id"]:02d}-{right["scene_id"]:02d}.wav'
            with wave.open(str(clip),'wb') as output:
                output.setparams(params)
                output.writeframes(raw[a*2:b*2])
            ca,cb = max(0,round((center-.01)*params.framerate)),min(params.nframes,round((center+.01)*params.framerate))
            block = samples[ca:cb]
            rms = math.sqrt(sum(x*x for x in block)/max(1,len(block)))/32768
            transition = dict(left_scene=left['scene_id'],right_scene=right['scene_id'],left_word_end=lo,right_word_start=hi,candidate_transition=center,gap_seconds=hi-lo,cut_neighborhood_rms_dbfs=round(20*math.log10(max(rms,1e-12)),2),clip=clip.relative_to(OUT).as_posix(),clip_start_frame=a,clip_end_frame=b,clip_sha256=hashlib.sha256(clip.read_bytes()).hexdigest(),status='REVIEW_REQUIRED')
            record['transitions'].append(transition)
            tail=' '.join(texts[left['scene_id']].split()[-4:]);head=' '.join(texts[right['scene_id']].split()[:4])
            sheet.append(f'| {left["scene_id"]} → {right["scene_id"]} | {center:.3f}s (clip {center-a/params.framerate:.3f}s) | [{clip.name}]({transition["clip"]}) | {tail} → {head} | |')
        report['calls'].append(record)
    (OUT/'validation-results.json').write_text(json.dumps(report,indent=2)+'\n')
    (OUT/'BOUNDARY_REVIEW.md').write_text('\n'.join(sheet)+'\n')
    print('Structural checks: 2/2 sources; failure cases: 13/13; sample-exact transition clips: 62; acoustic reference: unavailable; NOT_YET_PASS')


if __name__ == '__main__':
    main()

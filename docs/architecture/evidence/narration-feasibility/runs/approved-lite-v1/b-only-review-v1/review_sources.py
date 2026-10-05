import hashlib
import json
import wave
from pathlib import Path

root = Path('/Users/kazibadrul/Python Codes/YoutubeAISaaSFinal')
tree = root / 'docs/architecture/evidence/narration-feasibility'
out = tree / 'runs/approved-lite-v1/b-only-review-v1'
out.mkdir(exist_ok=True)
results = json.loads((tree / 'S5-GENERATION-RESULTS.json').read_text())
integrity = []
for c in results['calls']:
    path = root / c['audio']
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with wave.open(str(path), 'rb') as wav:
        frames = wav.readframes(wav.getnframes())
        assert len(frames) == wav.getnframes() * wav.getnchannels() * wav.getsampwidth()
        record = dict(call=c['call'], path=c['audio'], sha256=digest,
                      hash_matches=digest == c['hash'], duration=wav.getnframes()/wav.getframerate(),
                      sample_rate=wav.getframerate(), channels=wav.getnchannels(), sample_width=wav.getsampwidth())
    assert record['hash_matches']
    integrity.append(record)
(out / 'source-integrity.json').write_text(json.dumps(integrity, indent=2)+'\n')
lines = ['# B-only focused fidelity review', '',
         'S5 remains NOT_YET_PASS. These are ASR disagreement windows, not confirmed audio defects.',
         'Listen to the original Call 4 and Call 6 sources. Record the words actually spoken in each window.',
         'Numeric spelling and compound splits may be recognizer formatting; do not infer that material substitutions are harmless.',
         'Review all scene boundaries against waveform/listening before trusting mappings. This list alone cannot close mapping reliability.', '']
for call in (4, 6):
    d = json.loads((tree / f'runs/approved-lite-v1/alignment-closure-v1/call-{call:02}-alignment.json').read_text())
    exp, obs = d['expected_tokens'], d['recognized_words']
    lines += [f'## Call {call}', '', '| Listen window (seconds) | Approved token(s) | Recognized token(s) | Actual words / notes |', '|---|---|---|---|']
    for tag, a, b, c, e in d['alignment']['opcodes']:
        if tag == 'equal':
            continue
        left = max(0, c-1)
        right = min(len(obs)-1, max(c, e))
        start = max(0, obs[left]['start']-1)
        end = min(d['transcription_info']['duration'], obs[right]['end']+1)
        expected = ' '.join(x['text'] for x in exp[a:b]) or '(none)'
        recognized = ' '.join(x['text'] for x in obs[c:e]) or '(none)'
        lines.append(f'| {start:.2f}–{end:.2f} | {expected} | {recognized} | |')
    lines += ['', 'Full-source check: approved words, no truncation/repetition, natural pacing, no clipping.', '']
(out / 'FIDELITY_REVIEW.md').write_text('\n'.join(lines)+'\n')
print('Verified all eight source hashes and PCM decoding; wrote source-integrity.json and FIDELITY_REVIEW.md')

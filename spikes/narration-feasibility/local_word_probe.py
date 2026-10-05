"""Offline cropped recognition witness, not independent forced alignment."""
import os
os.environ['HF_HUB_OFFLINE']='1'
os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
import importlib.util
import json
from pathlib import Path

root=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('closure',root/'spikes/narration-feasibility/local_mapping_closure.py')
closure=importlib.util.module_from_spec(spec);spec.loader.exec_module(closure)
import av
old_open=av.open
def compat(*args,**kwargs):
    kwargs.pop('metadata_errors',None)
    return old_open(*args,**kwargs)
av.open=compat
from faster_whisper import WhisperModel
model_path=Path.home()/'.cache/huggingface/hub/models--Systran--faster-whisper-base/snapshots/ebe41f70d5b6dfa9166e2c581c45c9c0cfc57b66'
assert model_path.is_dir()
model=WhisperModel(str(model_path),device='cpu',compute_type='int8',local_files_only=True)
segments,info=model.transcribe(str(closure.OUT/'call-04-scene18-probe.wav'),language='en',word_timestamps=True,vad_filter=False,beam_size=5,temperature=0.,condition_on_previous_text=False)
words=[dict(text=w.word.strip(),start=w.start+92.1,end=w.end+92.1,probability=w.probability) for s in segments for w in s.words or []]
(closure.OUT/'scene18-probe-recognition.json').write_text(json.dumps(dict(method='same cached Whisper base, cropped input, no text prompt',source_offset=92.1,words=words,independent_acoustic_reference=False),indent=2)+'\n')
print(json.dumps(words))

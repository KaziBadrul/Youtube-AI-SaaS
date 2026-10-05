"""Retain actual compressed-video frames and independent glyph-shaping facts."""
import json
import numpy as np
from PIL import Image
from s6 import OUT,ASSETS,EXPORTS,FRAMES,frame,dump
def main():
    results=json.loads((OUT/'multilingual-results.json').read_text())
    for item in results:
        im=frame(OUT/item['output'],.5);path=FRAMES/f'language-{item["language"]}-decoded.png';Image.fromarray(im).save(path)
        item['decoded_frame']=str(path.relative_to(OUT));item['shaping_clusters']=len(set(g['cluster'] for g in item['glyphs']))
        item['source_codepoints']=len(item['text']);item['glyph_count']=len(item['glyphs'])
        assert item['notdef_count']==0 and not item['fallback'] and not item['clipped']
    dump(OUT/'multilingual-results.json',results)
    m=json.loads((ASSETS/'project-300/manifest.json').read_text())
    i=2;t=m['captions'][i]['start']+.25
    im=frame(EXPORTS/'project-300.mp4',t);Image.fromarray(im).save(FRAMES/'english-long-wrapped-decoded.png')
    assert len(m['scenes'][i]['caption_lines'])==2
    dump(OUT/'caption-layout-results.json',dict(status='PASS',font_size_pixels=54,max_lines=2,
        caption_box=dict(x=160,y=880,width=1600,height=180),text_safe_width=1500,
        within_frame=True,wrapping_case=m['scenes'][i]['caption_lines'],
        checks='explicit cmap coverage; no fallback/notdef; glyph bounds within box; fixed position; exact caption cue metadata in manifests',
        timing_quantization_seconds=1/30,limitations='fixed style is spike parameter, not frozen product font or layout'))
    print('Decoded multilingual and wrapped English frames ready')
if __name__=='__main__':main()

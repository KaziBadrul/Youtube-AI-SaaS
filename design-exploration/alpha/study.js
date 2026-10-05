const $ = id => document.getElementById(id);
const theme = $('theme'), system = matchMedia('(prefers-color-scheme: dark)');
let preference = 'system';
try { preference = localStorage.getItem('alpha-study-theme') || 'system'; } catch {}
if (!['system','light','dark'].includes(preference)) preference = 'system';
function applyTheme(){ document.documentElement.dataset.theme = preference === 'system' ? (system.matches ? 'dark' : 'light') : preference; }
theme.value = preference; applyTheme();
theme.onchange = () => { preference = theme.value; try { localStorage.setItem('alpha-study-theme', preference); } catch {} applyTheme(); };
system.addEventListener('change', applyTheme);
function notice(title,text){ $('notice-title').textContent=title; $('notice-text').textContent=text; $('notice').showModal(); }
document.querySelectorAll('[data-notice]').forEach(b=>b.onclick=()=>notice('Demonstration only',b.dataset.notice));
const params=new URLSearchParams(location.search);
if($('idea')){
 const draft={topic:$('idea').value,script:''}; let mode='topic';
 function inputMode(next){draft[mode]=$('idea').value;mode=next;$('idea').value=draft[mode];$('input-label').textContent=mode==='topic'?'Video idea':'Your complete script';$('topic-tab').setAttribute('aria-pressed',mode==='topic');$('script-tab').setAttribute('aria-pressed',mode==='script');}
 $('topic-tab').onclick=()=>inputMode('topic');$('script-tab').onclick=()=>inputMode('script');
 $('create-demo').onclick=()=>{location.href='progress.html?review='+($('review').checked?'1':'0');};
}
if($('progress-title')){
 const states={queued:['Waiting for your turn.','Your prepared example is safe.','Queued study: position would appear when known. No completion time is promised.'],partial:['One scene needs attention.','Successful work stays in your project.','Partial-failure study: Scene 14 has no usable image. Retry or replace it before rendering.'],budget:['Production is paused.','Your completed scenes are preserved.','Budget-blocked study: shared Alpha capacity is unavailable. No new paid work starts; there is no upgrade or payment flow.'],unknown:['We’re checking this request.','Saved work is preserved while the outcome is reconciled.','Unknown-outcome study: usage remains pending. No duplicate paid retry until the owner establishes a safe outcome.'],render:['Rendering your video.','Content editing is locked until rendering stops.','Render-lock study: viewing and cancellation remain available. This page does not run FFmpeg.']};
 const state=states[params.get('state')];if(state){$('progress-title').textContent=state[0];$('progress-copy').textContent=state[1];$('state-message').textContent=state[2];$('stage-active').textContent='State demonstration';}
 $('progress-next').textContent=params.get('review')==='1'?'Review scenes before rendering →':'Open prepared video and scenes →';
}
if($('scene-data')){
 const data=JSON.parse($('scene-data').textContent), edits=new Map();let selected=0, end=0;
 const audio=$('narration'), video=$('video-dialog').querySelector('video');
 const time=n=>`${String(Math.floor(n/60)).padStart(2,'0')}:${String(Math.floor(n%60)).padStart(2,'0')}`;
 function choose(index){audio.pause();selected=Math.max(0,Math.min(data.scenes.length-1,index));const s=data.scenes[selected],t=data.timings.find(x=>x.scene===s.id);$('scene-title').textContent=`Scene ${String(s.id).padStart(2,'0')}`;$('scene-image').src=`../../demo-video-example/images/${s.id}.png`;$('scene-image').alt=`Scene ${s.id} example illustration`;$('words').value=edits.get(s.id)||s.narration;$('visual').value=s.visual;$('caption').value=s.narration;$('duration').value=t?.duration||'';$('scene-time').textContent=t?`${time(t.start)} – ${time(t.end)}`:'Timing unavailable';$('preview-caption').textContent=s.narration;$('scene-context-text').textContent=s.visual;$('edit-warning').hidden=!edits.has(s.id);$('previous').disabled=selected===0;$('next').disabled=selected===data.scenes.length-1;document.querySelectorAll('[data-scene]').forEach(b=>b.setAttribute('aria-pressed',Number(b.dataset.scene)===selected));}
 document.querySelectorAll('[data-scene]').forEach(b=>b.onclick=()=>{choose(Number(b.dataset.scene));if(innerWidth<=1100){$('scenes-panel').classList.remove('open');$('scenes-toggle').setAttribute('aria-expanded','false');$('scenes-toggle').focus();}});
 $('next').onclick=()=>choose(selected+1);$('previous').onclick=()=>choose(selected-1);
 $('words').oninput=()=>{const s=data.scenes[selected];if($('words').value===s.narration)edits.delete(s.id);else edits.set(s.id,$('words').value);$('edit-warning').hidden=!edits.has(s.id);$('save-state').textContent='Local study edit · Not saved to a project';};
 $('listen').onclick=()=>{const t=data.timings.find(x=>x.scene===data.scenes[selected].id);if(!t){notice('Timing unavailable','No verified scene range is available.');return;}if(!audio.paused){audio.pause();return;}audio.currentTime=t.start;end=t.end;audio.play().catch(()=>notice('Audio unavailable','The prepared audio could not be played.'));};
 audio.ontimeupdate=()=>{if(audio.currentTime>=end)audio.pause();};audio.onplay=()=>{$('listen').textContent='Ⅱ Pause scene';};audio.onpause=()=>{$('listen').textContent='▶ Listen to scene';};
 const switchTab=visual=>{$('narration-view').hidden=visual;$('visual-view').hidden=!visual;$('narration-tab').setAttribute('aria-pressed',!visual);$('visual-tab').setAttribute('aria-pressed',visual);};
 $('narration-tab').onclick=()=>switchTab(false);$('visual-tab').onclick=()=>switchTab(true);
 $('regenerate').onclick=()=>notice('Review narration scope','A live correction may regenerate several scenes sharing narration. The reviewed plan would list affected scenes, voice, estimated usage and maximum spending. No segmentation policy or alternate audio is supplied in this study; no regeneration occurs.');
 $('history').onclick=()=>notice('Narration history','The supplied recording is the only available audio version. Restoration would show its associated words and voice before approval. No previous version or price is invented here.');
 $('render-study').onclick=()=>notice(edits.size?'Render needs current narration':'Prepared export available',edits.size?'Edited narration needs fresh audio, timing and captions before rendering. The original MP4 remains accessible; this study does not render.':'In manual review you would now render the current video. The static study supplies an existing MP4; use Play full video to inspect it.');
 $('full-video').onclick=()=>{audio.pause();$('video-dialog').showModal();};$('close-video').onclick=()=>{$('video-dialog').close();};$('video-dialog').addEventListener('close',()=>video.pause());
 $('scenes-toggle').onclick=()=>{const open=$('scenes-panel').classList.toggle('open');$('scenes-toggle').setAttribute('aria-expanded',open);if(open)$('close-scenes').focus();};
 function closeScenes(){$('scenes-panel').classList.remove('open');$('scenes-toggle').setAttribute('aria-expanded','false');$('scenes-toggle').focus();}
 $('close-scenes').onclick=closeScenes;document.addEventListener('keydown',e=>{if(e.key==='Escape'&&$('scenes-panel').classList.contains('open'))closeScenes();});
 choose(0);
}

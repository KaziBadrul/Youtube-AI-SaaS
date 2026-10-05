const $ = id => document.getElementById(id);
const theme = $('theme'), system = matchMedia('(prefers-color-scheme: dark)');
let preference = 'system';
try { preference = localStorage.getItem('alpha-prototypes-theme') || 'system'; } catch {}
if (!['system','light','dark'].includes(preference)) preference = 'system';
function applyTheme(){ document.documentElement.dataset.theme = preference === 'system' ? (system.matches ? 'dark' : 'light') : preference; }
theme.value = preference; applyTheme();
theme.onchange = () => { preference = theme.value; try { localStorage.setItem('alpha-prototypes-theme', preference); } catch {} applyTheme(); };
system.addEventListener('change', applyTheme);
function notice(title,text){ $('notice-title').textContent=title; $('notice-text').textContent=text; $('notice').showModal(); }
document.querySelectorAll('[data-notice]').forEach(b=>b.onclick=()=>notice('Demonstration only',b.dataset.notice));
const params=new URLSearchParams(location.search);
if($('idea')){ if(params.get('customize')==='1') $('customize').open=true;
 const draft={topic:$('idea').value,script:''}; let mode='topic';
 function inputMode(next){draft[mode]=$('idea').value;mode=next;$('idea').value=draft[mode];$('input-label').textContent=mode==='topic'?'What should your video be about?':'Your complete script';$('topic-tab').setAttribute('aria-pressed',mode==='topic');$('script-tab').setAttribute('aria-pressed',mode==='script');}
 $('topic-tab').onclick=()=>inputMode('topic');$('script-tab').onclick=()=>inputMode('script');
 $('create-demo').onclick=()=>{notice('Prepared workflow', 'Your idea → script → scenes → images and narration → timing → video. This is a prepared demonstration, not live production. Close this dialog, then open Projects or the workspace to inspect the example.');};
}
if($('scene-data')){
 const imageKept=new Set();
 const data=JSON.parse($('scene-data').textContent), edits=new Map();let selected=0, end=0;
 const audio=$('narration'), video=$('video-dialog').querySelector('video');
 const time=n=>`${String(Math.floor(n/60)).padStart(2,'0')}:${String(Math.floor(n%60)).padStart(2,'0')}`;
 function refreshStates(){
  const id=data.scenes[selected].id,changed=edits.has(id),review=changed&&!imageKept.has(id);
  $('edit-warning').hidden=!changed; $('image-review').hidden=!review;
  $('asset-state').textContent=review?'Image needs review':'Current image';
  $('scope-note').hidden=id!==8;
  const issues=[];for(const id of edits.keys()){issues.push({id,visual:false,text:`Scene ${id} · Narration needs regeneration`});if(!imageKept.has(id))issues.push({id,visual:true,text:`Scene ${id} · Image needs review`});}
  $('readiness-label').textContent=issues.length?`${issues.length} issues before rendering`:'Render ready';
  $('readiness-list').replaceChildren(...issues.map(issue=>{const li=document.createElement('li'),b=document.createElement('button');b.textContent=issue.text;b.className='issue-link';b.onclick=()=>{choose(issue.id-1);switchTab(issue.visual);const target=issue.visual?$('keep-image'):$('words');target.focus();target.scrollIntoView({block:'nearest',behavior:'instant'});window.motionPulse?.(target);};li.append(b);return li;}));
  document.querySelectorAll('[data-scene]').forEach(b=>{const id=data.scenes[Number(b.dataset.scene)].id;b.classList.toggle('needs-attention',edits.has(id));b.setAttribute('aria-label',`Scene ${String(id).padStart(2,'0')}${edits.has(id)?', needs attention':''}: ${data.scenes[Number(b.dataset.scene)].narration}`);});
 }
 function choose(index){audio.pause();selected=Math.max(0,Math.min(data.scenes.length-1,index));const s=data.scenes[selected],t=data.timings.find(x=>x.scene===s.id);$('scene-title').textContent=`Scene ${String(s.id).padStart(2,'0')}`;$('scene-image').src=`../../demo-video-example/images/${s.id}.png`;$('scene-image').alt=`Scene ${s.id} example illustration`;$('words').value=edits.get(s.id)||s.narration;$('visual').value=s.visual;$('caption').value=s.narration;$('duration').value=t?.duration||'';$('scene-time').textContent=t?`${time(t.start)} – ${time(t.end)}`:'Timing unavailable';$('preview-caption').textContent=s.narration;$('scene-context-text').textContent=s.visual;$('edit-warning').hidden=!edits.has(s.id);refreshStates();$('previous').disabled=selected===0;$('next').disabled=selected===data.scenes.length-1;document.querySelectorAll('[data-scene]').forEach(b=>b.setAttribute('aria-pressed',Number(b.dataset.scene)===selected));document.dispatchEvent(new Event('scene-selected'));}
 document.querySelectorAll('[data-scene]').forEach(b=>b.onclick=()=>{choose(Number(b.dataset.scene));if(innerWidth<=1100){$('scenes-panel').classList.remove('open');$('scenes-toggle').setAttribute('aria-expanded','false');$('scenes-toggle').focus();}});
 $('next').onclick=()=>choose(selected+1);$('previous').onclick=()=>choose(selected-1);
 $('words').oninput=()=>{const s=data.scenes[selected];if($('words').value===s.narration)edits.delete(s.id);else edits.set(s.id,$('words').value);$('edit-warning').hidden=!edits.has(s.id);imageKept.delete(s.id);refreshStates();$('save-state').textContent='Edited in this preview';};
 $('listen').onclick=()=>{const t=data.timings.find(x=>x.scene===data.scenes[selected].id);if(!t){notice('Timing unavailable','No verified scene range is available.');return;}if(!audio.paused){audio.pause();return;}audio.currentTime=t.start;end=t.end;audio.play().catch(()=>notice('Audio unavailable','The prepared audio could not be played.'));};
 audio.ontimeupdate=()=>{if(audio.currentTime>=end)audio.pause();};audio.onplay=()=>{$('listen').textContent='Ⅱ Pause scene';};audio.onpause=()=>{$('listen').textContent='▶ Listen to scene';};
 const switchTab=visual=>{$('narration-view').hidden=visual;$('visual-view').hidden=!visual;$('narration-tab').setAttribute('aria-pressed',!visual);$('visual-tab').setAttribute('aria-pressed',visual);window.motionPulse?.($(visual?'visual-view':'narration-view'));};
 $('narration-tab').onclick=()=>switchTab(false);$('visual-tab').onclick=()=>switchTab(true);
 $('regenerate').onclick=()=>{const panel=$('operation-preview');panel.hidden=false;panel.dataset.state='queued';$('operation-state').textContent='Queued · Narration update preview';window.motionPulse?.(panel);};
 $('history').onclick=()=>{$('history-words').textContent=data.scenes[selected].narration;$('history-sheet').showModal();};
 $('history-close').onclick=()=>{$('history-sheet').close();$('history').focus();};
 $('history-listen').onclick=()=>{$('listen').click();};
 $('render-study').onclick=()=>notice(edits.size?'Render needs current narration':'Prepared export available',edits.size?'Edited narration needs fresh audio, timing and captions before rendering. The original MP4 remains accessible; this study does not render.':'In manual review you would now render the current video. The static study supplies an existing MP4; use Play full video to inspect it.');
 $('full-video').onclick=()=>{audio.pause();$('video-dialog').showModal();};$('close-video').onclick=()=>{$('video-dialog').close();};$('video-dialog').addEventListener('close',()=>video.pause());
 $('scenes-toggle').onclick=()=>{const open=$('scenes-panel').classList.toggle('open');$('scenes-toggle').setAttribute('aria-expanded',open);if(open)$('close-scenes').focus();};
 function closeScenes(){$('scenes-panel').classList.remove('open');$('scenes-toggle').setAttribute('aria-expanded','false');$('scenes-toggle').focus();}
 $('close-scenes').onclick=closeScenes;document.addEventListener('keydown',e=>{if(e.key==='Escape'&&$('scenes-panel').classList.contains('open'))closeScenes();});
if(params.get('ready')!=='1')edits.set(8,'Your parents felt like mythical creatures when you were small.');
 choose(7);
 $('keep-image').onclick=()=>{imageKept.add(data.scenes[selected].id);refreshStates();};
}

if($('export-study')) $('export-study').onclick=()=>notice('Previous export','The original prepared export remains available through Play full video. It does not reflect the edited narration.');

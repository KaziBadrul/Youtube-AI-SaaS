// Focused same-origin enhancement, not a frontend application or generation engine.
const byId=id=>document.getElementById(id);
let current=null,job=null,saveQueue=Promise.resolve(),saveTimer,context='narration';
const csrf=()=>document.cookie.split('; ').find(c=>c.startsWith('csrftoken='))?.split('=')[1];
async function request(path,body){const r=await fetch(path,{credentials:'same-origin',method:body?'POST':'GET',headers:body?{'Content-Type':'application/json','X-CSRFToken':csrf()}: {},body:body?JSON.stringify(body):undefined});return {status:r.status,data:await r.json()};}
async function select(id){clearTimeout(saveTimer);await saveQueue;const r=await request('/scene/'+id);if(r.status!==200)return;current=r.data;byId('scene-title').textContent='Scene '+id;byId('words').value=current.words;byId('audio').src='/asset/'+id;document.querySelectorAll('[data-scene]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.scene==id));}
async function save(){const id=current.id,text=byId('words').value;saveQueue=saveQueue.then(async()=>{const r=await request('/save/'+id,{rev:current.rev,words:text});if(r.status===200){current=r.data.scene;byId('save-state').textContent='Saved · Audio outdated';}else byId('save-state').textContent=r.status===423?'Rendering: editing locked':'Conflict: preserve your input and reload current version';});return saveQueue;}
byId('words').addEventListener('input',()=>{if(context!=='narration')return;clearTimeout(saveTimer);saveTimer=setTimeout(save,250);});
document.querySelectorAll('[data-scene]').forEach(b=>b.onclick=async()=>{if(current && byId('words').value!==current.words && context==='narration')await save();await select(b.dataset.scene);});
async function enqueue(kind){await saveQueue;const r=await request('/command/'+(current?.id||1),{kind,key:crypto.randomUUID(),mode:byId('mode').value,text:byId('idea').value});if(r.status===202){job=r.data.job;byId('progress').textContent='Queued';poll();}}
byId('create').onclick=()=>{if(byId('idea').value.trim())enqueue('create');};
byId('idea').addEventListener('paste',()=>document.querySelector('#composer details').open=true);
byId('regenerate').onclick=async()=>{clearTimeout(saveTimer);if(current && byId('words').value!==current.words)await save();const r=await request('/scope/'+current.id);byId('scope-message').textContent=r.data.message;byId('scope-dialog').showModal();};
byId('confirm-regenerate').onclick=()=>{byId('scope-dialog').close();enqueue('regenerate');};
byId('render').onclick=()=>enqueue('render');byId('cancel').onclick=()=>job&&request('/cancel/'+job,{});
async function poll(){if(!job)return;const r=await request('/progress/'+job);if(r.status!==200)return;const state=r.data.job.state;byId('progress').textContent=state+' · '+(r.data.events.at(-1)?.stage||'');const locked=r.data.job.kind==='render'&&['running','cancelling','recovery_required'].includes(state);byId('words').disabled=locked;byId('regenerate').disabled=locked;byId('lock-state').textContent=locked?'Rendering: content editing is locked':'';if(!['completed','cancelled','failed'].includes(state))setTimeout(poll,300);}
byId('narration-tab').onclick=()=>{context='narration';byId('words-label').textContent='Scene narration';byId('words').value=current?.words||'';};
byId('visual-tab').onclick=()=>{context='visual';byId('words-label').textContent='Visual description (read-only fixture)';byId('words').value='Prepared still image';};
select(document.querySelector('[data-scene]')?.dataset.scene||1);

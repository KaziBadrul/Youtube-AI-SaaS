// Disposable one-tap creation demonstration: no provider calls.
(()=>{
 const get=id=>document.getElementById(id), input=get('composer-input'), options=get('composer-options'), toggle=get('more-toggle'), mode=get('input-use');
 function expand(open){window.animateDisclosure?.(options,open);if(!window.animateDisclosure)options.hidden=!open;toggle.setAttribute('aria-expanded',String(open));toggle.textContent=open?'See less −':'See more ＋';}
 toggle.onclick=()=>expand(options.hidden);
 input.oninput=()=>{document.querySelector('.composer').classList.toggle('has-input',!!input.value.trim());get('composer-continue').disabled=!input.value.trim();};
 mode.onchange=()=>{get('topic-duration').hidden=mode.value==='script';get('script-duration').hidden=mode.value!=='script';document.querySelector('.composer-help').textContent=mode.value==='script'?'Using your approved script. Your words are preserved.':'Using your text as an idea. For a complete script, choose “My approved script” in See more.';};
 input.addEventListener('paste',()=>expand(true)); // expose explicit interpretation; never classify pasted text.
 get('composer-continue').onclick=()=>{
  if(!input.value.trim())return;
  expand(false);input.readOnly=true;mode.disabled=true;toggle.disabled=true;
  get('composer-continue').disabled=true;get('composer-continue').textContent='Generating…';
  get('creation-progress').hidden=false;get('creation-status').hidden=false;get('creation-status').textContent='Queued · Progress preview';get('creation-progress').dataset.state='queued';window.motionPulse?.(get('creation-progress'));
  document.querySelector('.composer-help').textContent='Prepared progress demonstration — no live generation or spending.';
 };
 const query=new URLSearchParams(location.search);if(query.get('customize')==='1'||query.get('more')==='1')expand(true);
 if(query.get('example')==='script'){input.value='At some point, you realize your parents are ordinary people. They have hopes, worries and unanswered questions, just like you.';mode.value='script';mode.onchange();input.oninput();}
})();

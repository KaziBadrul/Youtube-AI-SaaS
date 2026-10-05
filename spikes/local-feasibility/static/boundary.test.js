const fs=require('fs'),vm=require('vm'),assert=require('assert');
(async()=>{
 const nodes=new Map();function element(id){if(!nodes.has(id))nodes.set(id,{id,value:'',textContent:'',disabled:false,events:{},addEventListener(n,f){this.events[n]=f},setAttribute(n,v){this[n]=v},showModal(){this.open=true},close(){this.open=false}});return nodes.get(id);}
 const buttons=[element('scene1'),element('scene2')];buttons[0].dataset={scene:'1'};buttons[1].dataset={scene:'2'};
 const scene={1:{id:1,words:'One',rev:0},2:{id:2,words:'Two',rev:0}};const requests=[],timers=[];let render=false;
 const fetch=async(path,opts)=>{requests.push({path,opts});let status=200,data;
  if(path.startsWith('/scene/'))data={...scene[path.split('/').at(-1)]};
  if(path.startsWith('/save/')){const id=path.split('/').at(-1),b=JSON.parse(opts.body);assert.equal(b.rev,scene[id].rev);scene[id]={id:+id,words:b.words,rev:b.rev+1};data={scene:{...scene[id]},result:'saved'};}
  if(path.startsWith('/scope/'))data={message:'Updates Scenes 1–2'};
  if(path.startsWith('/command/')){render=JSON.parse(opts.body).kind==='render';status=202;data={job:'j'};}
  if(path.startsWith('/progress/'))data={job:{state:render?'running':'completed',kind:render?'render':'generate'},events:[{stage:'Creating narration'}]};
  if(path.startsWith('/cancel/'))data={state:'cancelling'};
  return {status,json:async()=>data};
 };
 const document={cookie:'csrftoken=test',getElementById:element,querySelectorAll:()=>buttons,querySelector:s=>s.includes('details')?element('details'):buttons[0]};
 vm.runInNewContext(fs.readFileSync(__dirname+'/boundary.js','utf8'),{document,fetch,crypto:{randomUUID:()=>String(requests.length)},setTimeout(f,ms){timers.push({f,ms});return timers.length},clearTimeout(){},Promise,console});
 const flush=()=>new Promise(resolve=>setImmediate(resolve));await flush();assert.equal(element('words').value,'One');
 element('words').value='Changed one';element('words').events.input();await timers.find(t=>t.ms===250).f();assert.equal(scene[1].words,'Changed one');assert.equal(scene[2].words,'Two');
 await buttons[1].onclick();assert.equal(element('words').value,'Two');assert.equal(element('audio').src,'/asset/2');
 element('idea').events.paste();assert.equal(element('details').open,true);
 await element('regenerate').onclick();assert.equal(element('scope-dialog').open,true);assert.equal(element('scope-message').textContent,'Updates Scenes 1–2');
 element('confirm-regenerate').onclick();await flush();assert.equal(element('scope-dialog').open,false);
 element('render').onclick();await flush();assert.equal(element('words').disabled,true);assert.equal(element('regenerate').disabled,true);
 element('cancel').onclick();await flush();assert(requests.some(r=>r.path==='/cancel/j'));
 assert(requests.filter(r=>r.opts.method==='POST').every(r=>r.opts.headers['X-CSRFToken']==='test'));
 console.log('PASS: enhancement selection, debounce/serialized autosave, paste disclosure, scope confirmation, polling/render lock, cancel and CSRF');
})().catch(e=>{console.error(e);process.exitCode=1});

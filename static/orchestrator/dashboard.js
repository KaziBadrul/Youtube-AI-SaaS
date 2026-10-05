'use strict';
const el = id => document.getElementById(id);
const put = (id, text) => { el(id).textContent = text ?? ''; };
async function update() {
  try {
    const response = await fetch('/api/status', {cache:'no-store'});
    if (!response.ok) throw new Error('Monitor unavailable');
    const s = await response.json();
    put('mode',s.mode); el('mode').className=s.mode;
    put('task',s.active_task ? `${s.active_task.id}: ${s.active_task.title}` : 'No active task');
    put('phase',s.active_task?.phase);
    const details = {Status:s.active_task?.status ?? 'IDLE',Attempt:s.attempt ?? 0,Repairs:s.repair_count ?? 0,'Elapsed (seconds)':s.elapsed_seconds ?? 0,'Reviewer verdict':s.reviewer_verdict ?? '—','Codex exit':s.last_codex_exit_code ?? '—','OpenCode exit':s.last_opencode_exit_code ?? '—'};
    el('details').replaceChildren();
    for(const [key,value] of Object.entries(details)){const a=document.createElement('dt');a.textContent=key;const b=document.createElement('dd');b.textContent=value;el('details').append(a,b);}
    put('blocker',s.blocker); put('progress',`${s.completed} completed · ${s.remaining} remaining`);
    put('commit',`Latest accepted commit: ${s.latest_commit ?? 'none'}`);
    put('codex',s.codex_output || 'No output yet.');put('reviewer',s.reviewer_output || 'No output yet.');
    for(const [id,actor] of [['codex-process','codex'],['reviewer-process','reviewer']]) put(id,s.process?.actor===actor?`RUNNING · PID ${s.process.pid} · PGID ${s.process.pgid}`:'idle');
    put('events',(s.events??[]).map(e=>`${e.timestamp} ${e.task_id??'—'} ${e.actor} ${e.event_type}: ${e.message??''}`).join('\n'));
    el('tasks').replaceChildren();
    for(const task of s.tasks??[]){const row=document.createElement('tr');for(const text of [`${task.id} ${task.title}${task.optional?' (conditional)':''}`,task.status,`${task.dependencies_passed}/${task.dependencies.length} ${task.dependencies.join(', ') || 'None'}`]){const cell=document.createElement('td');cell.textContent=text;row.append(cell);}row.children[1].className=task.status;el('tasks').append(row);}
    put('updated',`Updated ${new Date().toLocaleTimeString()}`);
  }catch(error){put('mode','DISCONNECTED');put('updated',error.message);}
}
update();setInterval(update,2000);

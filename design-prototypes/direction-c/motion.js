// Disposable motion study. No networking, generation, render or persistence.
(()=>{
 const reduced=matchMedia('(prefers-reduced-motion: reduce)'), animations=new WeakMap();
 reduced.addEventListener('change',()=>{if(reduced.matches)document.getAnimations().forEach(animation=>{if(animation.effect?.getTiming().iterations!==Infinity){try{animation.finish();}catch{animation.cancel();}}});});
 window.motionPulse=(element)=>{
  if(!element||reduced.matches)return;
  animations.get(element)?.cancel();
  const animation=element.animate([{opacity:.55,transform:'translateY(3px)'},{opacity:1,transform:'translateY(0)'}],{duration:160,easing:'ease-out'});
  animations.set(element,animation);
 };
 window.animateDisclosure=(element,open)=>{
  animations.get(element)?.cancel();
  if(reduced.matches){element.hidden=!open;element.style.height='';element.style.overflow='';return;}
  const start=element.hidden?0:element.getBoundingClientRect().height;
  element.hidden=false;const end=open?element.scrollHeight:0;
  element.style.overflow='hidden';
  const animation=element.animate([{height:start+'px',opacity:open?.45:1},{height:end+'px',opacity:open?1:0}],{duration:200,easing:'cubic-bezier(.2,.7,.2,1)'});
  animations.set(element,animation);
  animation.onfinish=()=>{element.hidden=!open;element.style.overflow='';};
  animation.oncancel=()=>{element.style.overflow='';};
 };
 // Native disclosure semantics remain; only the body animates.
 document.querySelectorAll('details').forEach(details=>{
  const summary=details.querySelector(':scope > summary');if(!summary)return;
  const body=document.createElement('div');body.className='disclosure-body';
  [...details.childNodes].filter(n=>n!==summary).forEach(n=>body.append(n));details.append(body);body.hidden=!details.open;
  summary.addEventListener('click',event=>{
   event.preventDefault();const open=summary.getAttribute('aria-expanded')!=='true';summary.setAttribute('aria-expanded',String(open));
   if(open)details.open=true;
   window.animateDisclosure(body,open);
   if(!open){if(reduced.matches)details.open=false;else{const animation=animations.get(body);if(animation)animation.addEventListener('finish',()=>{if(summary.getAttribute('aria-expanded')==='false')details.open=false;},{once:true});}}
  });summary.setAttribute('aria-expanded',String(details.open));
 });
 document.addEventListener('scene-selected',()=>{window.motionPulse(document.querySelector('.scene-image'));window.motionPulse(document.querySelector('.inspector'));});
 document.querySelectorAll('[data-demo-state]').forEach(button=>button.addEventListener('click',()=>{
  const panel=button.closest('.operation-preview'),label=panel.querySelector('[role=status]'),state=button.dataset.demoState;
  panel.dataset.state=state;
  label.textContent={running:'Running · Preparing narration',complete:'Complete · Motion preview only',failed:'Could not finish · Your existing work is preserved'}[state];
  window.motionPulse(label);
 }));
 // Pause, slide one position, settle, pause. Cloned edge slides hide loop resets.
 const carousel=document.querySelector('.carousel');if(!carousel)return;
 const track=carousel.querySelector('.carousel-track'),slides=[...track.children],count=slides.length;
 const first=slides[0].cloneNode(true),last=slides[count-1].cloneNode(true);
 first.setAttribute('aria-hidden','true');last.setAttribute('aria-hidden','true');track.prepend(last);track.append(first);const second=slides[1].cloneNode(true);second.setAttribute('aria-hidden','true');track.append(second);const third=slides[2].cloneNode(true);third.setAttribute('aria-hidden','true');track.append(third);
 let index=1,step=0,timer,sliding=false,userPaused=false,hover=false,focused=false;
 const pause=document.getElementById('carousel-pause'),status=document.getElementById('carousel-status');
 function schedule(){clearTimeout(timer);if(!reduced.matches&&!userPaused&&!hover&&!focused&&!document.hidden)timer=setTimeout(()=>move(1,false),2400);}
 function position(animate){[...track.children].forEach((slide,i)=>{slide.classList.toggle('is-center',i===index+1);slide.classList.toggle('instant-position',!animate);});track.style.transition=animate&&!reduced.matches?'transform 500ms cubic-bezier(.25,.65,.25,1)':'none';track.style.transform=`translateX(${-index*step}px)`;}
 function measure(){if(index>count)index=1;if(index<1)index=count;const slide=track.children[1];step=slide.getBoundingClientRect().width+parseFloat(getComputedStyle(track).gap||0);position(false);sliding=false;schedule();}
 function settle(){if(index>count){index=1;position(false);}if(index<1){index=count;position(false);}sliding=false;schedule();}
 function move(direction,manual){if(sliding)return;clearTimeout(timer);sliding=true;index+=direction;position(true);if(manual)status.textContent=`Image ${((index+count)%count)+1} of ${count}`;if(reduced.matches)settle();}
 track.addEventListener('transitionend',event=>{if(event.propertyName==='transform')settle();});
 document.getElementById('carousel-prev').onclick=()=>move(-1,true);document.getElementById('carousel-next').onclick=()=>move(1,true);
 pause.onclick=()=>{userPaused=!userPaused;pause.textContent=userPaused?'Play':'Pause';pause.setAttribute('aria-label',userPaused?'Resume automatic carousel':'Pause automatic carousel');schedule();};
 carousel.addEventListener('mouseenter',()=>{hover=true;clearTimeout(timer);});carousel.addEventListener('mouseleave',()=>{hover=false;schedule();});
 carousel.addEventListener('focusin',()=>{focused=true;clearTimeout(timer);});carousel.addEventListener('focusout',event=>{if(!carousel.contains(event.relatedTarget)){focused=false;schedule();}});
 carousel.addEventListener('touchstart',()=>{userPaused=true;pause.textContent='Play';pause.setAttribute('aria-label','Resume automatic carousel');clearTimeout(timer);},{passive:true});
 document.addEventListener('visibilitychange',schedule);
 function motionPreference(){pause.hidden=reduced.matches;measure();}
 reduced.addEventListener('change',motionPreference);new ResizeObserver(measure).observe(carousel.querySelector('.carousel-viewport'));motionPreference();
})();

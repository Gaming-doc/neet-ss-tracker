p='tracker.tpl.html'; t=open(p).read()
def rep(a,b):
    global t
    assert t.count(a)==1,(a[:90],t.count(a)); t=t.replace(a,b)
# ---------- CSS ----------
rep(".item.running{box-shadow:inset 0 0 0 2px var(--hc)}", """.item.running{box-shadow:inset 0 0 0 2px var(--hc)}
.item.paused{box-shadow:inset 0 0 0 2px var(--line)}
.ab.pause{border-color:var(--warn)}
.plog{flex-basis:100%;font-size:12px;color:var(--muted)}
.plog summary{cursor:pointer;color:var(--accent);font-weight:700;width:max-content;max-width:100%}
.plog span{display:block;font-family:var(--f-mono);font-variant-numeric:tabular-nums;padding:1px 0}""")
# ---------- helpers ----------
rep('''function planM(v){''','''// pauses are stored as [{f: pausedAt, t: resumedAt}] on each module's actual record
function pauses(a){ return a && Array.isArray(a.p) ? a.p : []; }
function isPaused(a){ const p=pauses(a); return !!(a && a.s && !a.e && p.length && !p[p.length-1].t); }
function pausedM(a,now){ const end=a.e||now; return pauses(a).reduce((s,x)=>s+mins(x.f,x.t||end),0); }
function activeM(a,now){ now=now||new Date().toISOString(); if(!a||!a.s) return 0; return Math.max(0, mins(a.s,a.e||now)-pausedM(a,now)); }
function pauseLog(a){
  const p=pauses(a); if(!p.length) return "";
  const now=new Date().toISOString();
  return `<details class="plog"><summary>${p.length} pause${p.length>1?"s":""} · ${fmtM(pausedM(a,now))}</summary>${p.map((x,k)=>`<span>${k+1}. ${hm(x.f)} → ${x.t?hm(x.t):"now"} · ${fmtM(mins(x.f,x.t||a.e||now))}</span>`).join("")}</details>`;
}
function planM(v){''')
rep('''  const diff=mins(a.s,a.e)-pm;''','''  const diff=activeM(a)-pm;''')
rep('''  if(!a.e) return `<span class="run">Started <b>${hm(a.s)}</b> · <b class="live" data-since="${a.s}">${fmtM(mins(a.s,new Date().toISOString()))}</b> so far</span><button class="ab end" data-act="e">■ End now</button><button class="ab x" data-act="x" aria-label="Clear the start time">×</button>`;
  const v=vsPlan(id);
  return `<span class="did">Did <b>${hm(a.s)}–${hm(a.e)}</b> · ${fmtM(mins(a.s,a.e))}${v?" · "+v:""}</span><button class="ab x" data-act="x" aria-label="Clear the actual times">×</button>`;''',
'''  if(!a.e){
    const pz=isPaused(a), p=pauses(a);
    return `<span class="run">${pz?`Paused since <b>${hm(p[p.length-1].f)}</b>`:`Started <b>${hm(a.s)}</b>`} · <b class="live" data-id="${esc(id)}">${fmtM(activeM(a))}</b> studied</span>${pz?`<button class="ab start" data-act="r">▶ Resume</button>`:`<button class="ab pause" data-act="p">⏸ Pause</button>`}<button class="ab end" data-act="e">■ End now</button><button class="ab x" data-act="x" aria-label="Clear the times for this module">×</button>${pauseLog(a)}`;
  }
  const v=vsPlan(id);
  return `<span class="did">Did <b>${hm(a.s)}–${hm(a.e)}</b> · ${fmtM(activeM(a))} studied${v?" · "+v:""}</span><button class="ab x" data-act="x" aria-label="Clear the actual times">×</button>${pauseLog(a)}`;''')
rep('''function act(id,what){
  const now=new Date().toISOString(), a=Object.assign({},actual[id]||{});
  if(what==="s"){
    for(const k in actual){ if(k!==id && actual[k].s && !actual[k].e) actual[k]=Object.assign({},actual[k],{e:now}); }
    actual[id]={s:now};
  } else if(what==="e"){ if(a.s){ a.e=now; actual[id]=a; } }
  else { delete actual[id]; }
  queueSave(); renderAll();
}''','''function act(id,what){
  const now=new Date().toISOString(), a=JSON.parse(JSON.stringify(actual[id]||{}));
  const closePause=o=>{ const p=pauses(o).map(x=>Object.assign({},x)); if(p.length && !p[p.length-1].t) p[p.length-1].t=now; o.p=p; };
  const others=fn=>{ for(const k in actual){ const o=actual[k]; if(k!==id && o && o.s && !o.e && !isPaused(o)) actual[k]=fn(JSON.parse(JSON.stringify(o))); } };
  if(what==="s"){ others(o=>{ o.e=now; return o; }); actual[id]={s:now}; }
  else if(what==="p"){ if(a.s && !a.e && !isPaused(a)){ a.p=pauses(a).concat([{f:now}]); actual[id]=a; } }
  else if(what==="r"){ if(isPaused(a)){ others(o=>{ o.p=pauses(o).concat([{f:now}]); return o; }); closePause(a); actual[id]=a; } }
  else if(what==="e"){ if(a.s){ if(isPaused(a)) closePause(a); a.e=now; actual[id]=a; } }
  else { delete actual[id]; }
  queueSave(); renderAll();
}''')
rep('''  const running = withTime && actual[i.id] && actual[i.id].s && !actual[i.id].e;''','''  const ar=actual[i.id], running = withTime && ar && ar.s && !ar.e && !isPaused(ar), paused = withTime && isPaused(ar);''')
rep('''${running?"running":""}" data-id="${esc(i.id)}">''','''${running?"running":""} ${paused?"paused":""}" data-id="${esc(i.id)}">''')
# ---------- live timer + nudge use studied time ----------
rep('''    if(mins(a.s,now)>=90){''','''    const p=pauses(a); if(isPaused(a)) continue; const seg=p.length?p[p.length-1].t:a.s; if(nudged[seg]) continue;
    if(mins(seg,now)>=90){''')
rep('''nudged[a.s]=1;''','''nudged[seg]=1;''')
rep('''$("#nudgeT").innerHTML=`<b>${fmtM(mins(a.s,now))}</b> on''','''$("#nudgeT").innerHTML=`<b>${fmtM(mins(seg,now))}</b> without a break on''')
rep('''document.querySelectorAll(".live").forEach(el=>el.textContent=fmtM(mins(el.dataset.since,new Date().toISOString())));''','''document.querySelectorAll(".live").forEach(el=>{ const a=actual[el.dataset.id]; if(a) el.textContent=fmtM(activeM(a)); });''')
# ---------- Your times ----------
rep('''  const aTot=rows.reduce((s,i)=>{ const a=actual[i.id]; return s+(a&&a.s&&a.e?mins(a.s,a.e):0); },0);
  const meta=i=>{ const a=actual[i.id]; if(a&&a.s&&!a.e) return `running since ${hm(a.s)}`;
    if(a&&a.s&&a.e){ const v=vsPlan(i.id); return `did ${hm(a.s)}–${hm(a.e)}${v?" · "+v:""}`; }''','''  const aTot=rows.reduce((s,i)=>{ const a=actual[i.id]; return s+(a&&a.s&&a.e?activeM(a):0); },0);
  const pz=a=>{ const n=pauses(a).length; return n?` · ${n} pause${n>1?"s":""}`:""; };
  const meta=i=>{ const a=actual[i.id]; if(a&&a.s&&!a.e) return (isPaused(a)?`paused · ${fmtM(activeM(a))} studied`:`running since ${hm(a.s)}`)+pz(a);
    if(a&&a.s&&a.e){ const v=vsPlan(i.id); return `did ${hm(a.s)}–${hm(a.e)} · ${fmtM(activeM(a))}${pz(a)}${v?" · "+v:""}`; }''')
# ---------- Stats ----------
rep('''  for(const id in actual){ const a=actual[id]; if(a&&a.s&&a.e) add(DK.format(new Date(a.s)),"a",mins(a.s,a.e)); }''','''  for(const id in actual){ const a=actual[id]; if(a&&a.s&&a.e) add(DK.format(new Date(a.s)),"a",activeM(a)); }''')
rep('''  for(const id in actual){ const a=actual[id], r=ITEMBY[id]; if(!(a&&a.s&&a.e&&r&&r.i.q)) continue; const m=mins(a.s,a.e); if(m<1) continue;''','''  for(const id in actual){ const a=actual[id], r=ITEMBY[id]; if(!(a&&a.s&&a.e&&r&&r.i.q)) continue; const m=activeM(a); if(m<1) continue;''')
rep('''<p class="note">From your ▶ Start / ■ End taps; the outline is the time you planned that day.</p>''','''<p class="note">Studied time from your ▶ Start, ⏸ Pause and ■ End taps (pauses left out); the outline is the time you planned that day.</p>''')
rep("Tap ▶ Start now and ■ End now while you study to compare with your plan.","Tap ▶ Start now, ⏸ Pause and ■ End now while you study; only studied time is compared with your plan.")
open(p,'w').write(t); print('template ok')

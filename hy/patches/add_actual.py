p='tracker.tpl.html'; t=open(p).read()
def rep(a,b):
    global t
    assert t.count(a)==1,(a[:80],t.count(a)); t=t.replace(a,b)
rep(".tr{display:flex;align-items:center;gap:6px}",
""".ctl{display:grid;gap:6px;justify-items:end}
.tr{display:flex;align-items:center;gap:6px}
.act{display:flex;flex-wrap:wrap;gap:6px;align-items:center;justify-content:flex-end;font-size:12.5px;color:var(--muted)}
.ab{font:inherit;font-size:12px;font-weight:800;border-radius:8px;padding:5px 10px;border:1.5px solid var(--line);background:var(--surface);color:var(--ink);cursor:pointer;line-height:1.2}
.ab.start{border-color:var(--hc)}
.ab.end{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.ab.x{padding:5px 8px;color:var(--muted)}
.ab:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.act .run b,.act .did b{color:var(--ink);font-family:var(--f-mono);font-variant-numeric:tabular-nums}
.over{color:var(--bad);font-weight:700}
.under{color:var(--good);font-weight:700}
.item.running{box-shadow:inset 0 0 0 2px var(--hc)}""")
rep(".item .tr{grid-row:2;grid-column:1 / -1;margin-left:38px}",".item .ctl{grid-row:2;grid-column:1 / -1;margin-left:38px;justify-items:start}.item .act{justify-content:flex-start}")
rep(".mt-row{grid-template-columns:96px 10px minmax(0,1fr)}.mt-row .mt-q{display:none}",".mt-row{grid-template-columns:96px 10px minmax(0,1fr)}.mt-row .mt-q{grid-column:3;font-size:11.5px}")
rep("let times = {};","let times = {};\nlet actual = {};")
rep('const tm=localStorage.getItem("neetss-times"); if(tm) times=JSON.parse(tm)||{};','const tm=localStorage.getItem("neetss-times"); if(tm) times=JSON.parse(tm)||{}; const ac=localStorage.getItem("neetss-actual"); if(ac) actual=JSON.parse(ac)||{};')
rep('localStorage.setItem("neetss-times",JSON.stringify(times));','localStorage.setItem("neetss-times",JSON.stringify(times)); localStorage.setItem("neetss-actual",JSON.stringify(actual));')
rep("try{ await ref.set({done, times, updatedAt:new Date().toISOString()});","try{ await ref.set({done, times, actual, updatedAt:new Date().toISOString()});")
rep("      times = Object.assign({}, d.times||{});","      times = Object.assign({}, d.times||{});\n      actual = Object.assign({}, d.actual||{});")
rep('''function itemHTML(i,opt){''','''const HM = new Intl.DateTimeFormat("en-GB",{timeZone:"Asia/Kolkata",hour:"2-digit",minute:"2-digit",hour12:false});
function hm(iso){ try{ return HM.format(new Date(iso)); }catch(e){ return ""; } }
function mins(a,b){ return Math.max(0,Math.round((Date.parse(b)-Date.parse(a))/60000)); }
function fmtM(m){ const h=Math.floor(m/60), r=m%60; return h ? (h+" h"+(r?" "+r+" min":"")) : (r+" min"); }
function planM(v){ if(!v.s||!v.e) return null; let m=(+v.e.slice(0,2)*60+ +v.e.slice(3))-(+v.s.slice(0,2)*60+ +v.s.slice(3)); if(m<=0) m+=1440; return m; }
function vsPlan(id){
  const a=actual[id]||{}, pm=planM(tget(id)); if(!a.s||!a.e||pm==null) return "";
  const diff=mins(a.s,a.e)-pm;
  return Math.abs(diff)<3 ? `<span class="under">on plan</span>` : (diff>0 ? `<span class="over">${fmtM(diff)} over</span>` : `<span class="under">${fmtM(-diff)} under</span>`);
}
function actHTML(id){
  const a=actual[id]||{};
  if(!a.s) return `<button class="ab start" data-act="s">▶ Start now</button>`;
  if(!a.e) return `<span class="run">Started <b>${hm(a.s)}</b> · <b class="live" data-since="${a.s}">${fmtM(mins(a.s,new Date().toISOString()))}</b> so far</span><button class="ab end" data-act="e">■ End now</button><button class="ab x" data-act="x" aria-label="Clear the start time">×</button>`;
  const v=vsPlan(id);
  return `<span class="did">Did <b>${hm(a.s)}–${hm(a.e)}</b> · ${fmtM(mins(a.s,a.e))}${v?" · "+v:""}</span><button class="ab x" data-act="x" aria-label="Clear the actual times">×</button>`;
}
function act(id,what){
  const now=new Date().toISOString(), a=Object.assign({},actual[id]||{});
  if(what==="s"){
    for(const k in actual){ if(k!==id && actual[k].s && !actual[k].e) actual[k]=Object.assign({},actual[k],{e:now}); }
    actual[id]={s:now};
  } else if(what==="e"){ if(a.s){ a.e=now; actual[id]=a; } }
  else { delete actual[id]; }
  queueSave(); renderAll();
}
setInterval(()=>document.querySelectorAll(".live").forEach(el=>el.textContent=fmtM(mins(el.dataset.since,new Date().toISOString()))),30000);
function itemHTML(i,opt){''')
rep('''    ${withTime?`<span class="tr">''','''    ${withTime?`<div class="ctl"><span class="tr">''')
rep('''aria-label="End time for ${esc(i.t)}"></span>`:""}''','''aria-label="End time for ${esc(i.t)}"></span><span class="act">${actHTML(i.id)}</span></div>`:""}''')
rep('''  return `<div class="item ${kcls} ${isDone(i.id)?"done":""} ${i.tier==="L"?"lt":""}" data-id="${esc(i.id)}">''','''  const running = withTime && actual[i.id] && actual[i.id].s && !actual[i.id].e;
  return `<div class="item ${kcls} ${isDone(i.id)?"done":""} ${i.tier==="L"?"lt":""} ${running?"running":""}" data-id="${esc(i.id)}">''')
rep('''  renderMyTimes(d);
  $("#prevD")''','''  $("#sheet").querySelectorAll(".ab").forEach(btn=>btn.onclick=()=>act(btn.closest(".item").dataset.id,btn.dataset.act));
  renderMyTimes(d);
  $("#prevD")''')
rep('''  const rows=d.items.filter(i=>tkey(i.id)).sort((a,b)=>tkey(a.id).localeCompare(tkey(b.id)));''','''  const akey=id=>{ const a=actual[id]; return a&&a.s?hm(a.s):""; };
  const rows=d.items.filter(i=>tkey(i.id)||akey(i.id)).sort((a,b)=>(tkey(a.id)||akey(a.id)).localeCompare(tkey(b.id)||akey(b.id)));
  const pTot=rows.reduce((s,i)=>s+(planM(tget(i.id))||0),0);
  const aTot=rows.reduce((s,i)=>{ const a=actual[i.id]; return s+(a&&a.s&&a.e?mins(a.s,a.e):0); },0);
  const meta=i=>{ const a=actual[i.id]; if(a&&a.s&&!a.e) return `running since ${hm(a.s)}`;
    if(a&&a.s&&a.e){ const v=vsPlan(i.id); return `did ${hm(a.s)}–${hm(a.e)}${v?" · "+v:""}`; }
    return [dur(tget(i.id)),i.q?i.q+" Qs":""].filter(Boolean).join(" · "); };''')
rep('''<span class="when">${rows.length?rows.length+" of "+d.items.length+" set":"none set yet"}</span>''','''<span class="when">${rows.length?([pTot?"planned "+fmtM(pTot):"",aTot?"done "+fmtM(aTot):""].filter(Boolean).join(" · ")||rows.length+" set"):"none set yet"}</span>''')
rep('''<span class="mt-q">${[dur(tget(i.id)),i.q?i.q+" Qs":""].filter(Boolean).join(" · ")}</span>''','''<span class="mt-q">${meta(i)}</span>''')
rep('''  const span=i=>{ const v=tget(i.id); return (v.s||"--:--")+"–"+(v.e||"--:--"); };''','''  const span=i=>{ const v=tget(i.id); if(!v.s&&!v.e){ const a=actual[i.id]; return a&&a.s?hm(a.s)+"–"+(a.e?hm(a.e):"…"):"--:--"; } return (v.s||"--:--")+"–"+(v.e||"--:--"); };''')
rep("Each end time fills in the next module's start.","Each end time fills in the next module's start. Tap ▶ Start now and ■ End now while you study to compare with your plan.")
open(p,'w').write(t); print('template ok')
b='build.py'; s=open(b).read()
for a,c in [('done,times,updatedAt:localStamp()||stamp()','done,times,actual,updatedAt:localStamp()||stamp()'),
            ('times=Object.assign({},remote.times||{}); saveLocal();','times=Object.assign({},remote.times||{}); actual=Object.assign({},remote.actual||{}); saveLocal();')]:
    assert a in s, a; s=s.replace(a,c)
open(b,'w').write(s); print('build ok')

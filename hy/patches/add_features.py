p='tracker.tpl.html'; t=open(p).read()
def rep(a,b):
    global t
    assert t.count(a)==1,(a[:90],t.count(a)); t=t.replace(a,b)

# ================= CSS =================
rep("@media (prefers-reduced-motion:reduce)", """.accrow{display:flex;align-items:center;gap:6px;font-size:12.5px;color:var(--muted);flex-wrap:wrap}
.acc-in,.sc-in,.sw-in{font-family:var(--f-mono);font-size:13px;font-weight:700;color:var(--ink);background:var(--surface);border:1.5px solid var(--line);border-radius:8px;padding:4px 6px;width:60px;min-height:30px}
.acc-in:focus,.sc-in:focus,.sw-in:focus,.mv:focus{outline:3px solid var(--accent);outline-offset:1px}
.pct{font-family:var(--f-mono);font-size:12px;font-weight:800;padding:2px 7px;border-radius:99px;background:var(--surface-2);color:var(--ink)}
.pct.lo{background:color-mix(in srgb,var(--bad) 18%,transparent);color:var(--bad)}
.pct.mid{background:color-mix(in srgb,var(--warn) 20%,transparent);color:var(--warn)}
.pct.hi{background:color-mix(in srgb,var(--good) 18%,transparent);color:var(--good)}
.mv{font:inherit;font-size:12px;font-weight:700;color:var(--muted);background:var(--surface);border:1.5px dashed var(--line);border-radius:8px;padding:4px 6px;max-width:150px}
.weak{display:grid;gap:4px;margin-top:4px}
.weak span{font-size:13px;color:var(--ink)}
.stats{display:grid;gap:14px}
.card{background:var(--surface);border-radius:var(--r);box-shadow:var(--shadow);padding:16px;display:grid;gap:12px;min-width:0}
.card h2{font-size:18px}
.card h3{font-size:14px}
.card p{margin:0}
.st-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
@media (max-width:860px){.st-grid{grid-template-columns:minmax(0,1fr)}}
.chart{width:100%;height:auto;display:block}
.chart .grid{stroke:var(--line);stroke-width:1}
.chart .ax{fill:var(--muted);font-family:var(--f-mono);font-size:11px}
.chart .ln{stroke:var(--hl-pyq);stroke-width:2.5;fill:none}
.chart .pt{fill:var(--surface);stroke:var(--hl-pyq);stroke-width:2.5}
.chart .pt.mock{stroke:var(--accent)}
.chart .val{fill:var(--ink);font-family:var(--f-mono);font-size:11.5px;font-weight:700}
.chart .ghost{fill:none;stroke:var(--line);stroke-dasharray:3 3}
.tbl-wrap{overflow-x:auto}
.tbl{width:100%;border-collapse:collapse;font-size:13.5px;min-width:560px}
.tbl th{text-align:left;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);font-weight:800;padding:6px 6px;border-bottom:1px solid var(--line)}
.tbl td{padding:7px 6px;border-bottom:1px solid var(--line);vertical-align:top}
.tbl td.num,.tbl th.num{text-align:right;font-family:var(--f-mono);font-variant-numeric:tabular-nums}
.tbl details{margin-top:6px}
.tbl summary{cursor:pointer;color:var(--accent);font-weight:700;font-size:12.5px}
.sw-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:6px 10px;margin-top:8px}
.sw-grid label{display:flex;justify-content:space-between;align-items:center;gap:6px;font-size:12.5px;color:var(--ink)}
.hb{display:grid;gap:7px}
.hb-row{display:grid;grid-template-columns:minmax(90px,150px) minmax(0,1fr) auto;gap:10px;align-items:center;font-size:13px}
.hb-row .lab{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.hb-track{position:relative;height:12px;background:var(--surface-2);border-radius:99px;overflow:hidden}
.hb-fill{position:absolute;inset:0 auto 0 0;border-radius:99px;background:var(--bc,var(--accent))}
.hb-plan{position:absolute;top:0;bottom:0;left:0;border:2px solid var(--ink);border-radius:99px;opacity:.55}
.hb-row .v{font-family:var(--f-mono);font-size:12px;font-weight:700;color:var(--ink);font-variant-numeric:tabular-nums}
.empty{font-size:13.5px;color:var(--muted);padding:10px 12px;border:1.5px dashed var(--line);border-radius:12px}
.legend2{display:flex;gap:14px;flex-wrap:wrap;font-size:12px;color:var(--muted)}
.legend2 i{display:inline-block;width:18px;height:9px;border-radius:99px;margin-right:6px;vertical-align:0}
.nudge{position:fixed;left:50%;transform:translateX(-50%);bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:30;background:var(--surface);color:var(--ink);border:2px solid var(--accent);box-shadow:var(--shadow);border-radius:14px;padding:12px 14px;display:flex;gap:12px;align-items:center;max-width:min(560px,calc(100% - 32px));font-size:14px}
.nudge b{font-family:var(--f-display)}
@media (prefers-reduced-motion:reduce)""")

# ================= HTML: Stats tab, view, nudge =================
rep('''    <button role="tab" id="tab-mar" aria-selected="false" data-tab="mar">Marrow</button>''','''    <button role="tab" id="tab-mar" aria-selected="false" data-tab="mar">Marrow</button>
    <button role="tab" id="tab-stats" aria-selected="false" data-tab="stats">Stats</button>''')
rep('''  <div id="marView" hidden></div>''','''  <div id="marView" hidden></div>
  <div id="statsView" hidden></div>''')
rep('''<div class="toast" id="toast" role="status"></div>''','''<div class="toast" id="toast" role="status"></div>
<div class="nudge" id="nudge" role="status" hidden><span id="nudgeT"></span><button class="btn primary" id="nudgeOk">OK</button></div>''')

# ================= state + sync =================
rep("let actual = {};","let actual = {};\nlet ext = {acc:{}, moved:{}, scores:{}};\nfunction normExt(x){ x=x||{}; return {acc:Object.assign({},x.acc||{}), moved:Object.assign({},x.moved||{}), scores:Object.assign({},x.scores||{})}; }")
rep('const ac=localStorage.getItem("neetss-actual"); if(ac) actual=JSON.parse(ac)||{};','const ac=localStorage.getItem("neetss-actual"); if(ac) actual=JSON.parse(ac)||{}; const ex=localStorage.getItem("neetss-ext"); if(ex) ext=normExt(JSON.parse(ex));')
rep('localStorage.setItem("neetss-actual",JSON.stringify(actual));','localStorage.setItem("neetss-actual",JSON.stringify(actual)); localStorage.setItem("neetss-ext",JSON.stringify(ext));')
rep("try{ await ref.set({done, times, actual, updatedAt:new Date().toISOString()});","try{ await ref.set({done, times, actual, ext, updatedAt:new Date().toISOString()});")
rep("      actual = Object.assign({}, d.actual||{});","      actual = Object.assign({}, d.actual||{});\n      ext = normExt(d.ext);")

# ================= day index, carried items =================
rep('''const isDone = id => !!done[id];
function sumQ(list,pred){ return list.reduce((a,i)=>a+(pred(i)&&isDone(i.id)?i.q:0),0); }
function dayPct(d){ const tot=d.items.reduce((a,i)=>a+(i.q||20),0); const got=d.items.reduce((a,i)=>a+(isDone(i.id)?(i.q||20):0),0); return tot?Math.round(got*100/tot):0; }''',
'''const isDone = id => !!done[id];
function sumQ(list,pred){ return list.reduce((a,i)=>a+(pred(i)&&isDone(i.id)?i.q:0),0); }
DATA.phase1.forEach(d=>d.key="p1:"+d.n); DATA.phase2.forEach(d=>d.key="p2:"+d.n);
const ALLDAYS=[...DATA.phase1,...DATA.phase2];
const DAYBY=Object.fromEntries(ALLDAYS.map(d=>[d.key,d]));
const ITEMBY={}; ALLDAYS.forEach(d=>d.items.forEach(i=>{ ITEMBY[i.id]={i,day:d}; }));
const dayLabel=d=>(d.key.startsWith("p1")?"Day ":"Rev ")+d.n;
function incoming(d){ const out=[]; for(const id in ext.moved){ if(ext.moved[id]===d.key){ const r=ITEMBY[id]; if(r && r.day.key!==d.key) out.push(Object.assign({},r.i,{from:r.day})); } } return out; }
function itemsOf(d){ return d.items.filter(i=>!ext.moved[i.id]||ext.moved[i.id]===d.key).concat(incoming(d)); }
function dayPct(d){ const its=itemsOf(d); const tot=its.reduce((a,i)=>a+(i.q||20),0); const got=its.reduce((a,i)=>a+(isDone(i.id)?(i.q||20):0),0); return tot?Math.round(got*100/tot):0; }
function curDay(id){ const m=ext.moved[id]; return m&&DAYBY[m] ? DAYBY[m] : (ITEMBY[id]?ITEMBY[id].day:null); }
function moveHTML(i){
  const cd=curDay(i.id); if(!cd) return "";
  const k=ALLDAYS.indexOf(cd), later=ALLDAYS.slice(k+1); if(!later.length && !ext.moved[i.id]) return "";
  const tom=later[0], lb=later.find(x=>x.light||x.buffer);
  let o=`<option value="">Move to…</option>`;
  if(ext.moved[i.id]) o+=`<option value="__back">Back to ${dayLabel(ITEMBY[i.id].day)}</option>`;
  if(tom) o+=`<option value="${tom.key}">Tomorrow · ${dayLabel(tom)}</option>`;
  if(lb && lb!==tom) o+=`<option value="${lb.key}">Next ${lb.buffer?"buffer":"light"} day · ${dayLabel(lb)}</option>`;
  if(later.length>1) o+=`<optgroup label="Other day">${later.slice(1).map(x=>`<option value="${x.key}">${dayLabel(x)} · ${esc(x.title)}</option>`).join("")}</optgroup>`;
  return `<select class="mv" aria-label="Move ${esc(i.t)} to another day">${o}</select>`;
}
function moveItem(id,val){
  if(!val) return;
  const orig=ITEMBY[id].day.key;
  if(val==="__back"||val===orig) delete ext.moved[id]; else ext.moved[id]=val;
  queueSave(); renderAll(); toast(val==="__back"||val===orig?"Moved back":"Moved to "+dayLabel(DAYBY[val]));
}
// ---------- accuracy and test scores ----------
const ACC_K={main:1,ss:1,qrp:1,mar:1};
const TESTS=[["pyq1:2022","PYQ 2022"],["pyq1:2023","PYQ 2023"],["pyq1:2024","PYQ 2024"],["pyq2:2025","PYQ 2025"],["mock:1","Mock 1"],["mock:2","Mock 2"],["mock:3","Mock 3"],["mock:4","Mock 4"]].map(([id,t])=>({id,t,date:ITEMBY[id]?ITEMBY[id].day.date:""}));
const TESTSET=Object.fromEntries(TESTS.map(x=>[x.id,x]));
const AUDIT=["Cardiology","Neurology","GI & Hepatology","Endocrinology","Nephrology","Infectious Diseases","Rheumatology","Haem & Onco","Pulm & Critical Care","Tox & others"];
const accPct=i=>{ const r=ext.acc[i.id]; return (r==null||r==="")?null:Math.round(100*Math.min(+r,i.q)/i.q); };
const pctCls=p=>p==null?"":(p<60?"lo":(p<75?"mid":"hi"));
const sc=id=>ext.scores[id]||{};
const marks=s=>(s.r==null&&s.w==null)?null:4*(+s.r||0)-(+s.w||0);
function accHTML(i){
  if(TESTSET[i.id]){ const s=sc(i.id), m=marks(s);
    return `<span class="accrow">Right <input type="number" class="sc-in" data-id="${esc(i.id)}" data-f="r" min="0" max="150" inputmode="numeric" value="${s.r??""}" aria-label="Right answers in ${esc(i.t)}"> Wrong <input type="number" class="sc-in" data-id="${esc(i.id)}" data-f="w" min="0" max="150" inputmode="numeric" value="${s.w??""}" aria-label="Wrong answers in ${esc(i.t)}"> <b class="pct mk" data-id="${esc(i.id)}">${m==null?"–":m}/600</b></span>`; }
  if(!ACC_K[i.k] || !i.q || !isDone(i.id)) return "";
  const p=accPct(i);
  return `<span class="accrow">Right <input type="number" class="acc-in" data-id="${esc(i.id)}" data-q="${i.q}" min="0" max="${i.q}" inputmode="numeric" value="${ext.acc[i.id]??""}" aria-label="Questions right in ${esc(i.t)}"> / ${i.q} <b class="pct ${pctCls(p)}">${p==null?"–":p+"%"}</b></span>`;
}
function bindScoreInputs(root,after){
  root.querySelectorAll(".acc-in").forEach(inp=>{
    const show=()=>{ const q=+inp.dataset.q, v=inp.value===""?null:Math.max(0,Math.min(q,Math.round(+inp.value))); const b=inp.parentElement.querySelector(".pct"); const p=v==null?null:Math.round(100*v/q); b.className="pct "+pctCls(p); b.textContent=p==null?"–":p+"%"; return v; };
    inp.oninput=show;
    inp.onchange=()=>{ const v=show(); if(v==null) delete ext.acc[inp.dataset.id]; else { ext.acc[inp.dataset.id]=v; inp.value=v; } queueSave(); if(after) after(); };
  });
  root.querySelectorAll(".sc-in").forEach(inp=>{
    const upd=()=>{ const id=inp.dataset.id, s=Object.assign({},sc(id)); const v=inp.value===""?null:Math.max(0,Math.min(150,Math.round(+inp.value)));
      if(v==null) delete s[inp.dataset.f]; else s[inp.dataset.f]=v; ext.scores[id]=s;
      const m=marks(s); document.querySelectorAll(`.mk[data-id="${CSS.escape(id)}"]`).forEach(b=>b.textContent=(m==null?"–":m)+"/600"); return v; };
    inp.oninput=upd;
    inp.onchange=()=>{ const v=upd(); if(v!=null) inp.value=v; queueSave(); if(after) after(); };
  });
  root.querySelectorAll(".sw-in").forEach(inp=>{
    inp.onchange=()=>{ const id=inp.dataset.id, s=Object.assign({},sc(id)), sub=Object.assign({},s.subj||{}); const v=inp.value===""?null:Math.max(0,Math.min(150,Math.round(+inp.value)));
      if(v==null) delete sub[inp.dataset.s]; else { sub[inp.dataset.s]=v; inp.value=v; } s.subj=sub; ext.scores[id]=s; queueSave(); if(after) after(); };
  });
  root.querySelectorAll(".mv").forEach(sel=>sel.onchange=()=>moveItem(sel.closest(".item").dataset.id,sel.value));
}''')

# ================= pace + ribbon use carried items =================
rep('''  const pending = pastDays.flatMap(d=>d.items.filter(i=>!isDone(i.id)).map(i=>({...i,d})));''','''  const pending = pastDays.flatMap(d=>itemsOf(d).filter(i=>!isDone(i.id)).map(i=>({...i,d})));''')
rep('''    if(td){ const left=td.items.filter(i=>!isDone(i.id));''','''    if(td){ const left=itemsOf(td).filter(i=>!isDone(i.id));''')
rep('''  t.innerHTML = `${pending.length} item${pending.length>1?"s":""} pending from earlier days: ${fmt(pMain)} Main Qs and ${fmt(pOther)} other Qs. Main comes first; SS can go in the Nov 10 buffer. <button''','''  t.innerHTML = `${pending.length} item${pending.length>1?"s":""} pending from earlier days: ${fmt(pMain)} Main Qs and ${fmt(pOther)} other Qs. Main comes first; use "Move to…" on a module to carry it to another day. <button''')
rep('''    const pct=dayPct(d), cur=sel[tab]===d.n;''','''    const pct=dayPct(d), cur=sel[tab]===d.n, inq=incoming(d).reduce((a,i)=>a+i.q,0);''')
rep('''      ${d.light?'<span class="lt">Light day</span>':""}''','''      ${d.light?'<span class="lt">Light day</span>':""}${inq?`<span class="lt" style="color:var(--warn)">+${inq} Qs moved in</span>`:""}''')

# ================= item markup: moved-from hint, accuracy, move select =================
rep('''  const tv = tget(i.id);''','''  if(i.from) hint += `<span class="hint" style="color:var(--warn)">Moved from ${dayLabel(i.from)}</span>`;
  const tv = tget(i.id);''')
rep('''<span class="act">${actHTML(i.id)}</span></div>`:""}''','''<span class="act">${actHTML(i.id)}${isDone(i.id)?"":moveHTML(i)}</span>${accHTML(i)}</div>`:""}''')

# ================= sheet: base vs carried items, weak modules in revision mornings =================
rep('''  const d = days.find(x=>x.n===sel[tab]) || days[0];
  const pct=dayPct(d);
  const tot=d.items.reduce((a,i)=>a+i.q,0), got=d.items.reduce((a,i)=>a+(isDone(i.id)?i.q:0),0);
  let body="";
  if(tab==="p1"){
    const main=d.items.filter(i=>i.k==="main");''','''  const d = days.find(x=>x.n===sel[tab]) || days[0];
  const pct=dayPct(d);
  const inc=incoming(d), base=itemsOf(d).filter(i=>!i.from), items=base.concat(inc);
  const tot=items.reduce((a,i)=>a+i.q,0), got=items.reduce((a,i)=>a+(isDone(i.id)?i.q:0),0);
  let body="";
  if(inc.length) body+=block("Carried over","moved here from other days","+"+inc.reduce((a,i)=>a+i.q,0)+" Qs","--hl-task-soft",inc);
  if(tab==="p1"){
    const main=base.filter(i=>i.k==="main");''')
rep('''    const pyq=d.items.filter(i=>i.k==="pyq"), ss=d.items.filter(i=>i.k==="ss");''','''    const pyq=base.filter(i=>i.k==="pyq"), ss=base.filter(i=>i.k==="ss");''')
rep('''    const mar=d.items.filter(i=>i.k==="mar");
    body+=block(d.light''','''    const mar=base.filter(i=>i.k==="mar");
    body+=block(d.light''')
rep('''    body+=block("QRP lagged recall","21:00–22:30","Lights out 23:00","--hl-qrp-soft",d.items.filter(i=>i.k==="qrp"));''','''    body+=block("QRP lagged recall","21:00–22:30","Lights out 23:00","--hl-qrp-soft",base.filter(i=>i.k==="qrp"));''')
rep('''    const mock=d.items.find(i=>i.id.startsWith("mock:")||i.id.startsWith("pyq2:"));
    body+=block(mock?"Test morning":"Morning · toughest work",mock?"09:00–13:15":"07:00–09:30",mock?"Exam conditions":"Your own errors","--hl-pyq-soft",d.items.filter(i=>i.b==="A"));
    body+=block("QRP revision pass","09:45–17:15","Most asked first","--hl-qrp-soft",d.items.filter(i=>i.b==="B"));
    body+=block("Evening","17:30–20:00","","",d.items.filter(i=>i.b==="C"));
    const mar2=d.items.filter(i=>i.k==="mar");''','''    const mock=base.find(i=>i.id.startsWith("mock:")||i.id.startsWith("pyq2:"));
    const weak=weakList().filter(w=>w.i.sys===d.sys).slice(0,8);
    const wnote=weak.length?`Weak modules for this system (under 60% right): <span class="weak">${weak.map(w=>`<span>${esc(w.i.t)} · <b class="pct lo">${w.p}%</b> · ${dayLabel(w.day)}</span>`).join("")}</span>`:"";
    body+=block(mock?"Test morning":"Morning · toughest work",mock?"09:00–13:15":"07:00–09:30",mock?"Exam conditions":"Your own errors","--hl-pyq-soft",base.filter(i=>i.b==="A"),wnote);
    body+=block("QRP revision pass","09:45–17:15","Most asked first","--hl-qrp-soft",base.filter(i=>i.b==="B"));
    body+=block("Evening","17:30–20:00","","",base.filter(i=>i.b==="C"));
    const mar2=base.filter(i=>i.k==="mar");''')
rep('''  $("#sheet").querySelectorAll(".ab").forEach(btn=>btn.onclick=()=>act(btn.closest(".item").dataset.id,btn.dataset.act));''','''  $("#sheet").querySelectorAll(".ab").forEach(btn=>btn.onclick=()=>act(btn.closest(".item").dataset.id,btn.dataset.act));
  bindScoreInputs($("#sheet"));''')
rep('''    d.items.forEach(i=>{ if(all) delete done[i.id]; else done[i.id]=1; });''','''    items.forEach(i=>{ if(all) delete done[i.id]; else done[i.id]=1; });''')
rep('''  const rows=d.items.filter(i=>tkey(i.id)||akey(i.id))''','''  const rows=itemsOf(d).filter(i=>tkey(i.id)||akey(i.id))''')
rep('''<div class="toast" id="toast" role="status"></div>''','''<div class="toast" id="toast" role="status"></div>''')

# ================= Marrow tab shows moved days =================
rep('''      <div class="subj-list">${s.items.map(i=>itemHTML(i)).join("")}</div></section>`;
  };
  $("#marView")''','''      <div class="subj-list">${s.items.map(i=>itemHTML(ext.moved[i.id]&&DAYBY[ext.moved[i.id]]?{...i,when:"Moved to "+dayLabel(DAYBY[ext.moved[i.id]])}:i)).join("")}</div></section>`;
  };
  $("#marView")''')

# ================= Stats tab =================
rep('''function toast(msg){''','''function weakList(){
  const out=[];
  for(const id in ext.acc){ const r=ITEMBY[id]; if(!r||!r.i.q) continue; const p=Math.round(100*Math.min(+ext.acc[id],r.i.q)/r.i.q); if(p<60) out.push({i:r.i,day:curDay(id)||r.day,p}); }
  return out.sort((a,b)=>a.p-b.p);
}
function hbars(rows,opt){
  opt=opt||{}; if(!rows.length) return `<p class="empty">${opt.empty||"Nothing to show yet."}</p>`;
  const max=Math.max(1,...rows.map(r=>Math.max(r.v,r.plan||0)), opt.max||0);
  return `<div class="hb">${rows.map(r=>`<div class="hb-row"><span class="lab" title="${esc(r.lab)}">${esc(r.lab)}</span><span class="hb-track">${r.plan?`<i class="hb-plan" style="width:${Math.min(100,100*r.plan/max)}%"></i>`:""}<i class="hb-fill" style="width:${Math.min(100,100*r.v/max)}%;${r.color?`--bc:${r.color}`:""}"></i></span><span class="v">${esc(r.txt)}</span></div>`).join("")}</div>`;
}
function testsChart(){
  const W=640,H=230,L=44,R=14,T=22,B=34, pts=TESTS.map((x,k)=>({x,k,m:marks(sc(x.id))}));
  const have=pts.filter(p=>p.m!=null);
  const lo=Math.min(0,...have.map(p=>p.m)), hi=600, X=k=>L+k*(W-L-R)/(TESTS.length-1), Y=m=>T+(hi-m)*(H-T-B)/(hi-lo);
  const ticks=[0,150,300,450,600].filter(v=>v>=lo); if(lo<0) ticks.unshift(lo);
  let s=`<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Marks out of 600 across PYQ papers and grand mocks">`;
  s+=ticks.map(v=>`<line class="grid" x1="${L}" x2="${W-R}" y1="${Y(v)}" y2="${Y(v)}"/><text class="ax" x="${L-6}" y="${Y(v)+4}" text-anchor="end">${v}</text>`).join("");
  s+=pts.map(p=>`<text class="ax" x="${X(p.k)}" y="${H-12}" text-anchor="middle">${p.x.t.replace("PYQ ","PYQ ’").replace("’20","’")}</text>`).join("");
  if(have.length>1) s+=`<polyline class="ln" points="${have.map(p=>X(p.k)+","+Y(p.m)).join(" ")}"/>`;
  s+=pts.map(p=>p.m==null?`<circle class="ghost" cx="${X(p.k)}" cy="${Y(0)}" r="4"/>`:`<circle class="pt ${p.x.id.startsWith("mock")?"mock":""}" cx="${X(p.k)}" cy="${Y(p.m)}" r="5"/><text class="val" x="${X(p.k)}" y="${Y(p.m)-10}" text-anchor="middle">${p.m}</text>`).join("");
  return s+`</svg>`;
}
function lossBars(){
  const tot=new Array(AUDIT.length).fill(0); let any=false;
  TESTS.forEach(x=>{ const sub=sc(x.id).subj||{}; for(const k in sub){ tot[+k]+=+sub[k]||0; any=true; } });
  if(!any) return `<p class="empty">After each paper's audit, open "Wrong answers by subject" below and type how many you got wrong in each system. The systems costing you the most marks will rise to the top here.</p>`;
  const rows=AUDIT.map((a,k)=>({lab:a,v:tot[k],txt:tot[k]+" wrong",color:"var(--bad)"})).filter(r=>r.v).sort((a,b)=>b.v-a.v);
  return hbars(rows);
}
function renderStats(){
  const v=$("#statsView");
  // tests table
  const rows=TESTS.map(x=>{ const s=sc(x.id), m=marks(s), att=(+s.r||0)+(+s.w||0), acc=att?Math.round(100*(+s.r||0)/att):null;
    return `<tr><td><b>${x.t}</b><br><span class="note">${x.date?nice(x.date):""}</span>
      <details><summary>Wrong answers by subject</summary><div class="sw-grid">${AUDIT.map((a,k)=>`<label>${a}<input type="number" class="sw-in" data-id="${x.id}" data-s="${k}" min="0" max="150" inputmode="numeric" value="${(s.subj||{})[k]??""}" aria-label="Wrong in ${a}, ${x.t}"></label>`).join("")}</div></details></td>
      <td class="num"><input type="number" class="sc-in" data-id="${x.id}" data-f="r" min="0" max="150" inputmode="numeric" value="${s.r??""}" aria-label="Right answers, ${x.t}"></td>
      <td class="num"><input type="number" class="sc-in" data-id="${x.id}" data-f="w" min="0" max="150" inputmode="numeric" value="${s.w??""}" aria-label="Wrong answers, ${x.t}"></td>
      <td class="num">${(s.r!=null||s.w!=null)?150-att:"–"}</td><td class="num"><b class="mk" data-id="${x.id}">${m==null?"–":m}/600</b></td><td class="num">${acc==null?"–":acc+"%"}</td></tr>`; }).join("");
  // accuracy
  const accItems=Object.keys(ext.acc).map(id=>ITEMBY[id]).filter(r=>r&&r.i.q);
  const sumBy=f=>{ const g={}; accItems.forEach(r=>{ const k=f(r.i); if(!k) return; g[k]=g[k]||{r:0,q:0}; g[k].r+=Math.min(+ext.acc[r.i.id],r.i.q); g[k].q+=r.i.q; }); return g; };
  const kinds=sumBy(i=>({main:"Main Harrison",ss:"Super Specialty",qrp:"QRP",mar:"Marrow"})[i.k]);
  const syss=sumBy(i=>SYS[i.sys]||"Other");
  const pr=g=>Object.entries(g).map(([k,x])=>{ const p=Math.round(100*x.r/x.q); return {lab:k,v:p,txt:p+"% · "+x.q+" Qs",color:p<60?"var(--bad)":(p<75?"var(--warn)":"var(--good)")}; }).sort((a,b)=>a.v-b.v);
  const weak=weakList();
  // hours
  const byDate={}, add=(d,k,m)=>{ byDate[d]=byDate[d]||{a:0,p:0}; byDate[d][k]+=m; };
  const DK=new Intl.DateTimeFormat("en-CA",{timeZone:"Asia/Kolkata",year:"numeric",month:"2-digit",day:"2-digit"});
  for(const id in actual){ const a=actual[id]; if(a&&a.s&&a.e) add(DK.format(new Date(a.s)),"a",mins(a.s,a.e)); }
  ALLDAYS.forEach(d=>itemsOf(d).forEach(i=>{ const pm=planM(tget(i.id)); if(pm) add(d.date,"p",pm); }));
  const hrows=Object.keys(byDate).sort().slice(-14).map(dt=>{ const x=byDate[dt]; return {lab:nice(dt),v:x.a/60,plan:x.p/60,txt:(x.a/60).toFixed(1)+" h"+(x.p?" of "+(x.p/60).toFixed(1):""),color:"var(--hl-mar)"}; });
  const speed={}, tod={};
  for(const id in actual){ const a=actual[id], r=ITEMBY[id]; if(!(a&&a.s&&a.e&&r&&r.i.q)) continue; const m=mins(a.s,a.e); if(m<1) continue;
    const k=({main:"Main Harrison",ss:"Super Specialty",qrp:"QRP",mar:"Marrow"})[r.i.k]; if(k){ speed[k]=speed[k]||{m:0,q:0}; speed[k].m+=m; speed[k].q+=r.i.q; }
    const h=+hm(a.s).slice(0,2), slot=h<5?"Night (00–05)":h<12?"Morning (05–12)":h<17?"Afternoon (12–17)":"Evening (17–24)"; tod[slot]=tod[slot]||{m:0,q:0}; tod[slot].m+=m; tod[slot].q+=r.i.q; }
  const spRows=g=>Object.entries(g).map(([k,x])=>({lab:k,v:x.m/x.q,txt:(x.m/x.q).toFixed(1)+" min/Q",color:"var(--hl-qrp)"}));
  v.innerHTML=`<div class="stats">
    <section class="card"><h2>Test scores</h2>
      <p class="note">NEET-SS marking: +4 right, −1 wrong, out of 600. Enter right and wrong after each paper; the line updates as you type.</p>
      <div id="stChart">${testsChart()}</div>
      <div class="legend2"><span><i style="background:var(--hl-pyq)"></i>PYQ papers</span><span><i style="background:var(--accent)"></i>Grand mocks</span></div>
      <div class="tbl-wrap"><table class="tbl"><thead><tr><th>Paper</th><th class="num">Right</th><th class="num">Wrong</th><th class="num">Skipped</th><th class="num">Marks</th><th class="num">Accuracy</th></tr></thead><tbody>${rows}</tbody></table></div>
      <h3>Where marks were lost</h3><div id="stLoss">${lossBars()}</div>
    </section>
    <div class="st-grid">
      <section class="card"><h2>Accuracy</h2>
        <p class="note">After you tick a module, type how many you got right beside it. Under 60% joins the weak list and shows up in that system's revision morning.</p>
        <h3>By QBank</h3>${hbars(pr(kinds),{max:100,empty:"No accuracy entered yet."})}
        <h3>By system</h3>${hbars(pr(syss),{max:100,empty:"No accuracy entered yet."})}
        <h3>Weak modules · under 60%</h3>${weak.length?`<div class="weak">${weak.map(w=>`<span><b class="pct lo">${w.p}%</b> ${esc(w.i.t)} · ${dayLabel(w.day)}</span>`).join("")}</div>`:`<p class="empty">None yet.</p>`}
      </section>
      <section class="card"><h2>Study hours</h2>
        <p class="note">From your ▶ Start / ■ End taps; the outline is the time you planned that day.</p>
        <div class="legend2"><span><i style="background:var(--hl-mar)"></i>Actual</span><span><i style="border:2px solid var(--ink);opacity:.55"></i>Planned</span></div>
        ${hbars(hrows,{empty:"Tap ▶ Start now and ■ End now on modules to see your real hours here."})}
        <h3>How long questions really take</h3>${hbars(spRows(speed),{empty:"Appears after your first timed module."})}
        <h3>Your fastest time of day</h3>${hbars(spRows(tod).sort((a,b)=>a.v-b.v),{empty:"Appears after a few timed modules."})}
      </section>
    </div></div>`;
  bindScoreInputs(v,()=>{ $("#stChart").innerHTML=testsChart(); $("#stLoss").innerHTML=lossBars(); });
}
function toast(msg){''')

# ================= render switch =================
rep('''  $("#planView").hidden = (tab==="clock"||tab==="hy"||tab==="mar"); $("#clockView").hidden = tab!=="clock"; $("#hyView").hidden = tab!=="hy"; $("#marView").hidden = tab!=="mar";''','''  $("#planView").hidden = (tab==="clock"||tab==="hy"||tab==="mar"||tab==="stats"); $("#clockView").hidden = tab!=="clock"; $("#hyView").hidden = tab!=="hy"; $("#marView").hidden = tab!=="mar"; $("#statsView").hidden = tab!=="stats";''')
rep('''  if(tab==="clock") renderClock(); else if(tab==="hy") renderHY(); else if(tab==="mar") renderMarrow(); else { renderRibbon(); renderSheet(scroll); }''','''  if(tab==="clock") renderClock(); else if(tab==="hy") renderHY(); else if(tab==="mar") renderMarrow(); else if(tab==="stats") renderStats(); else { renderRibbon(); renderSheet(scroll); }''')

# ================= break nudge =================
rep('''setInterval(()=>document.querySelectorAll(".live").forEach(el=>el.textContent=fmtM(mins(el.dataset.since,new Date().toISOString()))),30000);''','''let nudged={}; try{ nudged=JSON.parse(localStorage.getItem("neetss-nudged")||"{}")||{}; }catch(e){}
function checkNudge(){
  const now=new Date().toISOString();
  for(const id in actual){ const a=actual[id]; if(!a||!a.s||a.e||nudged[a.s]) continue;
    if(mins(a.s,now)>=90){ const r=ITEMBY[id]; nudged[a.s]=1; try{ localStorage.setItem("neetss-nudged",JSON.stringify(nudged)); }catch(e){}
      $("#nudgeT").innerHTML=`<b>${fmtM(mins(a.s,now))}</b> on ${esc(r?r.i.t:"this module")}. Take a 10-minute break: stand up, water, look out of a window.`;
      $("#nudge").hidden=false; break; } }
}
setInterval(()=>{ document.querySelectorAll(".live").forEach(el=>el.textContent=fmtM(mins(el.dataset.since,new Date().toISOString()))); checkNudge(); },30000);''')
rep('''loadLocal(); goToday(); renderAll(true); connect();''','''$("#nudgeOk").onclick=()=>{ $("#nudge").hidden=true; };
loadLocal(); goToday(); renderAll(true); connect(); setTimeout(checkNudge,1500);''')

open(p,'w').write(t); print('template ok')
b='build.py'; s=open(b).read()
for a,c in [('done,times,actual,updatedAt:localStamp()||stamp()','done,times,actual,ext,updatedAt:localStamp()||stamp()'),
            ('actual=Object.assign({},remote.actual||{}); saveLocal();','actual=Object.assign({},remote.actual||{}); ext=normExt(remote.ext); saveLocal();')]:
    assert a in s, a; s=s.replace(a,c)
open(b,'w').write(s); print('build ok')

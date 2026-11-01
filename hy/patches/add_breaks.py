p='tracker.tpl.html'; t=open(p).read()
def rep(a,b,n=1):
    global t
    assert t.count(a)==n,(a[:90],t.count(a)); t=t.replace(a,b)

# ---------- data ----------
rep('''sleep:Object.assign({},x.sleep||{}), bed:x.bed||null}; }''','''sleep:Object.assign({},x.sleep||{}), bed:x.bed||null, brk:Array.isArray(x.brk)?x.brk.map(b=>Object.assign({},b)):[]}; }''')
rep('''let ext = {acc:{}, moved:{}, scores:{}, dt:{}, sleep:{}, bed:null};''','''let ext = {acc:{}, moved:{}, scores:{}, dt:{}, sleep:{}, bed:null, brk:[]};''')

# ---------- CSS ----------
rep('''.sl-row .tm-in{width:112px}''','''.sl-row .tm-in{width:112px}
.brk-row{display:flex;flex-wrap:wrap;align-items:center;gap:6px 8px;font-size:13.5px;color:var(--muted)}
.brk-row .sl-l{font-weight:800;color:var(--ink);margin-right:2px}
.bk{font:inherit;font-size:12.5px;font-weight:800;border-radius:99px;padding:5px 11px;border:1.5px solid var(--line);background:var(--surface);color:var(--ink);cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.bk i{width:9px;height:9px;border-radius:50%;background:var(--bkc)}
.bk:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.brk-on{display:inline-flex;flex-wrap:wrap;align-items:center;gap:8px;padding:5px 10px;border-radius:10px;background:color-mix(in srgb,var(--bkc) 18%,var(--surface));color:var(--ink)}
.brk-on b{font-family:var(--f-mono)}
.brk-past summary{cursor:pointer;color:var(--accent);font-weight:700;font-size:13px}
.brk-past>div{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:8px;font-size:13px;color:var(--muted)}
.brk-past select,.brk-past input[type=text]{font:inherit;font-size:13px;color:var(--ink);background:var(--surface);border:1.5px solid var(--line);border-radius:9px;padding:5px 8px;min-height:34px}
.brk-past input[type=text]{width:150px}
.brk-past .tm-in{width:112px}
.brk-list{display:grid;gap:4px;margin-top:8px;font-size:13px}
.brk-list span{display:flex;align-items:center;gap:8px}
.brk-list b{font-family:var(--f-mono);font-size:12px}
.brk-list .dot{width:9px;height:9px;border-radius:50%;background:var(--bkc);display:inline-block;flex:0 0 auto}
.bk-lunch{--bkc:#E39A0B} .bk-dinner{--bkc:#B5654A} .bk-series{--bkc:#D6409F} .bk-nap{--bkc:#7C5CFC} .bk-other{--bkc:#0FA3A3}
.tl-bk{background:var(--bkc)}''')

# ---------- helpers (after timelineList so dayTimeline can use them) ----------
rep('''function dayTimeline(date){''','''// ---------- named breaks: lunch, dinner, series, short nap, other ----------
const BRK={lunch:{l:"Lunch",max:45},dinner:{l:"Dinner",max:45},series:{l:"Series",max:30},nap:{l:"Short nap",max:30},other:{l:"Break",max:30}};
const brkName=b=>b.k==="other"&&b.n?b.n:(BRK[b.k]||BRK.other).l;
function brkList(){ return Array.isArray(ext.brk)?ext.brk:(ext.brk=[]); }
function runningBrk(){ const l=brkList(); for(let k=l.length-1;k>=0;k--) if(!l[k].e) return l[k]; return null; }
function brkOn(date){ const now=nowISO(); return brkList().filter(b=>b.s&&dayOf(b.s)===date).map(b=>({a:minOf(b.s,date),b:minOf(b.e||now,date),k:BRK[b.k]?b.k:"other",label:brkName(b),ref:b})).filter(x=>x.b>x.a).sort((x,y)=>x.a-y.a); }
function overlapM(a,b,gaps){ let s=0; gaps.forEach(g=>{ const lo=Math.max(a,g.a), hi=Math.min(b,g.b); if(hi>lo) s+=hi-lo; }); return s; }
function brkTotals(date,tl){ const tot={}; if(!tl) return tot; brkOn(date).forEach(x=>{ const m=overlapM(x.a,x.b,tl.gaps); if(m>0) tot[x.label]=(tot[x.label]||0)+m; }); return tot; }
function brkSummary(date,tl){ const tot=brkTotals(date,tl), named=Object.values(tot).reduce((a,b)=>a+b,0), parts=Object.entries(tot).map(([k,v])=>`${k} ${fmtM(v)}`); if(!parts.length) return ""; const rest=Math.max(0,(tl?tl.brk:0)-named); return parts.join(" · ")+(rest>=1?` · other ${fmtM(rest)}`:""); }
function endRunningBrk(now){ const rb=runningBrk(); if(rb) rb.e=now; return rb; }
function startBrk(k,name){
  const now=nowISO(); endRunningBrk(now);
  let pid=null; for(const id in actual){ const a=actual[id]; if(a&&a.s&&!a.e&&!isPaused(a)){ actual[id]=Object.assign(JSON.parse(JSON.stringify(a)),{p:pauses(a).concat([{f:now}])}); pid=id; } }
  const b={k:BRK[k]?k:"other",s:now}; if(name) b.n=String(name).slice(0,40); if(pid) b.pid=pid;
  brkList().push(b); queueSave(); renderAll(); coachEvent("brk_s",null,b);
}
function endBrk(){
  const now=nowISO(), b=runningBrk(); if(!b) return; b.e=now;
  let res=null; if(b.pid && actual[b.pid] && isPaused(actual[b.pid]) && !Object.keys(actual).some(id=>{ const a=actual[id]; return a&&a.s&&!a.e&&!isPaused(a); })){
    const a=JSON.parse(JSON.stringify(actual[b.pid])), p=pauses(a); p[p.length-1].t=now; a.p=p; actual[b.pid]=a; res=b.pid; }
  queueSave(); renderAll(); coachEvent("brk_e",null,{b,res});
}
function brkRowHTML(d){
  if(d.date!==TODAY) return "";
  const rb=runningBrk(), list=brkOn(d.date);
  let h=`<div class="brk-row"><span class="sl-l">Break</span>`;
  if(rb){ const m=mins(rb.s,nowISO()), mx=(BRK[rb.k]||BRK.other).max;
    h+=`<span class="brk-on bk-${BRK[rb.k]?rb.k:"other"}">On <b>${esc(brkName(rb))}</b> since <b>${hm(rb.s)}</b> · <b class="${m>mx?"over":""}">${fmtM(m)}</b>${rb.pid&&ITEMBY[rb.pid]?` · ${esc(ITEMBY[rb.pid].i.t)} paused`:""}</span><button class="ab end bk-end">■ End break${rb.pid&&ITEMBY[rb.pid]?" &amp; resume":""}</button>`; }
  else h+=Object.keys(BRK).filter(k=>k!=="other").map(k=>`<button class="bk bk-${k}" data-k="${k}"><i></i>${BRK[k].l}</button>`).join("")+`<button class="bk bk-other" data-k="other"><i></i>Other…</button><span class="bk-oth" hidden><input type="text" class="bk-name" maxlength="40" placeholder="Name, e.g. Gym" aria-label="Name of the break"><button class="ab start bk-go">▶ Start</button></span>`;
  h+=`</div><details class="brk-past"><summary>Add a break you forgot to log${list.length?` · ${plural(list.length,"named break")} today`:""}</summary><div><select class="bp-k" aria-label="Break type">${Object.keys(BRK).map(k=>`<option value="${k}">${k==="other"?"Other":BRK[k].l}</option>`).join("")}</select><input type="text" class="bp-n" maxlength="40" placeholder="Name (for Other)" aria-label="Break name"><input type="time" class="tm-in bp-s" step="60" aria-label="Break start"><span>to</span><input type="time" class="tm-in bp-e" step="60" aria-label="Break end"><button class="ab start bp-add">Add</button></div>${list.length?`<div class="brk-list">${list.map((x,i)=>`<span><i class="dot bk-${x.k}"></i><b>${clock(x.a)}–${x.ref.e?clock(x.b):"now"}</b>${esc(x.label)} · ${fmtM(x.b-x.a)}<button class="ab x bp-del" data-i="${brkList().indexOf(x.ref)}" aria-label="Delete this break">×</button></span>`).join("")}</div>`:""}</details>`;
  return h;
}
function bindBrk(root,d){
  if(!root) return;
  root.querySelectorAll(".bk[data-k]").forEach(b=>b.onclick=()=>{ if(b.dataset.k==="other"){ const o=root.querySelector(".bk-oth"); if(o){ o.hidden=false; const n=o.querySelector(".bk-name"); if(n) n.focus(); } } else startBrk(b.dataset.k); });
  const go=root.querySelector(".bk-go"); if(go) go.onclick=()=>{ const n=root.querySelector(".bk-name"); startBrk("other",n&&n.value.trim()); };
  const nm=root.querySelector(".bk-name"); if(nm) nm.onkeydown=e=>{ if(e.key==="Enter") startBrk("other",nm.value.trim()); };
  const en=root.querySelector(".bk-end"); if(en) en.onclick=endBrk;
  const add=root.querySelector(".bp-add"); if(add) add.onclick=()=>{
    const k=root.querySelector(".bp-k").value, n=root.querySelector(".bp-n").value.trim(), s=root.querySelector(".bp-s").value, e=root.querySelector(".bp-e").value;
    if(!s||!e){ toast("Pick a start and end time for the break"); return; }
    const base=Date.parse(d.date+"T00:00:00+05:30"), sm=toMin(s); let em=toMin(e); const wm=wakeMinOf(d.date);
    const sAbs=sm<(wm!=null?Math.min(wm,720):DAY_CUT)?sm+1440:sm; if(em<=sm) em+=1440; const eAbs=sAbs+(em-sm);
    const b={k,s:new Date(base+sAbs*60000).toISOString(),e:new Date(base+eAbs*60000).toISOString()}; if(k==="other"&&n) b.n=n.slice(0,40);
    brkList().push(b); queueSave(); renderAll(); toast(`${brkName(b)} ${s}–${e} added`); };
  root.querySelectorAll(".bp-del").forEach(b=>b.onclick=()=>{ const i=+b.dataset.i, l=brkList(); if(l[i]){ l.splice(i,1); queueSave(); renderAll(); } });
}
function dayTimeline(date){''')

# timeline carries named breaks
rep('''  return {iv,gaps:g,start,end,sl,bed,nowM,studied,brk,awake:start!=null&&end!=null?Math.max(0,end-start):null};''',
'''  return {iv,gaps:g,start,end,sl,bed,nowM,studied,brk,named:brkOn(date),awake:start!=null&&end!=null?Math.max(0,end-start):null};''')
rep('''  tl.gaps.forEach(x=>h+=seg(x.a,x.b,"brk",`Break ${clock(x.a)}–${clock(x.b)} · ${fmtM(x.b-x.a)}`));''',
'''  tl.gaps.forEach(x=>h+=seg(x.a,x.b,"brk",`Break ${clock(x.a)}–${clock(x.b)} · ${fmtM(x.b-x.a)}`));
  (tl.named||[]).forEach(x=>{ h+=`<i class="tl-bk bk-${x.k}" style="left:${pc(x.a)}%;width:${Math.max(.35,pc(x.b)-pc(x.a))}%" title="${esc(x.label)} ${clock(x.a)}–${clock(x.b)} · ${fmtM(x.b-x.a)}"></i>`; });''')
rep('''  tl.gaps.forEach(x=>ev.push([x.a+.1,`<b>${clock(x.a)}</b>Break ${fmtM(x.b-x.a)} (to ${clock(x.b)})`]));''',
'''  const nm=tl.named||[];
  nm.forEach(x=>ev.push([x.a+.05,`<b>${clock(x.a)}</b>${esc(x.label)} ${fmtM(x.b-x.a)} (to ${clock(x.b)})`]));
  tl.gaps.forEach(x=>{ const rest=(x.b-x.a)-overlapM(x.a,x.b,nm.map(n=>({a:n.a,b:n.b}))); if(rest>=1) ev.push([x.a+.1,`<b>${clock(x.a)}</b>${nm.length?"Unlabelled break":"Break"} ${fmtM(rest)}${rest<x.b-x.a-0.5?"":` (to ${clock(x.b)})`}`]); });''')

# coach panel: break row + breakdown
rep('''    ${d.date<=todayIST()?sleepRowHTML(d):""}''','''    ${d.date<=todayIST()?sleepRowHTML(d):""}
    ${brkRowHTML(d)}''')
rep('''  bindSleep(el,d);
  bindAI(el);''','''  bindSleep(el,d);
  bindBrk(el,d);
  bindAI(el);''')
rep('''<span><i class="tl-brk"></i>Break · not studying</span></div>''','''<span><i class="tl-brk"></i>Break · not studying</span>${(tl.named||[]).length?[...new Set(tl.named.map(x=>x.k))].map(k=>`<span><i class="tl-bk bk-${k}"></i>${k==="other"?"Other break":BRK[k].l}</span>`).join(""):""}</div>${(()=>{ const s=brkSummary(d.date,tl); return s?`<p class="note">Breaks: ${s}</p>`:""; })()}''')

# act(): starting/resuming a module ends a running break; ending/clearing never touches it
rep('''  const others=fn=>{ for(const k in actual){ const o=actual[k]; if(k!==id && o && o.s && !o.e && !isPaused(o)) actual[k]=fn(JSON.parse(JSON.stringify(o))); } };
  if(what==="s"){''','''  const others=fn=>{ for(const k in actual){ const o=actual[k]; if(k!==id && o && o.s && !o.e && !isPaused(o)) actual[k]=fn(JSON.parse(JSON.stringify(o))); } };
  let endedBrk=null; if(what==="s"||what==="r"){ endedBrk=endRunningBrk(now); }
  if(what==="s"){''')
rep('''  queueSave(); renderAll(); coachEvent(what,id);
}
let nudged={};''','''  queueSave(); renderAll(); coachEvent(what,id,endedBrk?{brk:endedBrk}:undefined);
}
let nudged={};''')
rep('''  ext.bed=now; queueSave(); renderAll(); coachEvent("bed",null,todayIST());''','''  endRunningBrk(now); ext.bed=now; queueSave(); renderAll(); coachEvent("bed",null,todayIST());''')
rep('''  else if(o.t==="wake") wakeNow();''','''  else if(o.t==="wake") wakeNow();
  else if(o.t==="brkEnd") endBrk();''')

# coach events
rep('''  const r=ITEMBY[id], i=r?r.i:null; if(!i && !["plan","bed","wake"].includes(type)) return;''','''  const r=ITEMBY[id], i=r?r.i:null; if(!i && !["plan","bed","wake","brk_s","brk_e"].includes(type)) return;''')
rep('''  if(type==="s"){
    title=`Started ${i.t}`;''','''  if((type==="s"||type==="r") && extra && extra.brk){ const b=extra.brk, m=mins(b.s,b.e), mx=(BRK[b.k]||BRK.other).max; L.push(`${esc(brkName(b))} ended: ${fmtM(m)}${m>mx?`, ${fmtM(m-mx)} over the ${mx}-minute guide`:""}.`); }
  if(type==="s"){
    title=`Started ${i.t}`;''')
rep('''  } else if(type==="wake"){''','''  } else if(type==="brk_s"){
    const b=extra, nm=esc(brkName(b)), mx=(BRK[b.k]||BRK.other).max; title=`${brkName(b)} started`;
    if(b.pid&&ITEMBY[b.pid]) L.push(`<b>${esc(ITEMBY[b.pid].i.t)}</b> is paused. "End break" resumes it.`);
    if(b.k==="lunch") L.push(`Keep lunch under ${mx} min and light: a heavy, carb-rich meal deepens the afternoon dip. A 10-minute walk after helps.`);
    else if(b.k==="dinner") L.push(`Keep dinner under ${mx} min. Eat at least 2 hours before 23:00 lights out so it doesn't spoil your sleep.`);
    else if(b.k==="series") L.push(`Set a ${mx}-minute timer: one episode, then back. Series breaks run long because autoplay starts the next one, so turn it off.`);
    else if(b.k==="nap") L.push(`Set an alarm for 20 minutes. A 10–20 minute nap restores alertness; past 30 minutes you drop into deep sleep and wake up groggy.`);
    else L.push(`${nm}: aim to be back within ${mx} min.`);
    const tl=dayTimeline(todayIST()); if(tl&&tl.awake) L.push(`Breaks so far today: ${fmtM(tl.brk)} of ${fmtM(tl.awake)} awake.`);
    if(b.k==="nap" && nowMin()>=1020) L.push(`It's late for a nap; it can push tonight's sleep later. Keep it to 15 minutes.`);
    d0=TODAY;
  } else if(type==="brk_e"){
    const b=extra.b, m=mins(b.s,b.e), mx=(BRK[b.k]||BRK.other).max; title=`${brkName(b)} · ${fmtM(m)}`;
    L.push(m>mx?`${fmtM(m-mx)} over the ${mx}-minute guide.`:`Within the ${mx}-minute guide.`);
    if(b.k==="nap") L.push(m>30?`Long nap. Splash water on your face and start with an easier module for 15 minutes.`:`Good length. Light and water now, then straight back in.`);
    if(extra.res&&ITEMBY[extra.res]) L.push(`Resumed <b>${esc(ITEMBY[extra.res].i.t)}</b>.`);
    else { const td=ALLDAYS.find(x=>x.date===TODAY); if(td){ const nx=nextUp(dayStatus(td)); if(nx) L.push(`Next: <b>${esc(nx.t)}</b>${nx.q?` (${nx.q} Qs)`:""}.`); } }
    const tl=dayTimeline(todayIST()), s=tl?brkSummary(TODAY,tl):""; if(s) L.push(`Breaks today: ${s}.`);
    d0=TODAY;
  } else if(type==="wake"){''')

# coach suggestions while a break runs (put at top of today's block)
rep('''  } else if(st.isToday){
    const nm=nowMin(), run=runningItem();''','''  } else if(st.isToday){
    const nm=nowMin(), run=runningItem(), rb=runningBrk();
    if(rb){ const m=mins(rb.s,nowISO()), mx=(BRK[rb.k]||BRK.other).max;
      if(m>mx) push(4,`<b>${esc(brkName(rb))}</b> has run ${fmtM(m)}, ${fmtM(m-mx)} past the ${mx}-minute guide.${rb.k==="nap"?" Get up now; a longer nap leaves you groggy.":rb.k==="series"?" Stop at the end of this scene.":""}`,{t:"brkEnd",label:"End break"});
      else push(2,`On <b>${esc(brkName(rb))}</b> for ${fmtM(m)} (guide ${mx} min).`,{t:"brkEnd",label:"End break"}); }
    { const tl0=dayTimeline(TODAY), tot=brkTotals(TODAY,tl0); if((tot[BRK.series.l]||0)>=60) push(3,`${fmtM(tot[BRK.series.l])} of series today. Save the next episode as a reward for finishing Block C.`); }''')

# stats card: named break totals over 14 days
rep('''return hbars(rows,{max:9,empty:"Nothing logged yet. Tap \\"I'm up now\\" in the Coach panel tomorrow morning."}); })()}''',
'''return hbars(rows,{max:9,empty:"Nothing logged yet. Tap \\"I'm up now\\" in the Coach panel tomorrow morning."}); })()}
      ${(()=>{ const tot={}, days=new Set(); for(let k=13;k>=0;k--){ const dt=dateAdd(todayIST(),-k), tl=dayTimeline(dt), t2=brkTotals(dt,tl); Object.entries(t2).forEach(([n,v])=>{ tot[n]=(tot[n]||0)+v; days.add(dt); }); }
        const rows=Object.entries(tot).sort((a,b)=>b[1]-a[1]).map(([n,v])=>{ const k=Object.keys(BRK).find(x=>BRK[x].l===n)||"other"; return {lab:n,v:v/60,txt:`${fmtM(v)} total · ${fmtM(v/Math.max(1,days.size))} a day`,color:`var(--bkc)`,cls:`bk-${k}`}; });
        return `<h3>Named breaks · last 14 days</h3>`+(rows.length?`<div class="hb">${rows.map(r=>`<div class="hb-row ${r.cls}"><span class="lab">${esc(r.lab)}</span><span class="hb-track"><span class="hb-fill" style="width:${Math.min(100,100*r.v/Math.max(...rows.map(x=>x.v)))}%;--bc:var(--bkc)"></span></span><span class="v">${r.txt}</span></div>`).join("")}</div>`:`<p class="empty">No named breaks yet. Use the Lunch, Dinner, Series or Short nap buttons in the Coach panel.</p>`); })()}''')

# AI summary
rep('''  const tlT=dayTimeline(todayIST()); if(tlT) lines.push(`Today: studied ${tlT.studied} min, breaks (awake, not studying) ${tlT.brk} min, awake ${tlT.awake||0} min.`);''',
'''  const tlT=dayTimeline(todayIST()); if(tlT) lines.push(`Today: studied ${tlT.studied} min, breaks (awake, not studying) ${tlT.brk} min, awake ${tlT.awake||0} min.`);
  if(tlT){ const bs=brkSummary(todayIST(),tlT); if(bs) lines.push(`Named breaks today: ${bs}.`); }''')
open(p,'w').write(t); print('ok')

p='tracker.tpl.html'; t=open(p).read()
def rep(a,b):
    global t
    assert t.count(a)==1,(a[:100],t.count(a)); t=t.replace(a,b)

# ---------- state ----------
rep('''function normExt(x){ x=x||{}; return {acc:Object.assign({},x.acc||{}), moved:Object.assign({},x.moved||{}), scores:Object.assign({},x.scores||{}), dt:Object.assign({},x.dt||{})}; }''',
    '''function normExt(x){ x=x||{}; return {acc:Object.assign({},x.acc||{}), moved:Object.assign({},x.moved||{}), scores:Object.assign({},x.scores||{}), dt:Object.assign({},x.dt||{}), sleep:Object.assign({},x.sleep||{}), bed:x.bed||null}; }''')
rep("let ext = {acc:{}, moved:{}, scores:{}, dt:{}};","let ext = {acc:{}, moved:{}, scores:{}, dt:{}, sleep:{}, bed:null};")

# ---------- CSS ----------
rep(".co-stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}",".co-stats{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px}\n@media (max-width:980px){.co-stats{grid-template-columns:repeat(3,minmax(0,1fr))}}")
rep(".rep{display:grid;gap:6px;margin:0;padding-left:18px;font-size:14px;line-height:1.45}",""".rep{display:grid;gap:6px;margin:0;padding-left:18px;font-size:14px;line-height:1.45}
.sl-row{display:flex;flex-wrap:wrap;align-items:center;gap:8px;font-size:13.5px;color:var(--muted)}
.sl-row .sl-l{font-weight:800;color:var(--ink)}
.sl-row .tm-in{width:112px}
.tl{display:grid;gap:4px}
.tl-strip{position:relative;height:22px;border-radius:7px;background:var(--surface-2);overflow:hidden}
.tl-strip i{position:absolute;top:0;bottom:0}
.tl-sleep{background:color-mix(in srgb,var(--accent) 42%,transparent)}
.tl-brk{background:repeating-linear-gradient(135deg,color-mix(in srgb,var(--warn) 60%,transparent) 0 4px,transparent 4px 8px)}
.tl-main{background:var(--hl-main)} .tl-ss{background:var(--hl-ss)} .tl-qrp{background:var(--hl-qrp)} .tl-mar{background:var(--hl-mar)} .tl-pyq{background:var(--hl-pyq)} .tl-task,.tl-hy{background:var(--hl-task)}
.tl-now{position:absolute;top:-2px;bottom:-2px;width:2px;background:var(--ink)}
.tl-ax{position:relative;height:14px;font-family:var(--f-mono);font-size:10.5px;color:var(--muted)}
.tl-ax span{position:absolute;transform:translateX(-50%)} .tl-ax span:first-child{transform:none} .tl-ax span:last-child{transform:translateX(-100%)}
.tl-key{display:flex;flex-wrap:wrap;gap:12px;font-size:12px;color:var(--muted)}
.tl-key i{display:inline-block;width:14px;height:10px;border-radius:3px;margin-right:5px;vertical-align:-1px}""")

# ---------- sleep & break model (inserted after the coach helpers) ----------
rep('''function act2(o){''','''// ---------- sleep and breaks: any awake time not spent studying counts as a break ----------
const dKey=iso=>DKF.format(new Date(iso));
const minOf=(iso,date)=>Math.round((Date.parse(iso)-Date.parse(date+"T00:00:00+05:30"))/60000);
function sleepOf(date){ const s=ext.sleep[date]; if(!s||!s.w) return null; const w=toMin(s.w), b=s.b?toMin(s.b):null; return {b:s.b||"",w:s.w,wm:w,dur:b==null?null:(((w-b)%1440)+1440)%1440}; }
function bedOf(date){
  const n=dateAdd(date,1), s=ext.sleep[n];
  if(s&&s.b){ const bm=toMin(s.b); return bm>=720?bm:bm+1440; }
  if(ext.bed){ const k=dKey(ext.bed); if(k===date||(k===n&&minOf(ext.bed,n)<720)) return minOf(ext.bed,date); }
  return null;
}
function activeIntervals(date){
  const out=[], now=nowISO();
  for(const id in actual){ const a=actual[id]; if(!a||!a.s||dKey(a.s)!==date) continue;
    const r=ITEMBY[id], k=r?r.i.k:"task", tt=r?r.i.t:"", end=a.e||now; let cur=a.s;
    pauses(a).slice().sort((x,y)=>x.f.localeCompare(y.f)).forEach(p=>{ if(p.f>cur) out.push({a:minOf(cur,date),b:minOf(p.f,date),k,t:tt}); cur=p.t||end; });
    if(end>cur) out.push({a:minOf(cur,date),b:minOf(end,date),k,t:tt}); }
  return out.filter(x=>x.b>x.a).sort((x,y)=>x.a-y.a);
}
function dayTimeline(date){
  const iv=activeIntervals(date), sl=sleepOf(date), bed=bedOf(date), isT=date===todayIST();
  if(!iv.length&&!sl&&bed==null) return null;
  const start=sl?sl.wm:(iv.length?iv[0].a:null), nowM=isT?minOf(nowISO(),date):null;
  const end=bed!=null?bed:(isT?nowM:(iv.length?iv[iv.length-1].b:start));
  const gaps=[]; let cur=start;
  if(start!=null&&end!=null){ iv.forEach(x=>{ if(x.a>cur) gaps.push({a:cur,b:Math.min(x.a,end)}); cur=Math.max(cur,x.b); }); if(end>cur) gaps.push({a:cur,b:end}); }
  const g=gaps.filter(x=>x.b-x.a>=1), studied=iv.reduce((s,x)=>s+(x.b-x.a),0), brk=g.reduce((s,x)=>s+(x.b-x.a),0);
  return {iv,gaps:g,start,end,sl,bed,nowM,studied,brk,awake:start!=null&&end!=null?Math.max(0,end-start):null};
}
function stripHTML(tl){
  const span=Math.max(1440,tl.end||0,...tl.iv.map(x=>x.b)), pc=m=>Math.max(0,Math.min(100,100*m/span));
  const seg=(a,b,c,ti)=>`<i class="tl-${c}" style="left:${pc(a)}%;width:${Math.max(.35,pc(b)-pc(a))}%" title="${esc(ti)}"></i>`;
  let h=`<div class="tl-strip" role="img" aria-label="Day timeline: ${fmtM(tl.studied)} studied, ${fmtM(tl.brk)} breaks${tl.sl&&tl.sl.dur?`, ${fmtM(tl.sl.dur)} sleep last night`:""}">`;
  if(tl.sl) h+=seg(0,tl.sl.wm,"sleep",`Sleep until ${tl.sl.w}`);
  if(tl.bed!=null) h+=seg(tl.bed,span,"sleep",`Sleep from ${clock(tl.bed)}`);
  tl.gaps.forEach(x=>h+=seg(x.a,x.b,"brk",`Break ${clock(x.a)}–${clock(x.b)} · ${fmtM(x.b-x.a)}`));
  tl.iv.forEach(x=>h+=seg(x.a,x.b,x.k,`${x.t} ${clock(x.a)}–${clock(x.b)}`));
  if(tl.nowM!=null&&tl.bed==null&&tl.nowM<=span) h+=`<b class="tl-now" style="left:${pc(tl.nowM)}%"></b>`;
  return h+`</div><div class="tl-ax">${[0,6,12,18,24].map(x=>`<span style="left:${pc(x*60)}%">${String(x).padStart(2,"0")}</span>`).join("")}</div>`;
}
function timelineList(tl){
  const ev=[]; if(tl.sl) ev.push([tl.sl.wm,`<b>${tl.sl.w}</b>Woke up${tl.sl.dur?` · slept ${fmtM(tl.sl.dur)}`:""}`]);
  tl.iv.forEach(x=>ev.push([x.a,`<b>${clock(x.a)}</b>${esc(x.t)} · studied ${fmtM(x.b-x.a)}`]));
  tl.gaps.forEach(x=>ev.push([x.a+.1,`<b>${clock(x.a)}</b>Break ${fmtM(x.b-x.a)} (to ${clock(x.b)})`]));
  if(tl.bed!=null) ev.push([tl.bed+.2,`<b>${clock(tl.bed)}</b>Went to sleep`]);
  return ev.sort((a,b)=>a[0]-b[0]).map(e=>`<span>${e[1]}</span>`).join("");
}
function sleepNights(n){ const o=[]; for(let k=0;k<n;k++){ const dt=dateAdd(todayIST(),-k), s=sleepOf(dt); if(s&&s.dur) o.push({dt,dur:s.dur}); } return o; }
function sleepRowHTML(d){
  const date=d.date, isT=date===todayIST(), s=ext.sleep[date]||{}, sl=sleepOf(date);
  let btn="";
  if(isT){ if(!s.w) btn=`<button class="ab start sl-act" data-a="wake">I'm up now</button>`;
    else if(!ext.bed && nowMin()>=1080) btn=`<button class="ab end sl-act" data-a="bed">Going to sleep</button>`;
    else if(ext.bed) btn=`<span>Sleeping since <b>${hm(ext.bed)}</b></span>`; }
  if(isT && ext.bed && !s.w) btn=`<span>Went to sleep at <b>${hm(ext.bed)}</b></span>`+btn;
  const c=sl&&sl.dur!=null?(sl.dur<360?"lo":sl.dur<420?"mid":"hi"):"";
  return `<div class="sl-row"><span class="sl-l">Night before ${isT?"today":"this day"}</span>slept <input type="time" class="tm-in sl-in ${s.b?"set":""}" data-f="b" value="${s.b||""}" aria-label="Bedtime the night before">woke <input type="time" class="tm-in sl-in ${s.w?"set":""}" data-f="w" value="${s.w||""}" aria-label="Wake-up time">${sl&&sl.dur!=null?`<b class="pct ${c}">${fmtM(sl.dur)}</b>`:""}${btn}</div>`;
}
function bedNow(){
  const now=nowISO();
  for(const k in actual){ const a=actual[k]; if(a&&a.s&&!a.e){ const o=JSON.parse(JSON.stringify(a)); const p=pauses(o); if(p.length&&!p[p.length-1].t) p[p.length-1].t=now; o.p=p; o.e=now; actual[k]=o; } }
  ext.bed=now; queueSave(); renderAll(); coachEvent("bed",null,todayIST());
}
function wakeNow(){
  const now=nowISO(), today=todayIST(), s=Object.assign({},ext.sleep[today]||{});
  s.w=hm(now); if(ext.bed && mins(ext.bed,now)<20*60) s.b=hm(ext.bed);
  ext.sleep[today]=s; ext.bed=null; queueSave(); renderAll(); coachEvent("wake",null,today);
}
function bindSleep(root,d){
  if(!root) return;
  root.querySelectorAll(".sl-in").forEach(inp=>inp.onchange=()=>{ const s=Object.assign({},ext.sleep[d.date]||{}); if(inp.value) s[inp.dataset.f]=inp.value; else delete s[inp.dataset.f];
    if(s.b||s.w) ext.sleep[d.date]=s; else delete ext.sleep[d.date]; queueSave(); renderCoach(d); });
  root.querySelectorAll(".sl-act").forEach(b=>b.onclick=()=>{ if(b.dataset.a==="bed") bedNow(); else wakeNow(); });
}
function act2(o){''')

# ---------- coach panel: six numbers, sleep row, timeline ----------
rep('''  const stats=[
    ["Done",`${fmt(st.qDone)}/${fmt(st.qTot)} Qs`,st.qTot&&st.qDone===st.qTot?"good":""],''','''  const tl=dayTimeline(d.date), slp=sleepOf(d.date);
  const stats=[
    ["Done",`${fmt(st.qDone)}/${fmt(st.qTot)} Qs`,st.qTot&&st.qDone===st.qTot?"good":""],
    ["Breaks",tl?fmtM(tl.brk):"–",tl&&tl.awake>=120&&tl.brk/tl.awake>0.3?"warn":""],
    ["Sleep",slp&&slp.dur!=null?fmtM(slp.dur):"log it",slp&&slp.dur!=null?(slp.dur<360?"bad":slp.dur<420?"warn":"good"):""],''')
rep('''    <div class="co-stats">${stats.map(s=>`<div class="co-stat ${s[2]}"><span>${s[0]}</span><b>${s[1]}</b></div>`).join("")}</div>''','''    <div class="co-stats">${stats.map(s=>`<div class="co-stat ${s[2]}"><span>${s[0]}</span><b>${s[1]}</b></div>`).join("")}</div>
    ${d.date<=todayIST()?sleepRowHTML(d):""}
    ${tl?`<div class="tl">${stripHTML(tl)}<div class="tl-key"><span><i class="tl-sleep"></i>Sleep</span><span><i class="tl-main"></i>Studying (colour = QBank)</span><span><i class="tl-brk"></i>Break · not studying</span></div><details class="co-notes"><summary>Day timeline · studied ${fmtM(tl.studied)}, breaks ${fmtM(tl.brk)}${tl.awake?`, awake ${fmtM(tl.awake)}`:""}</summary><div>${timelineList(tl)}</div></details></div>`:""}''')
rep('''  el.querySelectorAll(".co-act").forEach(b=>b.onclick=()=>runAct(CO_ACTS[+b.dataset.k]));''','''  el.querySelectorAll(".co-act").forEach(b=>b.onclick=()=>runAct(CO_ACTS[+b.dataset.k]));
  bindSleep(el,d);''')
rep('''  else act(o.id,o.t);''','''  else if(o.t==="bed") bedNow();
  else if(o.t==="wake") wakeNow();
  else act(o.id,o.t);''')

# ---------- suggestions ----------
rep('''    const tot=st.studied+st.paused;
    if(st.studied>=60 && st.paused/tot>0.3) push(2,`Breaks are ${Math.round(100*st.paused/tot)}% of today's session time (${fmtM(st.paused)} paused). Try 50 minutes on, 10 off.`);''','''    const tl=dayTimeline(d.date), slp=sleepOf(d.date);
    if(!ext.sleep[d.date]||!ext.sleep[d.date].w) push(2,`Log when you woke up (or type it above) so sleep and breaks are counted from the start of your day.`,{t:"wake",label:"I'm up now"});
    if(tl && tl.awake>=120 && tl.brk/tl.awake>0.3) push(3,`Breaks are ${Math.round(100*tl.brk/tl.awake)}% of your awake time today (${fmtM(tl.brk)} of ${fmtM(tl.awake)}). The plan allows about 2 h 15 min a day for meals and breaks.`);
    if(slp&&slp.dur!=null&&slp.dur<360) push(3,`You slept ${fmtM(slp.dur)} last night. A 20-minute nap after lunch will help more than coffee; protect 23:00 lights out tonight.`);
    else if(slp&&slp.dur!=null&&slp.dur<420) push(1,`${fmtM(slp.dur)} of sleep last night, a little under the 7–7.5 h that memory consolidation needs.`);''')
rep('''      if(nx) push(3,`Next up: <b>${esc(nx.t)}</b>''','''      const tl2=dayTimeline(d.date), lastGap=tl2&&tl2.gaps.length?tl2.gaps[tl2.gaps.length-1]:null, idle=lastGap&&tl2.nowM!=null&&lastGap.b>=tl2.nowM-1?lastGap.b-lastGap.a:0;
      if(nx) push(idle>=30?4:3,`${idle>=20?`On a break for <b>${fmtM(idle)}</b>. `:""}Next up: <b>${esc(nx.t)}</b>''')
rep('''      push(4, nm>=LIGHTS_OUT ? `It's past 23:00.''','''      if(!ext.bed) push(3,`When you stop for the night, tap "Going to sleep" so tonight's sleep is counted.`,{t:"bed",label:"Going to sleep"});
      push(4, nm>=LIGHTS_OUT ? `It's past 23:00.''')

# ---------- coach events ----------
rep('''  const r=ITEMBY[id], i=r?r.i:null; if(!i && type!=="plan") return;''','''  const r=ITEMBY[id], i=r?r.i:null; if(!i && !["plan","bed","wake"].includes(type)) return;''')
rep('''  if(type==="s"){
    title=`Started ${i.t}`;''','''  if(type==="s"){
    title=`Started ${i.t}`;
    const tl=dayTimeline(todayIST()), g=tl&&tl.gaps.length?tl.gaps[tl.gaps.length-1]:null;
    if(g && tl.nowM!=null && g.b>=tl.nowM-1 && g.b-g.a>=3) L.push(`Back after a ${fmtM(g.b-g.a)} break.${g.b-g.a>=45?" That was a long one; a 5-minute skim of your last highlights will warm you up.":""}`);''')
rep('''  } else return;
  addLog(''','''  } else if(type==="bed"){
    const date=extra||todayIST(), tl=dayTimeline(date), bm=toMin(hm(ext.bed||nowISO())), late=(bm<720?bm+1440:bm)-LIGHTS_OUT;
    title="Good night";
    if(tl) L.push(`Today: ${fmtM(tl.studied)} studied, ${fmtM(tl.brk)} of breaks${tl.awake?` across ${fmtM(tl.awake)} awake`:""}.`);
    L.push(late>15?`Bedtime ${hm(ext.bed||nowISO())} is ${fmtM(late)} past 23:00. For 7.5 h, wake at ${clock(bm+450)}.`:`On time. 7.5 h of sleep means waking at ${clock(bm+450)}.`);
    const nd=ALLDAYS.find(x=>x.date===dateAdd(date,1)); if(nd){ const f=itemsOf(nd).find(x=>!isDone(x.id)&&x.k==="main")||itemsOf(nd).find(x=>!isDone(x.id)); if(f) L.push(`Tomorrow (${dayLabel(nd)}, ${esc(nd.title)}) starts with <b>${esc(f.t)}</b>.`); }
    d0=date;
  } else if(type==="wake"){
    const date=extra||todayIST(), sl=sleepOf(date), avg=sleepNights(7);
    title=sl&&sl.dur!=null?`Good morning · slept ${fmtM(sl.dur)}`:"Good morning";
    if(sl&&sl.dur!=null) L.push(sl.dur<360?`That's short. Put the toughest most-asked module after a 20-minute post-lunch nap and keep caffeine before 14:00.`:sl.dur<420?`Slightly under 7 h. Fine for today; aim for 23:00 tonight.`:`Well rested. Use the first 2.5 hours on the day's most-asked modules.`);
    else L.push(`Type last night's bedtime above to see how long you slept.`);
    if(avg.length>=3) L.push(`Average over your last ${avg.length} logged nights: ${fmtM(avg.reduce((a,x)=>a+x.dur,0)/avg.length)}.`);
    const td=ALLDAYS.find(x=>x.date===date); if(td){ const s2=dayStatus(td), f=nextUp(s2); L.push(`Today: ${dayLabel(td)}, ${esc(td.title)} · ${fmt(s2.qRem)} Qs, about ${fmtM(s2.remM)} at your pace.${f?` Start with <b>${esc(f.t)}</b>.`:""}`); }
    d0=date;
  } else return;
  addLog(''')
rep('''  const d=i?(curDay(id)||r.day):extra, st=d?dayStatus(d):null;''','''  let d0=null; const d=i?(curDay(id)||r.day):(extra&&extra.key?extra:null), st=d?dayStatus(d):null;''')
rep('''  addLog({t:nowISO(),d:(d&&d.date)||TODAY,title,lines:L});''','''  addLog({t:nowISO(),d:d0||(d&&d.date)||todayIST(),title,lines:L});''')

# ---------- report, Claude/Gemini summary, stats ----------
rep('''  const hy=(DATA.hy||[]).flatMap(s=>s.topics), hyd=hy.filter(x=>isDone(x.id)).length;''','''  const sn=sleepNights(7);
  if(sn.length){ const av=sn.reduce((a,x)=>a+x.dur,0)/sn.length, short=sn.filter(x=>x.dur<390).length; L.push(`Sleep: ${fmtM(av)} a night on average over ${plural(sn.length,"logged night")}${short?`; ${short} under 6.5 h`:""}.`);
    const by={s:[],n:[]}; sn.forEach(x=>{ const ss=sessions().filter(o=>o.i.k==="main"&&dKey(actual[o.id].s)===x.dt); if(ss.length){ const q=ss.reduce((a,o)=>a+o.q,0); by[x.dur<390?"s":"n"].push(ss.reduce((a,o)=>a+o.m,0)/q); } });
    if(by.s.length>=2&&by.n.length>=2){ const a=by.s.reduce((x,y)=>x+y,0)/by.s.length, b=by.n.reduce((x,y)=>x+y,0)/by.n.length; L.push(`After short nights your Main pace is ${a.toFixed(1)} min/Q against ${b.toFixed(1)} after normal nights.`); } }
  else L.push(`Log sleep with "I'm up now" and "Going to sleep" and I'll show how it affects your pace.`);
  const tlT=dayTimeline(todayIST()); if(tlT&&tlT.awake) L.push(`Today so far: ${fmtM(tlT.studied)} studied, ${fmtM(tlT.brk)} of breaks.`);
  const hy=(DATA.hy||[]).flatMap(s=>s.topics), hyd=hy.filter(x=>isDone(x.id)).length;''')
rep('''  const pend=ALLDAYS.filter(x=>x.date<TODAY).flatMap(x=>itemsOf(x).filter(i=>!isDone(i.id))); if(pend.length) lines.push(`Backlog''','''  const sn=sleepNights(7); if(sn.length) lines.push("Sleep last nights (min): "+sn.map(x=>`${x.dt} ${x.dur}`).join(", "));
  const tlT=dayTimeline(todayIST()); if(tlT) lines.push(`Today: studied ${tlT.studied} min, breaks (awake, not studying) ${tlT.brk} min, awake ${tlT.awake||0} min.`);
  const pend=ALLDAYS.filter(x=>x.date<TODAY).flatMap(x=>itemsOf(x).filter(i=>!isDone(i.id))); if(pend.length) lines.push(`Backlog''')
rep('''    </div></div>`;
  bindScoreInputs(v,''','''    </div>
    <section class="card"><h2>Sleep &amp; breaks</h2>
      <p class="note">Sleep from "I'm up now" / "Going to sleep" or the times you type; breaks are all awake time not spent studying, pauses included.</p>
      ${(()=>{ const rows=[]; for(let k=13;k>=0;k--){ const dt=dateAdd(todayIST(),-k), s=sleepOf(dt), tl=dayTimeline(dt); if(!(s&&s.dur)&&!tl) continue; rows.push({lab:nice(dt),v:s&&s.dur?s.dur/60:0,txt:[s&&s.dur?(s.dur/60).toFixed(1)+" h sleep":"no sleep logged",tl?(tl.studied/60).toFixed(1)+" h study":"",tl?(tl.brk/60).toFixed(1)+" h break":""].filter(Boolean).join(" · "),color:s&&s.dur<390?"var(--warn)":"var(--accent)"}); } return hbars(rows,{max:9,empty:"Nothing logged yet. Tap \\"I'm up now\\" in the Coach panel tomorrow morning."}); })()}
    </section></div>`;
  bindScoreInputs(v,''')
open(p,'w').write(t); print('template ok')

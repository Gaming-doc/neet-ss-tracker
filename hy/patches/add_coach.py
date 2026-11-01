p='tracker.tpl.html'; t=open(p).read()
def rep(a,b):
    global t
    assert t.count(a)==1,(a[:90],t.count(a)); t=t.replace(a,b)

# ================= CSS =================
rep("@media (prefers-reduced-motion:reduce)", """.coach{display:grid;gap:10px}
.coach .block-h h3::before{content:"";display:inline-block;width:9px;height:9px;border-radius:50%;background:var(--good);margin-right:7px;vertical-align:1px}
.co-stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.co-stat{background:var(--surface-2);border-radius:10px;padding:8px 10px;display:grid;gap:2px;min-width:0}
.co-stat b{font-family:var(--f-mono);font-size:15px;font-variant-numeric:tabular-nums;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.co-stat span{font-size:10.5px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);font-weight:800}
.co-stat.bad b{color:var(--bad)} .co-stat.warn b{color:var(--warn)} .co-stat.good b{color:var(--good)}
@media (max-width:620px){.co-stats{grid-template-columns:repeat(2,minmax(0,1fr))}}
.co-last{font-size:14px;line-height:1.45;padding:10px 12px;border-radius:10px;background:color-mix(in srgb,var(--accent) 9%,var(--surface));display:grid;gap:3px}
.co-last .co-when{font-family:var(--f-mono);font-size:11px;color:var(--muted)}
.co-list{display:grid;gap:6px;margin:0;padding:0;list-style:none}
.co-list li{display:flex;gap:10px;align-items:center;justify-content:space-between;font-size:14px;line-height:1.4;background:var(--surface-2);border-radius:10px;padding:8px 10px}
.co-list li .tx{min-width:0}
.co-list li.u4{box-shadow:inset 0 0 0 1.5px var(--bad)} .co-list li.u3{box-shadow:inset 0 0 0 1.5px var(--warn)}
.co-act{flex:0 0 auto;white-space:nowrap}
.co-notes summary{cursor:pointer;color:var(--accent);font-weight:700;font-size:13px}
.co-notes div{display:grid;gap:6px;margin-top:6px;font-size:13px}
.co-notes div span{display:block}
.co-notes b{font-family:var(--f-mono);font-size:11.5px;color:var(--muted);margin-right:6px}
.co-ai{display:grid;gap:8px}
.co-ai-out{white-space:pre-wrap;font-size:14px;line-height:1.5;background:var(--surface-2);border-radius:10px;padding:10px 12px}
.co-pop{position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:31;width:min(420px,calc(100% - 32px));background:var(--surface);color:var(--ink);border-radius:14px;box-shadow:0 10px 40px rgba(0,0,0,.25);border:1.5px solid var(--line);padding:12px 14px;display:grid;gap:6px;font-size:14px;line-height:1.45}
.co-pop-h{display:flex;justify-content:space-between;align-items:center;gap:10px}
.co-pop-h b{font-family:var(--f-display);font-size:15px}
.co-pop ul{margin:0;padding-left:18px;display:grid;gap:3px}
@media (max-width:520px){.co-pop{right:16px;left:16px;width:auto}}
.rep{display:grid;gap:6px;margin:0;padding-left:18px;font-size:14px;line-height:1.45}
@media (prefers-reduced-motion:reduce)""")

# ================= HTML: pop card =================
rep('''<div class="nudge" id="nudge" role="status" hidden>''','''<div class="co-pop" id="coachPop" role="status" aria-live="polite" hidden><div class="co-pop-h"><b id="cpT"></b><button class="ab x" id="cpX" aria-label="Close the coach note">×</button></div><ul id="cpB"></ul></div>
<div class="nudge" id="nudge" role="status" hidden>''')

# ================= state: tick dates =================
rep('''function normExt(x){ x=x||{}; return {acc:Object.assign({},x.acc||{}), moved:Object.assign({},x.moved||{}), scores:Object.assign({},x.scores||{})}; }''',
    '''function normExt(x){ x=x||{}; return {acc:Object.assign({},x.acc||{}), moved:Object.assign({},x.moved||{}), scores:Object.assign({},x.scores||{}), dt:Object.assign({},x.dt||{})}; }''')
rep("let ext = {acc:{}, moved:{}, scores:{}};","let ext = {acc:{}, moved:{}, scores:{}, dt:{}};")

# ================= hooks =================
rep('''  else { delete actual[id]; }
  queueSave(); renderAll();
}''','''  else { delete actual[id]; }
  queueSave(); renderAll(); coachEvent(what,id);
}''')
rep('''  if(done[id]) delete done[id]; else done[id]=1;''','''  if(done[id]){ delete done[id]; delete ext.dt[id]; } else { done[id]=1; ext.dt[id]=TODAY; }''')
rep('''  if(wasFull) toast(`${d.title} complete`);''','''  if(wasFull) toast(`${d.title} complete`);
  coachEvent(done[id]?"tick":null,id);''')
rep('''    items.forEach(i=>{ if(all) delete done[i.id]; else done[i.id]=1; });''','''    items.forEach(i=>{ if(all){ delete done[i.id]; delete ext.dt[i.id]; } else { if(!done[i.id]) ext.dt[i.id]=TODAY; done[i.id]=1; } });''')
rep('''    inp.onchange=()=>{ const v=show(); if(v==null) delete ext.acc[inp.dataset.id]; else { ext.acc[inp.dataset.id]=v; inp.value=v; } queueSave(); if(after) after(); };''',
    '''    inp.onchange=()=>{ const v=show(); if(v==null) delete ext.acc[inp.dataset.id]; else { ext.acc[inp.dataset.id]=v; inp.value=v; } queueSave(); if(after) after(); if(v!=null) coachEvent("acc",inp.dataset.id); else refreshCoach(); };''')
rep('''    inp.onchange=()=>{ const v=upd(); if(v!=null) inp.value=v; queueSave(); if(after) after(); };''','''    inp.onchange=()=>{ const v=upd(); if(v!=null) inp.value=v; queueSave(); if(after) after(); scoreSoon(inp.dataset.id); };''')
rep('''  queueSave(); renderAll(); toast(val==="__back"||val===orig?"Moved back":"Moved to "+dayLabel(DAYBY[val]));''','''  queueSave(); renderAll(); if(val==="__back"||val===orig) toast("Moved back"); else coachEvent("move",id,val);''')
rep('''    if(nextMain) autoFillMain(d,nextMain);
    queueSave(); renderMyTimes(d);''','''    if(nextMain) autoFillMain(d,nextMain);
    queueSave(); renderMyTimes(d); renderCoach(d); planSoon(d);''')
rep('''<div class="blocks"><section class="block" id="myTimes"></section>${body}</div>`;''','''<div class="blocks"><section class="block coach" id="coach"></section><section class="block" id="myTimes"></section>${body}</div>`;''')
rep('''  renderMyTimes(d);
  $("#prevD")''','''  renderMyTimes(d); SHEET_D=d; renderCoach(d);
  $("#prevD")''')
rep('''checkNudge(); },30000);''','''checkNudge(); refreshCoach(); },30000);''')
rep('''  v.innerHTML=`<div class="stats">''','''  v.innerHTML=`<div class="stats"><section class="card" id="coachReport">${coachReport()}</section>''')
rep('''  bindScoreInputs(v,()=>{ $("#stChart").innerHTML=testsChart(); $("#stLoss").innerHTML=lossBars(); });''','''  bindScoreInputs(v,()=>{ $("#stChart").innerHTML=testsChart(); $("#stLoss").innerHTML=lossBars(); });
  bindAI($("#coachReport"));''')

# ================= the coach =================
COACH = r'''
// ======================= COACH =======================
// A rule engine that reads everything the tracker knows (plan, ticks, timers, pauses,
// accuracy, scores, moves) and turns it into assessments and next steps after every tap.
const PACE0={main:MIN_PER_Q,ss:1.4,qrp:1.2,mar:2,pyq:1};
const LIGHTS_OUT=23*60;
let SHEET_D=null, CO_ACTS=[], SAMPLE=null;
const DKF=new Intl.DateTimeFormat("en-CA",{timeZone:"Asia/Kolkata",year:"numeric",month:"2-digit",day:"2-digit"});
const nowISO=()=>new Date().toISOString();
const toMin=h=>+h.slice(0,2)*60+ +h.slice(3);
const nowMin=()=>toMin(hm(nowISO()));
const plural=(n,w)=>n+" "+w+(n===1?"":"s");
function clock(m){ m=Math.round(m); const x=((m%1440)+1440)%1440, dd=Math.floor(m/1440); return String(Math.floor(x/60)).padStart(2,"0")+":"+String(x%60).padStart(2,"0")+(dd>0?" (after midnight)":""); }
function dateAdd(d,n){ const x=new Date(d+"T00:00:00Z"); x.setUTCDate(x.getUTCDate()+n); return x.toISOString().slice(0,10); }
const slotOf=m=>m<300?"night":m<720?"morning":m<1020?"afternoon":"evening";
function sessions(){ const o=[]; for(const id in actual){ const a=actual[id], r=ITEMBY[id]; if(a&&a.s&&a.e&&r&&r.i.q){ const m=activeM(a); if(m>=3) o.push({id,i:r.i,m,q:r.i.q,mpq:m/r.i.q,slot:slotOf(toMin(hm(a.s)))}); } } return o; }
function pace(k){ const ss=sessions().filter(x=>x.i.k===k), q=ss.reduce((a,x)=>a+x.q,0); return q<25?{v:PACE0[k]||1.5,own:false}:{v:ss.reduce((a,x)=>a+x.m,0)/q,own:true}; }
const planRate=k=>PACE0[k]||1.5;
function needM(i){ return i.q ? i.q*pace(i.k).v : (i.k==="task"?30:0); }
function remainingM(i){ const a=actual[i.id], n=needM(i); return a&&a.s&&!a.e ? Math.max(5,n-activeM(a)) : n; }
function onDate(date,f){ let m=0; for(const id in actual){ const a=actual[id]; if(a&&a.s&&DKF.format(new Date(a.s))===date) m+=f(a); } return m; }
function dayStatus(d){
  const its=itemsOf(d), undone=its.filter(i=>!isDone(i.id)), isToday=d.date===TODAY;
  const remM=undone.reduce((a,i)=>a+remainingM(i),0);
  return {its,undone,isToday,remM,qTot:its.reduce((a,i)=>a+i.q,0),qDone:its.reduce((a,i)=>a+(isDone(i.id)?i.q:0),0),qRem:undone.reduce((a,i)=>a+i.q,0),
    finish:isToday?nowMin()+remM:null,studied:onDate(d.date,a=>activeM(a)),paused:onDate(d.date,a=>pausedM(a,a.e||nowISO()))};
}
function runningItem(){ let pz=null; for(const id in actual){ const a=actual[id]; if(a&&a.s&&!a.e&&ITEMBY[id]){ const o={id,a,i:ITEMBY[id].i,paused:isPaused(a)}; if(!o.paused) return o; pz=pz||o; } } return pz; }
function nextUp(st){ const c=st.undone.filter(i=>!(actual[i.id]&&actual[i.id].s)); const w=c.filter(i=>tget(i.id).s).sort((a,b)=>tget(a.id).s.localeCompare(tget(b.id).s)); return w[0]||c[0]||null; }
function sysAcc(sys){ let r=0,q=0; for(const id in ext.acc){ const x=ITEMBY[id]; if(x&&x.i.q&&x.i.sys===sys){ r+=Math.min(+ext.acc[id],x.i.q); q+=x.i.q; } } return q?{p:Math.round(100*r/q),q}:null; }
function allSysAcc(){ const g={}; for(const id in ext.acc){ const x=ITEMBY[id]; if(!x||!x.i.q) continue; const k=x.i.sys||"misc"; g[k]=g[k]||{r:0,q:0}; g[k].r+=Math.min(+ext.acc[id],x.i.q); g[k].q+=x.i.q; } return Object.entries(g).filter(([,x])=>x.q>=20).map(([k,x])=>({k,p:Math.round(100*x.r/x.q),q:x.q})).sort((a,b)=>a.p-b.p); }
function bestSlot(){ const g={}; sessions().forEach(s=>{ g[s.slot]=g[s.slot]||{m:0,q:0}; g[s.slot].m+=s.m; g[s.slot].q+=s.q; }); const e=Object.entries(g).filter(([,x])=>x.q>=20).map(([k,x])=>({k,v:x.m/x.q})).sort((a,b)=>a.v-b.v); return e.length>=2?{best:e[0],worst:e[e.length-1]}:null; }
function revDayFor(sys){ return DATA.phase2.find(x=>x.sys===sys && x.date>=TODAY && x.items.some(i=>i.id.startsWith("eb:")))||null; }
const dropRank=i=>i.k==="pyq"?99:i.k==="main"?(i.tier==="L"?1:i.tier==="M"?8:20):i.tier==="L"?2:i.k==="task"?6:(i.k==="mar"?(i.tier==="H"?6:3):i.k==="ss"?(i.tier==="H"?7:4):5);
function mainProjection(){
  const doneQ=BASELINE_MAIN+sumQ(allP1,i=>i.k==="main");
  const planned=BASELINE_MAIN+DATA.phase1.filter(d=>d.date<TODAY).reduce((a,d)=>a+d.items.filter(i=>i.k==="main").reduce((s,i)=>s+i.q,0),0);
  const since=dateAdd(TODAY,-6); let q7=0; const days=new Set();
  for(const id in ext.dt){ const r=ITEMBY[id]; if(r&&r.i.k==="main"&&ext.dt[id]>=since&&ext.dt[id]<=TODAY){ q7+=r.i.q; days.add(ext.dt[id]); } }
  const rate=days.size?q7/days.size:null, left=5172-doneQ, need=rate?Math.ceil(left/rate):null;
  return {doneQ,planned,diff:doneQ-planned,rate,left,finish:rate?dateAdd(TODAY,Math.max(0,need-1)):null};
}
function act2(o){ CO_ACTS.push(o); return `<button class="btn co-act" data-k="${CO_ACTS.length-1}">${esc(o.label)}</button>`; }

function coachSuggest(d){
  const st=dayStatus(d), out=[], push=(u,html,a)=>out.push({u,html,a});
  const k=ALLDAYS.indexOf(d), later=ALLDAYS.slice(k+1), tom=later[0], lb=later.find(x=>x.light||x.buffer)||tom;
  const todayD=ALLDAYS.find(x=>x.date===TODAY);
  if(st.isToday){
    const nm=nowMin(), run=runningItem();
    if(!st.undone.length) push(2,`Today's plan is complete. Add accuracy for anything ticked without it, then sleep by 23:00.`);
    if(st.undone.length && nm>=LIGHTS_OUT-30){
      const idle=st.undone.filter(i=>!(actual[i.id]&&actual[i.id].s));
      push(4, nm>=LIGHTS_OUT ? `It's past 23:00. Sleep now: the night's sleep is when today's reading turns into memory. Carry what's left forward.` : `Lights out is at 23:00. Finish with QRP recall only and carry the rest forward.`, idle.length&&tom?{t:"moveMany",ids:idle.map(i=>i.id),to:tom.key,label:`Carry ${idle.length} to ${dayLabel(tom)}`}:null);
    } else if(st.undone.length && st.finish>LIGHTS_OUT){
      const over=st.finish-LIGHTS_OUT, cand=st.undone.filter(i=>!(actual[i.id]&&actual[i.id].s)&&dropRank(i)<10).sort((a,b)=>dropRank(a)-dropRank(b));
      let saved=0; const pick=[]; for(const i of cand){ if(saved>=over) break; pick.push(i); saved+=remainingM(i); }
      push(4,`At your pace the remaining ${fmt(st.qRem)} Qs need ${fmtM(st.remM)}, so you'd finish about <b>${clock(st.finish)}</b>, ${fmtM(over)} past lights out.${pick.length&&lb?` Moving ${pick.length===1?"<b>"+esc(pick[0].t)+"</b>":plural(pick.length,"lower-yield item")} to ${dayLabel(lb)} saves ${fmtM(saved)}.`:""}`, pick.length&&lb?{t:"moveMany",ids:pick.map(i=>i.id),to:lb.key,label:`Move ${pick.length} to ${dayLabel(lb)}`}:null);
    } else if(st.undone.length) push(1,`At your pace you'll finish today's plan about <b>${clock(st.finish)}</b>, ${fmtM(LIGHTS_OUT-st.finish)} before lights out.`);
    if(run){
      const pm=planM(tget(run.id)), am=activeM(run.a);
      if(run.paused){ const p=pauses(run.a), pz=mins(p[p.length-1].f,nowISO()); push(pz>=20?3:2,`<b>${esc(run.i.t)}</b> has been paused for ${fmtM(pz)}.${pz>=20?" Resume, or end it and carry what's left.":""}`,{t:"r",id:run.id,label:"▶ Resume"}); }
      else if(pm && am>pm) push(3,`<b>${esc(run.i.t)}</b> is ${fmtM(am-pm)} past its planned length; everything after it slips by the same amount.`);
      else if(run.i.q) push(2,`On <b>${esc(run.i.t)}</b>: ${fmtM(am)} studied, about ${fmtM(Math.max(0,needM(run.i)-am))} left at your pace.`);
      const segS=(()=>{ const p=pauses(run.a); return p.length?p[p.length-1].t:run.a.s; })();
      if(!run.paused && segS && mins(segS,nowISO())>=75) push(3,`${fmtM(mins(segS,nowISO()))} without a break. Pause for 10 minutes: water, stand, look out of a window.`,{t:"p",id:run.id,label:"⏸ Pause"});
      const undH=st.undone.filter(i=>i.k==="main"&&i.tier==="H"&&i.id!==run.id);
      if(run.i.tier==="L" && undH.length && nm<780) push(3,`You're on a light-pass module while ${plural(undH.length,"most-asked module")} ${undH.length>1?"are":"is"} still open. Morning focus is best spent on <b>${esc(undH[0].t)}</b>.`,{t:"s",id:undH[0].id,label:"Switch"});
    } else if(st.undone.length && nm<LIGHTS_OUT){
      const nx=nextUp(st);
      if(nx) push(3,`Next up: <b>${esc(nx.t)}</b>${tget(nx.id).s?` (planned ${tget(nx.id).s})`:""}${nx.q?` · ${nx.q} Qs, about ${fmtM(needM(nx))}`:""}.`,{t:"s",id:nx.id,label:"▶ Start"});
    }
    const tot=st.studied+st.paused;
    if(st.studied>=60 && st.paused/tot>0.3) push(2,`Breaks are ${Math.round(100*st.paused/tot)}% of today's session time (${fmtM(st.paused)} paused). Try 50 minutes on, 10 off.`);
    const noAcc=st.its.filter(i=>isDone(i.id)&&ACC_K[i.k]&&i.q&&ext.acc[i.id]==null);
    if(noAcc.length) push(2,`Add how many you got right for ${noAcc.slice(0,3).map(i=>"<b>"+esc(i.t)+"</b>").join(", ")}${noAcc.length>3?` and ${noAcc.length-3} more`:""}. It keeps the weak list honest.`);
    const pend=ALLDAYS.filter(x=>x.date<TODAY).flatMap(x=>itemsOf(x).filter(i=>!isDone(i.id)&&i.k==="main"));
    if(pend.length && lb) push(3,`${fmt(pend.reduce((a,i)=>a+i.q,0))} Main Qs are still open from earlier days. Main is never skipped, so give them a slot on ${dayLabel(lb)}.`,{t:"moveMany",ids:pend.map(i=>i.id),to:lb.key,label:`Carry to ${dayLabel(lb)}`});
    const bs=bestSlot(); if(bs) push(1,`You work fastest in the ${bs.best.k} (${bs.best.v.toFixed(1)} min/Q) and slowest in the ${bs.worst.k} (${bs.worst.v.toFixed(1)}). Put most-asked modules in your fast window.`);
  } else if(d.date<TODAY){
    if(st.undone.length && todayD) push(4,`${plural(st.undone.length,"item")} (${fmt(st.qRem)} Qs) were left on this day.`,{t:"moveMany",ids:st.undone.map(i=>i.id),to:todayD.key,label:"Carry to today"});
    else if(!st.undone.length) push(1,`Everything on this day is done.`);
  } else if(st.undone.length){
    const h=st.remM/60;
    push(h>13.5?3:1,`At your current pace this day needs about <b>${h.toFixed(1)} h</b> of work${h>13.5?", more than a full day holds. Move a light-pass item now, or plan to use the Marrow hour for catch-up.":"."}`);
  }
  const wk=weakList().filter(w=>w.i.sys===d.sys);
  if(wk.length) push(2,`Weak so far in ${SYS[d.sys]||"this system"}: ${wk.slice(0,3).map(w=>`${esc(w.i.t)} <b class="pct lo">${w.p}%</b>`).join(", ")}. Re-solve their wrong answers in the Marrow hour.`);
  if(d.key && d.key.startsWith("p2")){ const sa=sysAcc(d.sys); if(sa) push(1,`${SYS[d.sys]} accuracy across your logged modules: ${sa.p}% (${sa.q} Qs).`); }
  return out.sort((a,b)=>b.u-a.u);
}

function coachLog(){ try{ return JSON.parse(localStorage.getItem("neetss-coachlog")||"[]")||[]; }catch(e){ return []; } }
let CO_MEM=[];
function addLog(e){ let l=coachLog(); if(!l.length&&CO_MEM.length) l=CO_MEM; l.push(e); l=l.slice(-60); CO_MEM=l; try{ localStorage.setItem("neetss-coachlog",JSON.stringify(l)); }catch(x){} }
function lastLog(){ const l=coachLog(); return (l.length?l:CO_MEM); }

function renderCoach(d){
  const el=$("#coach"); if(!el||!d) return;
  CO_ACTS=[];
  const st=dayStatus(d), sug=coachSuggest(d).slice(0,5), P=pace("main"), mp=mainProjection();
  const fin=st.isToday&&st.undone.length?st.finish:null;
  const stats=[
    ["Done",`${fmt(st.qDone)}/${fmt(st.qTot)} Qs`,st.qTot&&st.qDone===st.qTot?"good":""],
    st.isToday||d.date<TODAY?["Studied",fmtM(st.studied),""]:["Needs",`${(st.remM/60).toFixed(1)} h`,st.remM/60>13.5?"warn":""],
    ["Main pace",`${P.v.toFixed(1)} min/Q`,P.own?(P.v>MIN_PER_Q+0.3?"warn":(P.v<=MIN_PER_Q?"good":"")):""],
    fin!=null?["Finish ≈",clock(fin),fin>LIGHTS_OUT?"bad":"good"]:["Main vs plan",(mp.diff>=0?"+":"")+fmt(mp.diff)+" Qs",mp.diff<-100?"bad":(mp.diff<0?"warn":"good")]
  ];
  const logs=lastLog().filter(x=>x.d===d.date), last=logs[logs.length-1];
  el.innerHTML=`<div class="block-h"><h3>Coach</h3><span class="when">updates with every tap${P.own?"":" · uses plan rates until you've timed a few modules"}</span></div>
    <div class="co-stats">${stats.map(s=>`<div class="co-stat ${s[2]}"><span>${s[0]}</span><b>${s[1]}</b></div>`).join("")}</div>
    ${last?`<div class="co-last"><span class="co-when">${hm(last.t)} · latest</span><b>${esc(last.title)}</b>${last.lines.map(x=>`<span>${x}</span>`).join("")}</div>`:""}
    ${sug.length?`<ul class="co-list">${sug.map(s=>`<li class="u${s.u}"><span class="tx">${s.html}</span>${s.a?act2(s.a):""}</li>`).join("")}</ul>`:""}
    ${aiBlock()}
    ${logs.length>1?`<details class="co-notes"><summary>${plural(logs.length,"coach note")} on this day</summary><div>${logs.slice().reverse().map(x=>`<span><b>${hm(x.t)}</b>${esc(x.title)}</span>`).join("")}</div></details>`:""}`;
  el.querySelectorAll(".co-act").forEach(b=>b.onclick=()=>runAct(CO_ACTS[+b.dataset.k]));
  bindAI(el);
}
function refreshCoach(){ if((tab==="p1"||tab==="p2") && SHEET_D) renderCoach(SHEET_D); }
function runAct(o){
  if(!o) return;
  if(o.t==="moveMany"){ o.ids.forEach(id=>{ if(ITEMBY[id] && ITEMBY[id].day.key===o.to) delete ext.moved[id]; else ext.moved[id]=o.to; }); queueSave(); renderAll(); coachEvent("moveMany",o.ids[0],o); }
  else act(o.id,o.t);
}

function coachEvent(type,id,extra){
  if(!type) return;
  const r=ITEMBY[id], i=r?r.i:null; if(!i && type!=="plan") return;
  const L=[]; let title="";
  const d=i?(curDay(id)||r.day):extra, st=d?dayStatus(d):null;
  const dayLine=()=>{ if(st&&st.isToday&&st.undone.length){ const f=st.finish; L.push(f>LIGHTS_OUT?`Day outlook: about ${clock(f)} finish, ${fmtM(f-LIGHTS_OUT)} past lights out. The Coach panel suggests what to move.`:`Day outlook: about ${clock(f)} finish, ${fmtM(LIGHTS_OUT-f)} before lights out.`); } else if(st&&st.isToday&&!st.undone.length) L.push(`That's everything planned for today. Sleep by 23:00.`); };
  if(type==="s"){
    title=`Started ${i.t}`;
    const pv=tget(id); if(pv.s){ const df=nowMin()-toMin(pv.s); L.push(Math.abs(df)<5?`Right on your planned time.`:df>0?`${fmtM(df)} later than planned (${pv.s}).`:`${fmtM(-df)} ahead of your plan.`); }
    const P=pace(i.k); if(i.q) L.push(`${i.q} Qs at ${P.v.toFixed(1)} min/Q (${P.own?"your average":"plan rate"}) is about ${fmtM(needM(i))}: done near ${clock(nowMin()+needM(i))}.`);
    if(i.tier==="H") L.push(`Most asked in PYQs${i.hint?` (${esc(i.hint)})`:""}. Read every explanation and highlight tested lines yellow.`);
    else if(i.tier==="L") L.push(`Light pass: aim under 2 min/Q and highlight answers only.`);
    const sa=sysAcc(i.sys); if(sa&&sa.p<65) L.push(`Your ${SYS[i.sys]} accuracy is ${sa.p}% so far. Slow down on two-step reasoning questions.`);
    const bs=bestSlot(); if(bs && slotOf(nowMin())===bs.worst.k && i.tier==="H") L.push(`The ${bs.worst.k} is usually your slowest time. Phone in another room.`);
    if(nowMin()>=LIGHTS_OUT-45) L.push(`It's late. After this, wind down for 23:00 lights out.`);
  } else if(type==="p"){
    const a=actual[id], p=pauses(a), n=p.length, prevT=n>1?p[n-2].t:a.s, seg=mins(prevT,p[n-1].f);
    title=`Paused ${i.t}`;
    L.push(`${fmtM(activeM(a))} studied so far${n>1?`; pause ${n} on this module`:""}.`);
    L.push(seg>=50?`You'd gone ${fmtM(seg)} without a break, so take a proper one: about 10 minutes, water, away from screens.`:`Short stretch (${fmtM(seg)}). Keep this pause under 5 minutes to stay in flow.`);
    if(n>=4) L.push(`${n} pauses on one module usually means distraction. Put the phone in another room for the rest of it.`);
  } else if(type==="r"){
    const a=actual[id], p=pauses(a), last=p[p.length-1], pm=last&&last.t?mins(last.f,last.t):0;
    title=`Resumed ${i.t}`;
    L.push(`Break: ${fmtM(pm)}. Paused on this module in total: ${fmtM(pausedM(a,nowISO()))}.`);
    if(pm>=30) L.push(`Long break. Skim the last page you highlighted before the next question.`);
    if(i.q) L.push(`About ${fmtM(Math.max(0,needM(i)-activeM(a)))} left at your pace.`);
  } else if(type==="e"){
    const a=actual[id], m=activeM(a); title=`Finished ${i.t}`;
    if(i.q){ const mpq=m/i.q, pr=planRate(i.k);
      L.push(`${fmtM(m)} studied for ${i.q} Qs: <b>${mpq.toFixed(1)} min/Q</b> against a plan of ${pr.toFixed(1)}.`);
      if(i.k==="main"&&mpq<1.3) L.push(`Very fast for Main. Make sure explanations are being read, not skipped.`);
      else if(mpq>pr*1.4) L.push(`Slower than planned. If that's from reading explanations it's time well spent; if not, set a 25-minute timer per 8 Qs.`); }
    const v=vsPlan(id); if(v) L.push(`Against your planned time: ${v.replace(/<[^>]+>/g,"")}.`);
    const n=pauses(a).length; if(n) L.push(`${plural(n,"pause")}, ${fmtM(pausedM(a,a.e))} in total.`);
    if(!isDone(id)) L.push(`Tick it when it's complete, then type how many you got right.`);
    dayLine();
    if(st){ const nx=nextUp(st); if(nx&&st.isToday) L.push(`Next: <b>${esc(nx.t)}</b>${nx.q?` (${nx.q} Qs, about ${fmtM(needM(nx))})`:""}.`); }
  } else if(type==="tick"){
    title=`${i.t} done`;
    if(ACC_K[i.k]&&i.q) L.push(`Type how many you got right in the box under it. Below 60% joins the weak list for its revision day.`);
    if(i.k==="main"){ const mp=mainProjection(); L.push(`Main: ${fmt(mp.doneQ)} / 5,172 done, ${mp.diff>=0?`${fmt(mp.diff)} Qs ahead of`:`${fmt(-mp.diff)} Qs behind`} the plan up to yesterday.`); }
    if(st && !st.undone.length) L.push(`<b>Day complete.</b> Nice work.`); else dayLine();
  } else if(type==="acc"){
    const p=accPct(i); if(p==null) return; title=`${i.t}: ${p}% right`;
    const ses=sessions().find(x=>x.id===id), fast=ses&&ses.mpq<(i.k==="main"?2:planRate(i.k)*0.7), slow=ses&&ses.mpq>planRate(i.k)*1.25;
    if(p<60){ const rd=revDayFor(i.sys);
      L.push(`Added to your weak list${rd?`; it will show in the morning of ${dayLabel(rd)} (${rd.title})`:""}.`);
      L.push(fast?`You were fast (${ses.mpq.toFixed(1)} min/Q) but inaccurate: slow down and read every option.`:slow?`Slow and inaccurate points to a concept gap. Re-read this Harrison section before its QRP recall.`:`Re-solve the wrong ones tonight and write one line on each trap.`);
      if(i.hint) L.push(`PYQ themes in this module: ${esc(i.hint)}.`); }
    else if(p<75) L.push(fast?`Fair, and quick. A little more time per question should lift this.`:`Fair. Read the explanations of the wrong ones before the QRP recall.`);
    else L.push(p>=85?`Strong. A quick flip of the highlights is enough at revision.`:`Good. Keep this pace.`);
    const sa=sysAcc(i.sys); if(sa) L.push(`${SYS[i.sys]} overall: ${sa.p}% across ${sa.q} Qs.`);
  } else if(type==="score"){
    const s=sc(id), m=marks(s), T=TESTSET[id]; if(m==null||!T) return; title=`${T.t}: ${m}/600`;
    const att=(+s.r||0)+(+s.w||0), acc=att?100*(+s.r||0)/att:0, skip=150-att;
    L.push(`${s.r||0} right, ${s.w||0} wrong, ${skip} skipped: ${Math.round(acc)}% accuracy on attempted questions.`);
    const k=TESTS.findIndex(x=>x.id===id), prev=TESTS.slice(0,k).reverse().find(x=>marks(sc(x.id))!=null);
    if(prev){ const df=m-marks(sc(prev.id)); L.push(`${df>=0?"Up":"Down"} ${Math.abs(df)} marks from ${prev.t}.`); }
    if(acc>=70&&skip>=15) L.push(`With accuracy this high, skipping ${skip} costs marks. A guess gains on average whenever your odds beat 1 in 5, so attempt anything you can narrow to two options.`);
    else if(att&&acc<55) L.push(`Each wrong answer costs a mark. At this accuracy, skip questions where you can't rule out at least two options.`);
    const sub=s.subj||{}, top=Object.entries(sub).sort((a,b)=>b[1]-a[1]).filter(x=>x[1]>0).slice(0,2);
    if(top.length) L.push(`Most marks lost in ${top.map(([x,n])=>`${AUDIT[+x]} (${n} wrong)`).join(" and ")}: weight those revision days.`);
    else L.push(`After your audit, fill in "Wrong answers by subject" in Stats so I can point to the systems costing you marks.`);
  } else if(type==="move"||type==="moveMany"){
    const to=type==="move"?DAYBY[extra]:DAYBY[extra.to]; if(!to) return; const ts=dayStatus(to);
    title=type==="move"?`Moved ${i.t}`:`Moved ${plural(extra.ids.length,"item")}`;
    L.push(`${dayLabel(to)} (${to.title}) now holds ${fmt(ts.qTot)} Qs, about ${(ts.remM/60).toFixed(1)} h at your pace.`);
    if(ts.remM/60>13.5) L.push(`That's more than a full day. A light or buffer day would absorb it better.`);
    if(i&&i.k==="main"&&i.tier==="H") L.push(`This is a most-asked module. Keep it in a morning block on the new day.`);
  } else if(type==="plan"){
    const its=itemsOf(d).filter(x=>tget(x.id).e); if(!its.length) return;
    const lastE=its.map(x=>tget(x.id)).reduce((a,v)=>{ const m=toMin(v.e)+(v.s&&toMin(v.e)<toMin(v.s)?1440:0); return Math.max(a,m); },0);
    if(lastE<=LIGHTS_OUT) return;
    title=`Plan check: ${dayLabel(d)}`; L.push(`Your planned times run to ${clock(lastE)}, ${fmtM(lastE-LIGHTS_OUT)} past 23:00 lights out. Shorten a block or move a light-pass item.`);
  } else return;
  addLog({t:nowISO(),d:(d&&d.date)||TODAY,title,lines:L});
  showPop(title,L); refreshCoach();
}
let popTimer=null;
function showPop(title,lines){ $("#cpT").textContent=title; $("#cpB").innerHTML=lines.map(x=>`<li>${x}</li>`).join(""); $("#coachPop").hidden=false; $("#toast").classList.remove("on"); clearTimeout(popTimer); popTimer=setTimeout(()=>{ $("#coachPop").hidden=true; },14000); }
let scoreT={}; function scoreSoon(id){ clearTimeout(scoreT[id]); scoreT[id]=setTimeout(()=>coachEvent("score",id),900); }
let planT=null; function planSoon(d){ clearTimeout(planT); planT=setTimeout(()=>coachEvent("plan",null,d),1500); }

function coachReport(){
  const mp=mainProjection(), sa=allSysAcc(), L=[];
  const left=dayDiff(TODAY,EXAM);
  L.push(`<b>${left>0?left+" days":"Exam day"}</b> to NEET SS. Main: ${fmt(mp.doneQ)} / 5,172 done, ${mp.diff>=0?`<b>${fmt(mp.diff)} Qs ahead</b> of`:`<b>${fmt(-mp.diff)} Qs behind</b>`} the plan up to yesterday.`);
  if(mp.rate) L.push(`Your last 7 days average ${Math.round(mp.rate)} Main Qs per study day. At that rate Main finishes on <b>${nice(mp.finish)}</b> (plan: Thu 26 Nov)${mp.finish>"2026-11-26"?` — about ${Math.ceil(mp.left/mp.rate)-dayDiff(TODAY,"2026-11-26")-1} days late. Lean on light days and the Nov 10 buffer.`:"."}`);
  else L.push(`Tick modules as you finish them; from tomorrow I'll project when Main will be finished at your real pace.`);
  if(sa.length){ L.push(`Weakest systems by your logged accuracy: ${sa.slice(0,3).map(x=>`${SYS[x.k]||x.k} ${x.p}%`).join(", ")}. Strongest: ${SYS[sa[sa.length-1].k]||sa[sa.length-1].k} ${sa[sa.length-1].p}%.`); }
  else L.push(`Type "Right __ / Qs" after ticking modules and I'll rank your systems by accuracy.`);
  const sc2=TESTS.map(x=>({x,m:marks(sc(x.id))})).filter(o=>o.m!=null);
  if(sc2.length>=2){ const a=sc2[0], b=sc2[sc2.length-1]; L.push(`Test trend: ${a.x.t} ${a.m} → ${b.x.t} ${b.m} (${b.m-a.m>=0?"+":""}${b.m-a.m}).`); }
  else if(sc2.length===1) L.push(`First test logged: ${sc2[0].x.t} ${sc2[0].m}/600. The trend appears after the next one.`);
  const days=[...Array(7)].map((_,k)=>dateAdd(TODAY,-k)), hrs=days.map(dt=>onDate(dt,a=>activeM(a))), act=hrs.filter(h=>h>0);
  if(act.length) L.push(`Studied time logged on ${plural(act.length,"day")} this week, averaging ${fmtM(Math.round(act.reduce((a,b)=>a+b,0)/act.length))} a day.`);
  const bs=bestSlot(); if(bs) L.push(`Fastest time of day: ${bs.best.k} (${bs.best.v.toFixed(1)} min/Q). Slowest: ${bs.worst.k} (${bs.worst.v.toFixed(1)}).`);
  const hy=(DATA.hy||[]).flatMap(s=>s.topics), hyd=hy.filter(x=>isDone(x.id)).length;
  L.push(`PYQ topics revised: ${hyd} / ${hy.length}.`);
  const mar=ALLDAYS.filter(x=>x.date<=TODAY).flatMap(x=>itemsOf(x).filter(i=>i.k==="mar")), mq=mar.reduce((a,i)=>a+i.q,0), md=mar.reduce((a,i)=>a+(isDone(i.id)?i.q:0),0);
  if(mq) L.push(`Marrow: ${md} of the ${mq} Qs scheduled up to today are done.`);
  return `<h2>Coach report</h2><ul class="rep">${L.map(x=>`<li>${x}</li>`).join("")}</ul>${aiBlock()}`;
}

// ---- optional deeper review written by Claude (only inside the Claude app) ----
function aiBlock(){ return SAMPLE?`<div class="co-ai"><div><button class="btn co-ai-btn">Ask Claude for a deeper review</button></div><div class="co-ai-out" hidden></div></div>`:""; }
function aiSummary(){
  const td=ALLDAYS.find(x=>x.date===TODAY)||SHEET_D, st=td?dayStatus(td):null, mp=mainProjection();
  const lines=[`Today ${TODAY}; NEET SS (Medical group) on ${EXAM}, ${dayDiff(TODAY,EXAM)} days away. Lights out 23:00. Plan rate Main ${MIN_PER_Q} min/Q.`,
    `Main ${mp.doneQ}/5172 done; ${mp.diff} vs plan to yesterday; 7-day rate ${mp.rate?Math.round(mp.rate):"n/a"} Qs/day.`];
  ["main","ss","qrp","mar"].forEach(k=>{ const P=pace(k); lines.push(`Pace ${k}: ${P.v.toFixed(2)} min/Q ${P.own?"(measured)":"(plan default)"}`); });
  if(td&&st){ lines.push(`Today's plan "${td.title}": ${st.qDone}/${st.qTot} Qs done, studied ${st.studied} min, paused ${st.paused} min, remaining est ${Math.round(st.remM)} min.`);
    st.its.forEach(i=>{ const a=actual[i.id], v=tget(i.id); lines.push(`- [${isDone(i.id)?"x":" "}] ${i.k}${i.tier?"/"+i.tier:""} ${i.t} (${i.q} Qs)${v.s?` plan ${v.s}-${v.e||"?"}`:""}${a&&a.s?` actual ${hm(a.s)}-${a.e?hm(a.e):"running"} studied ${activeM(a)}m, ${pauses(a).length} pauses`:""}${ext.acc[i.id]!=null?` right ${ext.acc[i.id]}/${i.q}`:""}`); }); }
  const w=weakList().slice(0,12); if(w.length) lines.push("Weak modules (<60%): "+w.map(x=>`${x.i.t} ${x.p}%`).join("; "));
  const sa=allSysAcc(); if(sa.length) lines.push("System accuracy: "+sa.map(x=>`${SYS[x.k]||x.k} ${x.p}% (${x.q}Q)`).join("; "));
  TESTS.forEach(x=>{ const s=sc(x.id), m=marks(s); if(m!=null) lines.push(`${x.t}: ${m}/600 (R${s.r||0} W${s.w||0})${s.subj?" wrong by subject "+Object.entries(s.subj).map(([k,n])=>AUDIT[+k]+" "+n).join(", "):""}`); });
  const pend=ALLDAYS.filter(x=>x.date<TODAY).flatMap(x=>itemsOf(x).filter(i=>!isDone(i.id))); if(pend.length) lines.push(`Backlog from earlier days: ${pend.length} items, ${pend.reduce((a,i)=>a+i.q,0)} Qs.`);
  return lines.join("\n");
}
function bindAI(root){
  if(!root||!SAMPLE) return;
  const btn=root.querySelector(".co-ai-btn"), out=root.querySelector(".co-ai-out"); if(!btn) return;
  btn.onclick=async()=>{
    btn.disabled=true; out.hidden=false; out.textContent="Thinking…";
    const prompt=`You are a concise, practical study coach for a doctor preparing for NEET-SS (Medical group, India). Using ONLY the data below from their study tracker, give an honest assessment in 2 sentences, then 5 numbered, specific actions for the rest of today and this week (each under 30 words). Mention module names and times where useful. No preamble, no markdown headings.\n\nDATA\n${aiSummary()}`;
    try{ await SAMPLE(prompt,{onText:({text})=>{ out.textContent=text; }}); }
    catch(e){ if(e&&e.code==="not_granted"){ out.textContent="Claude wasn't allowed for this page, so only the built-in coach is available."; } else out.textContent=(e&&e.text)||"Couldn't reach Claude just now. The built-in coach above still works; try again in a minute."; }
    finally{ btn.disabled=false; }
  };
}
(async()=>{ try{ SAMPLE = window.claude && window.claude.use ? await window.claude.use("sample") : null; }catch(e){ SAMPLE=null; } if(SAMPLE){ refreshCoach(); if(tab==="stats") renderStats(); } })();
'''
rep('''function toast(msg){''', COACH+'''
function toast(msg){''')
rep('''$("#nudgeOk").onclick=()=>{ $("#nudge").hidden=true; };''','''$("#nudgeOk").onclick=()=>{ $("#nudge").hidden=true; };
$("#cpX").onclick=()=>{ $("#coachPop").hidden=true; };''')
open(p,'w').write(t); print('template ok')

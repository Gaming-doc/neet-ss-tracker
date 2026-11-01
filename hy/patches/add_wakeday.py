p='tracker.tpl.html'; t=open(p).read()
def rep(a,b,n=1):
    global t
    assert t.count(a)==n,(a[:90],t.count(a)); t=t.replace(a,b)

# ---- the study day starts when you wake up, not at midnight ----
rep('''function todayIST(){
  try{ return new Intl.DateTimeFormat("en-CA",{timeZone:"Asia/Kolkata",year:"numeric",month:"2-digit",day:"2-digit"}).format(new Date()); }
  catch(e){ return new Date().toISOString().slice(0,10); }
}
const TODAY = todayIST();''','''// The study day starts when you wake up, not at midnight. Until you log waking up,
// anything before DAY_CUT (06:00) still belongs to the day before.
const DAY_CUT=360;
let _dk=null;
function calIST(d){ try{ _dk=_dk||new Intl.DateTimeFormat("en-CA",{timeZone:"Asia/Kolkata",year:"numeric",month:"2-digit",day:"2-digit"}); return _dk.format(d); }catch(e){ return new Date(d.getTime()+19800000).toISOString().slice(0,10); } }
function calMin(d){ const x=new Date(d.getTime()+19800000); return x.getUTCHours()*60+x.getUTCMinutes(); }
function prevDate(s){ const d=new Date(s+"T00:00:00Z"); d.setUTCDate(d.getUTCDate()-1); return d.toISOString().slice(0,10); }
function wakeMinOf(date){ try{ const s=ext&&ext.sleep&&ext.sleep[date]; if(s&&s.w) return +s.w.slice(0,2)*60+ +s.w.slice(3); }catch(e){} return null; }
function dayOf(iso){ const d=new Date(iso), c=calIST(d), m=calMin(d), w=wakeMinOf(c); return m < (w!=null?Math.min(w,720):DAY_CUT) ? prevDate(c) : c; }
function todayIST(){
  const now=new Date(), c=calIST(now), m=calMin(now), w=wakeMinOf(c);
  if(w!=null) return m>=Math.min(w,720)?c:prevDate(c);
  if(m<DAY_CUT) return prevDate(c);
  // still up from last night (no sleep logged): stay on yesterday until noon while you keep studying
  try{ if(m<720 && !ext.bed){ const P=prevDate(c), lim=now.getTime()-60*60000;
    for(const k in actual){ const a=actual[k]; if(!a||!a.s||dayOf(a.s)!==P) continue;
      const last=a.e?Date.parse(a.e):now.getTime(); if(last>=lim) return P; } } }catch(e){}
  return c;
}
let TODAY = todayIST();''')

# timestamps -> study day
rep('''const dKey=iso=>DKF.format(new Date(iso));''','''const dKey=iso=>dayOf(iso);''')
rep('''function onDate(date,f){ let m=0; for(const id in actual){ const a=actual[id]; if(a&&a.s&&DKF.format(new Date(a.s))===date) m+=f(a); } return m; }''',
'''function onDate(date,f){ let m=0; for(const id in actual){ const a=actual[id]; if(a&&a.s&&dayOf(a.s)===date) m+=f(a); } return m; }''')
rep('''if(a&&a.s&&DKF.format(new Date(a.s))===d.date) m+=pauseSplit(a,k).brk;''','''if(a&&a.s&&dayOf(a.s)===d.date) m+=pauseSplit(a,k).brk;''')
rep('''  if(ext.bed){ const k=dKey(ext.bed); if(k===date||(k===n&&minOf(ext.bed,n)<720)) return minOf(ext.bed,date); }''',
'''  if(ext.bed && dayOf(ext.bed)===date) return minOf(ext.bed,date);''')

# minutes "now" counted from the study day's midnight (so 01:30 after a late night is 25:30)
rep('''const nowMin=()=>toMin(hm(nowISO()));''','''const nowMin=()=>minOf(nowISO(),TODAY);''')
rep('''const slotOf=m=>m<300?"night":''','''const slotOf=m=>(m=((m%1440)+1440)%1440)<300?"night":''')
rep('''const pv=tget(id); if(pv.s){ const df=nowMin()-toMin(pv.s);''','''const pv=tget(id); if(pv.s){ let df=nowMin()-toMin(pv.s); if(df>720) df-=1440;''')

# timeline axis past midnight
rep('''${[0,6,12,18,24].map(x=>`<span style="left:${pc(x*60)}%">${String(x).padStart(2,"0")}</span>`).join("")}''',
'''${[0,6,12,18,24,30,36].filter(x=>x*60<=span).map(x=>`<span style="left:${pc(x*60)}%">${String(x%24).padStart(2,"0")}</span>`).join("")}''')

# wake button available while "sleeping since"; wake is logged on the calendar date you wake on
rep('''  if(isT && ext.bed && !s.w) btn=`<span>Went to sleep at <b>${hm(ext.bed)}</b></span>`+btn;''',
'''  if(isT && ext.bed && !s.w) btn=`<span>Went to sleep at <b>${hm(ext.bed)}</b></span>`+btn;
  else if(isT && ext.bed) btn=`<span>Sleeping since <b>${hm(ext.bed)}</b></span><button class="ab start sl-act" data-a="wake">I'm up now</button>`;''')
rep('''  const now=nowISO(), today=todayIST(), s=Object.assign({},ext.sleep[today]||{});
  s.w=hm(now);''','''  const now=nowISO(), today=calIST(new Date()), s=Object.assign({},ext.sleep[today]||{});
  s.w=hm(now);''')
rep('''  ext.sleep[today]=s; ext.bed=null; queueSave(); renderAll(); coachEvent("wake",null,today);''',
'''  ext.sleep[today]=s; ext.bed=null; queueSave(); renderAll(true); coachEvent("wake",null,today);''')

# keep TODAY current: re-check on every render and every 30 s
rep('''function renderAll(scroll){
''','''function renderAll(scroll){
  { const td=todayIST(); if(td!==TODAY){ TODAY=td; goToday(); scroll=true; } }
''')
rep('''checkNudge(); refreshCoach(); },30000);''','''checkNudge(); if(todayIST()!==TODAY) renderAll(true); else refreshCoach(); },30000);''')
rep('''if(a&&a.s&&a.e) add(DK.format(new Date(a.s)),"a",activeM(a));''','''if(a&&a.s&&a.e) add(dayOf(a.s),"a",activeM(a));''')

# explain it in the sleep row
rep('''<span class="sl-l">Night before ${isT?"today":"this day"}</span>''','''<span class="sl-l" title="Your study day starts when you tap I'm up now (or at 06:00 if you don't), so a late night still counts as the day before.">Night before ${isT?"today":"this day"}</span>''')
open(p,'w').write(t); print('ok')

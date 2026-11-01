p='tracker.tpl.html'; t=open(p).read()
def rep(a,b,n=1):
    global t
    assert t.count(a)==n,(a[:90],t.count(a)); t=t.replace(a,b)

# helpers: time inside a pause that was spent studying other modules is study, not break
rep('''function pauseLog(a){''','''// ---------- a pause spent on another module is study time, not a break ----------
function studySpans(skip,nowIso){ const now=Date.parse(nowIso||new Date().toISOString()), out=[];
  for(const k in actual){ if(k===skip) continue; const o=actual[k]; if(!o||!o.s) continue;
    const end=o.e?Date.parse(o.e):now; let cur=Date.parse(o.s);
    pauses(o).slice().sort((x,y)=>x.f.localeCompare(y.f)).forEach(q=>{ const f=Date.parse(q.f); if(f>cur) out.push([cur,f]); cur=q.t?Date.parse(q.t):end; });
    if(end>cur) out.push([cur,end]); }
  return out.sort((x,y)=>x[0]-y[0]); }
function coveredM(f,t,sp){ let s=0, cur=f; for(const [a,b] of sp){ const lo=Math.max(a,cur), hi=Math.min(b,t); if(hi>lo){ s+=hi-lo; cur=hi; } } return s/60000; }
function pauseSplit(a,id,nowIso){ nowIso=nowIso||new Date().toISOString(); const sp=studySpans(id,nowIso), end=a.e||nowIso;
  const rows=pauses(a).map(x=>{ const f=Date.parse(x.f), t=Date.parse(x.t||end), tot=Math.max(0,(t-f)/60000), oth=Math.min(tot,coveredM(f,t,sp)); return {tot,oth,brk:Math.max(0,tot-oth)}; });
  return {rows,tot:rows.reduce((s,r)=>s+r.tot,0),oth:rows.reduce((s,r)=>s+r.oth,0),brk:rows.reduce((s,r)=>s+r.brk,0)}; }
function lastStudyEnd(nowIso){ const sp=studySpans(null,nowIso); return sp.length?Math.max(...sp.map(x=>x[1])):null; }
function pauseLog(a,id){''')

rep('''  return `<details class="plog"><summary>${p.length} pause${p.length>1?"s":""} · ${fmtM(pausedM(a,now))}</summary>${p.map((x,k)=>`<span>${k+1}. ${hm(x.f)} → ${x.t?hm(x.t):"now"} · ${fmtM(mins(x.f,x.t||a.e||now))}</span>`).join("")}</details>`;''',
'''  const sp=pauseSplit(a,id,now), oth=m=>Math.round(m)>=1;
  return `<details class="plog"><summary>${p.length} pause${p.length>1?"s":""} · ${fmtM(sp.tot)}${oth(sp.oth)?` · ${fmtM(sp.brk)} break, ${fmtM(sp.oth)} on other modules`:""}</summary>${p.map((x,k)=>{ const r=sp.rows[k]; return `<span>${k+1}. ${hm(x.f)} → ${x.t?hm(x.t):"now"} · ${fmtM(r.tot)}${oth(r.oth)?` (${fmtM(r.oth)} studying other modules, ${fmtM(r.brk)} break)`:""}</span>`; }).join("")}</details>`;''')
rep('${pauseLog(a)}','${pauseLog(a,id)}',2)

# day status "paused" = real break inside pauses
rep('''paused:onDate(d.date,a=>pausedM(a,a.e||nowISO()))};''','''paused:(()=>{ let m=0; for(const k in actual){ const a=actual[k]; if(a&&a.s&&DKF.format(new Date(a.s))===d.date) m+=pauseSplit(a,k).brk; } return m; })()};''')

# coach suggestion: paused module while nothing else runs -> idle since the later of pause start / last study
rep('''if(run.paused){ const p=pauses(run.a), pz=mins(p[p.length-1].f,nowISO());''','''if(run.paused){ const p=pauses(run.a), le=lastStudyEnd(nowISO()), pf=Date.parse(p[p.length-1].f), pz=mins(new Date(Math.max(pf,le||pf)).toISOString(),nowISO());''')
rep('''has been paused for ${fmtM(pz)}.${pz>=20?''','''has been paused${le&&le>pf?`; you've been off every module`:""} for ${fmtM(pz)}.${pz>=20?''')

# resume event
rep('''    L.push(`Break: ${fmtM(pm)}. Paused on this module in total: ${fmtM(pausedM(a,nowISO()))}.`);
    if(pm>=30)''','''    const sp=pauseSplit(a,id), lr=sp.rows[sp.rows.length-1]||{tot:pm,oth:0,brk:pm}, bk=Math.round(lr.brk);
    L.push(Math.round(lr.oth)>=1?`Paused ${fmtM(lr.tot)}: ${fmtM(lr.oth)} of that was studying other modules, so only ${fmtM(bk)} counts as a break.`:`Break: ${fmtM(pm)}.`);
    if(sp.rows.length>1) L.push(`On this module so far: ${fmtM(sp.brk)} of breaks${Math.round(sp.oth)>=1?`, ${fmtM(sp.oth)} spent on other modules`:""}.`);
    if(bk>=30)''')

# end event
rep('''const n=pauses(a).length; if(n) L.push(`${plural(n,"pause")}, ${fmtM(pausedM(a,a.e))} in total.`);''',
'''const n=pauses(a).length; if(n){ const sp=pauseSplit(a,id); L.push(`${plural(n,"pause")}, ${fmtM(sp.tot)} in total${Math.round(sp.oth)>=1?`: ${fmtM(sp.brk)} break and ${fmtM(sp.oth)} studying other modules`:""}.`); }''')

# start event: say the paused one stays paused and this counts as study
rep('''    title=`Started ${i.t}`;''','''    title=`Started ${i.t}`;
    const pz=Object.keys(actual).filter(k=>k!==id&&ITEMBY[k]&&isPaused(actual[k]));
    if(pz.length) L.push(`<b>${esc(ITEMBY[pz[0]].i.t)}</b>${pz.length>1?` and ${plural(pz.length-1,"other")}`:""} stay${pz.length>1?"":"s"} paused. Time on this module counts as study, not as a break on ${pz.length>1?"those":"that one"}.`);''')

# summary label
rep('''paused ${st.paused} min,''','''break time inside pauses ${Math.round(st.paused)} min,''')
open(p,'w').write(t); print('ok')

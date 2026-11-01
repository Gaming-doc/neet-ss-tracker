p='tracker.tpl.html'; t=open(p).read()
def rep(a,b):
    global t
    assert t.count(a)==1,(a[:90],t.count(a)); t=t.replace(a,b)
rep('''function fmtM(m){ const h=Math.floor(m/60), r=m%60;''','''function fmtM(m){ m=Math.max(0,Math.round(m)); const h=Math.floor(m/60), r=m%60;''')
rep('''  const rate=days.size?q7/days.size:null, left=5172-doneQ''','''  const rate=days.size>=3?q7/days.size:null, left=5172-doneQ''')
rep('''  else L.push(`Tick modules as you finish them; from tomorrow I'll project when Main will be finished at your real pace.`);''','''  else L.push(`After 3 study days of ticks I'll project when Main will be finished at your real pace.`);''')
rep('''  if(sa.length){ L.push(`Weakest systems by your logged accuracy: ${sa.slice(0,3).map(x=>`${SYS[x.k]||x.k} ${x.p}%`).join(", ")}. Strongest: ${SYS[sa[sa.length-1].k]||sa[sa.length-1].k} ${sa[sa.length-1].p}%.`); }''',
    '''  if(sa.length>=2){ L.push(`Weakest systems by your logged accuracy: ${sa.slice(0,Math.min(3,sa.length-1)).map(x=>`${SYS[x.k]||x.k} ${x.p}%`).join(", ")}. Strongest: ${SYS[sa[sa.length-1].k]||sa[sa.length-1].k} ${sa[sa.length-1].p}%.`); }
  else if(sa.length===1) L.push(`Logged accuracy so far: ${SYS[sa[0].k]||sa[0].k} ${sa[0].p}% (${sa[0].q} Qs). Systems get ranked once you've logged two.`);''')
open(p,'w').write(t); print('ok')

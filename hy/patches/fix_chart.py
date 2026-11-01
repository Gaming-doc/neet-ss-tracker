p='tracker.tpl.html'; t=open(p).read()
def rep(a,b):
    global t
    assert t.count(a)==1,(a[:80],t.count(a)); t=t.replace(a,b)
rep('''  const W=640,H=230,L=44,R=14,T=22,B=34, pts=TESTS.map((x,k)=>({x,k,m:marks(sc(x.id))}));''',
    '''  const host=$("#statsView"), W=Math.max(300,Math.min(900,((host&&host.clientWidth)||640)-34)), narrow=W<560;
  const H=narrow?200:230,L=narrow?36:44,R=narrow?18:30,T=22,B=34, pts=TESTS.map((x,k)=>({x,k,m:marks(sc(x.id))}));''')
rep('''  s+=pts.map(p=>`<text class="ax" x="${X(p.k)}" y="${H-12}" text-anchor="middle">${p.x.t.replace("PYQ ","PYQ ’").replace("’20","’")}</text>`).join("");''',
    '''  const lab=x=>narrow ? x.t.replace("PYQ 20","P").replace("Mock ","M") : x.t.replace("PYQ 20","PYQ ’");
  s+=pts.map(p=>`<text class="ax" x="${X(p.k)}" y="${H-12}" text-anchor="middle">${lab(p.x)}</text>`).join("");''')
rep('''${inq?`<span class="lt" style="color:var(--warn)">+${inq} Qs moved in</span>`:""}''','''${inq?`<span class="lt" style="color:var(--warn);text-transform:none;letter-spacing:0">+${inq} Qs moved in</span>`:""}''')
rep('''.chart{width:100%;height:auto;display:block}''','''.chart{width:100%;height:auto;display:block;max-width:100%}''')
open(p,'w').write(t); print('ok')

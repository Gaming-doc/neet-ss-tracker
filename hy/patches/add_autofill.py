p='tracker.tpl.html'; t=open(p).read()
def rep(a,b,n=1):
    global t
    assert t.count(a)==n,(a[:90],t.count(a)); t=t.replace(a,b)

# minute steps so 3-min-per-question times are valid
rep('step="300"','step="60"',2)

# helpers
rep('''function planM(v){''','''// ---------- Main auto-plan: 30 min per 10 questions ----------
const MIN_PER_Q=3;
function addM(h,m){ const x=((+h.slice(0,2)*60+ +h.slice(3)+m)%1440+1440)%1440; return String(Math.floor(x/60)).padStart(2,"0")+":"+String(x%60).padStart(2,"0"); }
function flag(v,f,on){ let a=(v.a||"").replace(f,""); if(on) a+=f; if(a) v.a=a; else delete v.a; }
function mainSeq(d){ return itemsOf(d).filter(i=>!i.from && i.k==="main"); }
function setTimeUI(id,v){ const it=document.querySelector(`#sheet .item[data-id="${CSS.escape(id)}"]`); if(!it) return; it.querySelectorAll(".tm-in").forEach(x=>{ x.value=v[x.dataset.f]||""; x.classList.toggle("set",!!x.value); }); }
function autoFillMain(d,id){
  const seq=mainSeq(d), k=seq.findIndex(i=>i.id===id); if(k<0) return;
  let cur=null, last=null;
  for(let j=k;j<seq.length;j++){
    const it=seq[j], v=Object.assign({},tget(it.id));
    if(j===k){ if(!v.s) return; }
    else { if(v.s && !(v.a||"").includes("s")) break; v.s=cur; flag(v,"s",true); }
    if(!v.e || (v.a||"").includes("e")){ v.e=addM(v.s, it.q*MIN_PER_Q); flag(v,"e",true); }
    times[it.id]=v; setTimeUI(it.id,v); cur=v.e; last=it;
  }
  // hand the finish time to whatever comes right after the last Main module, if its start is empty or was filled in for you
  if(last && last===seq[seq.length-1]){
    const rows=[...document.querySelectorAll("#sheet .blocks .item")], el=document.querySelector(`#sheet .item[data-id="${CSS.escape(last.id)}"]`), nx=rows[rows.indexOf(el)+1];
    if(nx){ const nv=Object.assign({},tget(nx.dataset.id)); if(!nv.s || (nv.a||"").includes("s")){ nv.s=cur; flag(nv,"s",true); times[nx.dataset.id]=nv; setTimeUI(nx.dataset.id,nv); } }
  }
}
function planM(v){''')

# change handler
rep('''    const id=inp.dataset.id, v=Object.assign({},tget(id)), oldE=v.e||"";
    if(inp.value) v[inp.dataset.f]=inp.value; else delete v[inp.dataset.f];
    if(v.s||v.e) times[id]=v; else delete times[id];
    inp.classList.toggle("set",!!inp.value);
    // an end time becomes the next module's start, unless you've set that start yourself
    if(inp.dataset.f==="e"){
      const rows=[...document.querySelectorAll("#sheet .blocks .item")], k=rows.indexOf(inp.closest(".item")), nx=rows[k+1];
      if(nx){
        const nid=nx.dataset.id, nv=Object.assign({},tget(nid));
        if(!nv.s || nv.s===oldE){
          if(inp.value) nv.s=inp.value; else delete nv.s;
          if(nv.s||nv.e) times[nid]=nv; else delete times[nid];
          const ns=nx.querySelector('.tm-in[data-f="s"]'); if(ns){ ns.value=nv.s||""; ns.classList.toggle("set",!!nv.s); }
        }
      }
    }
    queueSave(); renderMyTimes(d);''','''    const id=inp.dataset.id, f=inp.dataset.f, v=Object.assign({},tget(id)), oldE=v.e||"";
    if(inp.value) v[f]=inp.value; else delete v[f];
    flag(v,f,false);   // a time you type yourself is never overwritten
    if(v.s||v.e) times[id]=v; else delete times[id];
    inp.classList.toggle("set",!!inp.value);
    let nextMain=null;
    // an end time becomes the next module's start, unless you've set that start yourself
    if(f==="e"){
      const rows=[...document.querySelectorAll("#sheet .blocks .item")], k=rows.indexOf(inp.closest(".item")), nx=rows[k+1];
      if(nx){
        const nid=nx.dataset.id, nv=Object.assign({},tget(nid));
        if(!nv.s || nv.s===oldE || (nv.a||"").includes("s")){
          if(inp.value){ nv.s=inp.value; flag(nv,"s",true); } else { delete nv.s; flag(nv,"s",false); }
          if(nv.s||nv.e) times[nid]=nv; else delete times[nid];
          const ns=nx.querySelector('.tm-in[data-f="s"]'); if(ns){ ns.value=nv.s||""; ns.classList.toggle("set",!!nv.s); }
          if(nv.s && mainSeq(d).some(i=>i.id===nid)) nextMain=nid;
        }
      }
    }
    if(f==="s" && inp.value && mainSeq(d).some(i=>i.id===id)) autoFillMain(d,id);
    if(nextMain) autoFillMain(d,nextMain);
    queueSave(); renderMyTimes(d);''')

rep("Set a start and end time beside any module to plan today in your own order. Each end time fills in the next module's start.",
    "Set a start and end time beside any module to plan today in your own order. A start time on a Main module plans the rest of Blocks A–C at 30 min per 10 questions. Each end time fills in the next module's start.")
open(p,'w').write(t); print('template ok')

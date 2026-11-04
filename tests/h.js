// shared harness
const {chromium}=require('playwright'); const fs=require('fs'); const path=require('path');
function gasSim(src,dst){ const t=fs.readFileSync(src,'utf8'); const s=t.indexOf('<script>\nconst DATA'); const e=t.lastIndexOf('</script>');
  const lines=t.slice(s,e).split('\n'); const sus=lines.filter(l=>l.includes('//')&&l.slice(0,l.indexOf('//')).trim()&&!/[;){}]\s*$/.test(l.slice(0,l.indexOf('//'))));
  const out=lines.map(l=>l.includes('//')?l.slice(0,l.indexOf('//')):l); fs.writeFileSync(dst,t.slice(0,s)+out.join('\n')+t.slice(e)); return sus; }
async function open(b,o){
  o=Object.assign({width:1300,height:1000,time:'2026-11-01T18:15:00Z',file:'sim.html',data:null,local:null,mode:'gas'},o);
  const pg=await b.newPage({viewport:{width:o.width,height:o.height}}); pg.errs=[];
  pg.on('pageerror',e=>pg.errs.push('PAGEERR '+e.message+' @'+(e.stack||'').split('\n').slice(1,3).join(' ')));
  pg.on('console',m=>{ if(m.type()==='error'&&!/ERR_TUNNEL|Failed to load resource/.test(m.text())) pg.errs.push('CONSOLE '+m.text()); });
  pg.on('dialog',d=>{ pg.errs.push('DIALOG '+d.message()); d.dismiss(); });
  await pg.clock.install({time:new Date(o.time)});
  await pg.addInitScript(([data,local,mode])=>{
    if(local) for(const k in local) localStorage.setItem(k,local[k]);
    window.__saves=[];
    if(mode==='gas'){ const mk=()=>{ let ok=()=>{},fl=()=>{}; const r={withSuccessHandler(f){ok=f;return r;},withFailureHandler(f){fl=f;return r;},loadProgress(){setTimeout(()=>window.__gasFail?fl(new Error('x')):ok(data),40);},saveProgress(j){window.__saves.push(j);setTimeout(()=>ok(new Date().toISOString()),20);}, loadDm(){ return r.loadProgress(); }, saveDm(j){ return r.saveProgress(j); } }; return r; }; window.google={script:{get run(){return mk();}}}; }
    if(mode==='claude'){ let snapCb=null; const store={v:data?JSON.parse(data):null};
      const ref={onSnapshot(cb,err){ snapCb=cb; setTimeout(()=>cb({exists:!!store.v,data:()=>store.v,metadata:{fromCache:false,hasPendingWrites:false}}),40); return ()=>{}; }, async set(v){ store.v=JSON.parse(JSON.stringify(v)); window.__saves.push(JSON.stringify(v)); }};
      window.claude={use:async(n)=>n==='db'?{doc:()=>ref}:n==='sample'?(async(p,cb)=>{ window.__prompt=p; cb&&cb.onText&&cb.onText({text:'AI says hi'}); return 'AI says hi'; }):null}; }
  },[o.data,o.local,o.mode]);
  await pg.goto('file://'+path.resolve(o.file)); await pg.clock.fastForward(1500); await pg.waitForTimeout(250);
  return pg;
}
const lastSave=pg=>pg.evaluate(()=>window.__saves.length?JSON.parse(window.__saves[window.__saves.length-1]):null);
const localState=pg=>pg.evaluate(()=>{ const o={}; for(let i=0;i<localStorage.length;i++){ const k=localStorage.key(i); o[k]=localStorage.getItem(k);} return o; });
module.exports={chromium,gasSim,open,lastSave,localState,fs};

import json
T=open('tracker.tpl.html').read()
DATA=open('marrow/schedule4.json').read()
SEED={}  # optional: module ids to pre-tick on a brand-new device, e.g. {"m:Cardio: IHD":1}
def must(t,a,b):
    assert a in t, a[:60]; return t.replace(a,b)
# ---- Claude artifact build (db sync) ----
a=T
a=must(a,"let db = null, ref = null, writing = false, pendingWrite = false;","let db = null, ref = null, writing = false, pendingWrite = false, dirty = false;")
a=must(a,"function queueSave(){\n  saveLocal();\n  if(!ref){ return; }","function queueSave(){\n  saveLocal();\n  if(!ref){ return; }\n  dirty=true;")
a=must(a,"  writing=false;\n  if(pendingWrite){ pendingWrite=false; flush(); }","  writing=false;\n  if(pendingWrite){ pendingWrite=false; flush(); } else dirty=false;")
a=must(a,"    if(snap.metadata && snap.metadata.hasPendingWrites) return;","    if((snap.metadata && snap.metadata.hasPendingWrites) || dirty) { first=false; return; }")
a=a.replace("__DATA__",DATA)
open('dist/neet-ss-tracker.html','w').write(a)
# ---- Google Apps Script build (Drive sync) ----
g=T
s=g.index('async function connect(){'); e=g.index('// ---------- math ----------')
GAS=r'''
// ---------- Google Drive sync via Apps Script ----------
const HAS_GAS = typeof google!=="undefined" && google.script && google.script.run;
let gasTimer=null, gasBusy=false, gasAgain=false;
function stamp(){ const s=new Date().toISOString(); try{ localStorage.setItem("neetss-updated",s); }catch(e){} return s; }
function localStamp(){ try{ return localStorage.getItem("neetss-updated")||""; }catch(e){ return ""; } }
function gasSave(){
  if(!HAS_GAS) return;
  clearTimeout(gasTimer);
  gasTimer=setTimeout(()=>{
    if(gasBusy){ gasAgain=true; return; }
    gasBusy=true; setSync("warn","Saving to Google Drive…");
    google.script.run
      .withSuccessHandler(()=>{ gasBusy=false; setSync("ok","Saved to Google Drive"); if(gasAgain){ gasAgain=false; gasSave(); } })
      .withFailureHandler(()=>{ gasBusy=false; setSync("warn","Couldn't reach Google Drive — kept on this device, will retry on next tap"); })
      .saveProgress(JSON.stringify({app:"NEET SS Highlighter Tracker",done,times,actual,ext,updatedAt:localStamp()||stamp()}));
  },700);
}
function gasLoad(){
  if(!HAS_GAS){ setSync("warn","Saved on this device only"); return; }
  if(gasBusy || gasAgain) return;
  google.script.run
    .withSuccessHandler(txt=>{
      let remote=null; try{ remote=txt?JSON.parse(txt):null; }catch(e){}
      const local=localStamp();
      if(remote && remote.done && (!local || (remote.updatedAt||"")>=local)){
        done=Object.assign({},remote.done); times=Object.assign({},remote.times||{}); actual=Object.assign({},remote.actual||{}); ext=normExt(remote.ext); saveLocal();
        try{ localStorage.setItem("neetss-updated",remote.updatedAt||""); }catch(e){}
        renderAll(); setSync("ok","Synced with Google Drive");
      } else { gasSave(); }
    })
    .withFailureHandler(()=>setSync("warn","Couldn't reach Google Drive — showing this device's copy"))
    .loadProgress();
}
function connect(){ gasLoad(); document.addEventListener("visibilitychange",()=>{ if(document.visibilityState==="visible") gasLoad(); }); }

'''
g=g[:s]+GAS+g[e:]
qs=g.index('let saveTimer=null;'); fe=g.index('// ---------- Google Drive sync via Apps Script')
g=g[:qs]+'function queueSave(){ saveLocal(); stamp(); gasSave(); }\nfunction flush(){}\n'+g[fe:]
g=must(g,"let db = null, ref = null, writing = false, pendingWrite = false;","const ref = null;")
g=must(g,'function loadLocal(){ try{','const SEED='+json.dumps(SEED)+';\nfunction loadLocal(){ done=Object.assign({},SEED); try{')
g=g.replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
g=g.replace("__DATA__",DATA)
g=g.replace('<style>\n','<style>\nbody{margin:0} [hidden]{display:none!important} img{max-width:100%}\n',1)
i=g.index('<div class="wrap">')
html='<!DOCTYPE html>\n<html>\n<head>\n<base target="_top">\n'+g[:i]+'</head>\n<body>\n'+g[i:]+'\n</body>\n</html>\n'
open('dist/NEET SS Tracker app.html','w').write(html)
print(len(a),len(html))

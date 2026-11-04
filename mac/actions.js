// Menu-bar actions: same rules as the tracker's act(), startBrk(), endBrk(), wakeNow(), bedNow().
function neetAct(D, what, arg, nowMs){
  var now=new Date(nowMs).toISOString();
  D.actual=D.actual||{}; D.done=D.done||{}; D.ext=D.ext||{};
  var A=D.actual, ext=D.ext; ext.dt=ext.dt||{}; ext.sleep=ext.sleep||{}; if(!Array.isArray(ext.brk)) ext.brk=[];
  function pauses(a){ return Array.isArray(a.p)?a.p:(a.p=[]); }
  function isPaused(a){ var p=Array.isArray(a.p)?a.p:[]; return !!(a&&a.s&&!a.e&&p.length&&!p[p.length-1].t); }
  function running(a){ return a&&a.s&&!a.e&&!isPaused(a); }
  function closePause(a){ var p=pauses(a); if(p.length&&!p[p.length-1].t) p[p.length-1].t=now; }
  function runBrk(){ for(var i=ext.brk.length-1;i>=0;i--) if(!ext.brk[i].e) return ext.brk[i]; return null; }
  function endBrk(){ var b=runBrk(); if(b) b.e=now; return b; }
  function hhmm(ms){ var d=new Date(ms+19800000); return String(d.getUTCHours()).padStart(2,"0")+":"+String(d.getUTCMinutes()).padStart(2,"0"); }
  var today=neetCore(D,nowMs).today, a=A[arg];
  if(what==="p"){ if(running(a)) pauses(a).push({f:now}); }
  else if(what==="r"){ if(isPaused(a)){ endBrk(); for(var k in A) if(k!==arg&&running(A[k])) pauses(A[k]).push({f:now}); closePause(a); } }
  else if(what==="e"){ if(a&&a.s&&!a.e){ if(isPaused(a)) closePause(a); a.e=now; if(!D.done[arg]&&!/^x:/.test(arg)){ D.done[arg]=1; ext.dt[arg]=today; } } }
  else if(what==="own"){ var nm=String(arg||"").trim().slice(0,80)||"Own study", id="x:"+nowMs.toString(36); ext.free=ext.free||{}; ext.free[id]={n:nm,k:/harrison/i.test(nm)?"read":"other",d:today};
    endBrk(); for(var k6 in A) if(running(A[k6])) pauses(A[k6]).push({f:now}); A[id]={s:now}; }
  else if(what==="brk"){ endBrk(); var pid=null; for(var k2 in A) if(running(A[k2])){ pauses(A[k2]).push({f:now}); pid=k2; }
    var b={k:arg,s:now}; if(pid) b.pid=pid; ext.brk.push(b); }
  else if(what==="brkEnd"){ var rb=runBrk(); if(rb){ rb.e=now; var any=false; for(var k3 in A) if(running(A[k3])) any=true;
    if(rb.pid&&A[rb.pid]&&isPaused(A[rb.pid])&&!any) closePause(A[rb.pid]); } }
  else if(what==="wake"){ var c=new Date(nowMs+19800000).toISOString().slice(0,10), s=Object.assign({},ext.sleep[c]||{}); s.w=hhmm(nowMs);
    if(ext.bed && nowMs-Date.parse(ext.bed)<20*3600000) s.b=hhmm(Date.parse(ext.bed)); ext.sleep[c]=s; ext.bed=null; }
  else if(what==="bed"){ for(var k4 in A){ var o=A[k4]; if(o&&o.s&&!o.e){ closePause(o); o.e=now; } } endBrk(); ext.bed=now; }
  else return false;
  D.updatedAt=now;
  return true;
}
function neetHex(s){ return Array.prototype.map.call(unescape(encodeURIComponent(s)),function(ch){ return ("0"+ch.charCodeAt(0).toString(16)).slice(-2); }).join(""); }
function neetUnhex(h){ return decodeURIComponent(h.replace(/../g,"%$&")); }
if(typeof module!=="undefined") module.exports={neetAct:neetAct,neetHex:neetHex,neetUnhex:neetUnhex};

#!/bin/bash
# <xbar.title>NEET SS study timer</xbar.title>
# <xbar.desc>Live studied / awake / break time from the NEET SS tracker (reads the progress file Google Drive syncs to this Mac).</xbar.desc>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
/usr/bin/osascript -l JavaScript - "$0" "$@" <<'JXA'
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
  else if(what==="bed"){ for(var k4 in A){ var o=A[k4]; if(running(o)) pauses(o).push({f:now}); } endBrk(); ext.bed=now; }
  else return false;
  D.updatedAt=now;
  return true;
}
function neetHex(s){ return Array.prototype.map.call(unescape(encodeURIComponent(s)),function(ch){ return ("0"+ch.charCodeAt(0).toString(16)).slice(-2); }).join(""); }
function neetUnhex(h){ return decodeURIComponent(h.replace(/../g,"%$&")); }


// Decides which Mac notifications to show this second. Pure: (core output, now, saved state) -> {msgs, state}.
function neetNotify(c, nowMs, st){
  st=st||{}; st.sent=st.sent||{}; st.lvl=st.lvl||{}; var msgs=[], M=60000;
  if(st.off) return {msgs:msgs,state:st};
  function once(key,title,body){ if(!st.sent[key]){ st.sent[key]=nowMs; msgs.push({title:title,body:body}); } }
  function fmt(m){ m=Math.round(m); var h=Math.floor(m/60), r=m%60; return h?(h+" h"+(r?" "+r+" min":"")):(r+" min"); }
  var lightsOut=Date.parse(c.today+"T00:00:00+05:30")+23*60*M;
  // 4. named break over its guide (again every 15 min over)
  if(c.onBreak && c.brkStart && c.onBreak.min>=c.onBreak.max){
    var n=Math.floor((c.onBreak.min-c.onBreak.max)/15);
    once("brk:"+c.brkStart+":"+n, "☕ "+c.onBreak.name+" is at "+fmt(c.onBreak.min), "Guide is "+c.onBreak.max+" min."+(c.onBreak.pname?" Back to "+c.onBreak.pname+"?":" Time to get back to it."));
  }
  // 5. 90 min straight without a break (again every 30 min)
  if(c.run && c.ivMs && c.ivMs.length){
    var segs=[]; c.ivMs.forEach(function(x){ var l=segs[segs.length-1]; if(l && x[0]-l[1]<=60000) l[1]=Math.max(l[1],x[1]); else segs.push([x[0],x[1]]); });
    var last=segs[segs.length-1];
    if(last && nowMs-last[1]<=5000){ var len=(last[1]-last[0])/M;
      if(len>=90){ var k=Math.floor((len-90)/30); once("nb:"+last[0]+":"+k, "⏱ "+fmt(len)+" straight", "On "+c.run.name+". Take 10 minutes: water, stand up, look away from the screen."); } }
  }
  // 6. awake, nothing running and no named break for 20 min (again every 20 min), until lights out
  if(!c.run && !c.onBreak && !c.sleeping && c.woke && nowMs<lightsOut){
    var lastEnd=c.sMs||0; (c.ivMs||[]).forEach(function(x){ if(x[1]>lastEnd) lastEnd=x[1]; }); if(c.lastBrkEnd&&c.lastBrkEnd>lastEnd) lastEnd=c.lastBrkEnd;
    var idle=(nowMs-lastEnd)/M;
    if(lastEnd && idle>=20){ var j=Math.floor((idle-20)/20);
      once("idle:"+lastEnd+":"+j, "Nothing running for "+fmt(idle), c.paused&&c.paused.length?"Resume "+c.paused[0].name+", or log a named break.":"Start a module or own study, or log a named break."); }
  }
  // 7. study-ratio milestones (after the first hour awake; 2% hysteresis so it doesn't flicker)
  if(c.awakeS>=3600 && !c.sleeping){
    var r=c.studiedS/c.awakeS, prev=st.lvl[c.today]||0, lvl;
    if(r>=0.75) lvl=2; else if(r>=0.5) lvl=(prev===2&&r>=0.73)?2:1; else lvl=(prev>=1&&r>=0.48)?1:0;
    if(lvl>prev){ if(lvl===2) msgs.push({title:"✅ Study ratio crossed 75%",body:Math.round(r*100)+"% of your awake time today is study. Keep it there."});
      else msgs.push({title:"🟠 Study ratio crossed 50%",body:Math.round(r*100)+"% so far. Next stop 75%."}); }
    st.lvl[c.today]=lvl;
  }
  // tidy: keep a day of history
  for(var key in st.sent) if(nowMs-st.sent[key]>36*3600000) delete st.sent[key];
  return {msgs:msgs,state:st};
}


// NEET SS menu-bar core: same day/sleep/break rules as the tracker (IST, day starts at wake-up).
function neetCore(D, nowMs){
  var IST=19800000, DAY_CUT=360;
  var ext=D.ext||{}, actual=D.actual||{}, sleep=ext.sleep||{}, brk=Array.isArray(ext.brk)?ext.brk:[];
  function cal(ms){ return new Date(ms+IST).toISOString().slice(0,10); }
  function calMin(ms){ var x=new Date(ms+IST); return x.getUTCHours()*60+x.getUTCMinutes(); }
  function addDays(s,n){ var d=new Date(s+"T00:00:00Z"); d.setUTCDate(d.getUTCDate()+n); return d.toISOString().slice(0,10); }
  function hm2m(h){ return h? (+h.slice(0,2))*60+(+h.slice(3)) : null; }
  function wakeMin(date){ var s=sleep[date]; return s&&s.w?hm2m(s.w):null; }
  function P(iso){ return Date.parse(iso); }
  function dayOf(iso){ var ms=P(iso), c=cal(ms), m=calMin(ms), w=wakeMin(c); return m<(w!=null?Math.min(w,720):DAY_CUT)?addDays(c,-1):c; }
  function pauses(a){ return Array.isArray(a.p)?a.p:[]; }
  function isPaused(a){ var p=pauses(a); return !!(a&&a.s&&!a.e&&p.length&&!p[p.length-1].t); }
  function today(){
    var c=cal(nowMs), m=calMin(nowMs), w=wakeMin(c);
    if(w!=null) return m>=Math.min(w,720)?c:addDays(c,-1);
    if(m<DAY_CUT) return addDays(c,-1);
    if(m<720 && !ext.bed){ var Pd=addDays(c,-1), lim=nowMs-3600000;
      for(var k in actual){ var a=actual[k]; if(!a||!a.s||dayOf(a.s)!==Pd) continue;
        var pp=pauses(a), lp=pp[pp.length-1];
        if(!a.e && !(lp&&!lp.t)){ var seg=lp?P(lp.t):P(a.s); if(nowMs-seg<3*3600000) return Pd; continue; }
        var last=a.e?P(a.e):P(lp.f); if(last>=lim) return Pd; } }
    return c;
  }
  var T=today(), base=P(T+"T00:00:00+05:30"), mOf=function(ms){ return Math.round((ms-base)/60000); }, nowIso=new Date(nowMs).toISOString();
  // Today runs from today's wake-up (or 06:00) onwards. Each stretch of study counts on the day it happened,
  // so a module carried over from an earlier day (paused overnight, resumed today) counts today's part.
  var wT=wakeMin(T), W0=base+(wT!=null?Math.min(wT,720):DAY_CUT)*60000;
  function segs(a){ var out=[], end=a.e||nowIso, cur=a.s;
    function add(f,t){ var lo=Math.max(P(f),W0), hi=P(t); if(hi>lo) out.push([lo,hi]); }
    pauses(a).slice().sort(function(x,y){ return x.f<y.f?-1:1; }).forEach(function(p){ if(p.f>cur) add(cur,p.f); cur=p.t||end; });
    if(end>cur) add(cur,end); return out; }
  var iv=[], ivMs=[];
  for(var id in actual){ var a=actual[id]; if(!a||!a.s) continue;
    segs(a).forEach(function(x){ ivMs.push(x); iv.push([mOf(x[0]),mOf(x[1])]); }); }
  iv=iv.filter(function(x){ return x[1]>x[0]; }).sort(function(x,y){ return x[0]-y[0]; });
  var studied=iv.reduce(function(s,x){ return s+(x[1]-x[0]); },0);
  var sl=sleep[T], wm=sl&&sl.w?hm2m(sl.w):null;
  var bed=null, nx=sleep[addDays(T,1)];
  if(nx&&nx.b){ var bm=hm2m(nx.b); bed=bm>=720?bm:bm+1440; } else if(ext.bed && dayOf(ext.bed)===T) bed=mOf(P(ext.bed));
  var start=wm!=null?wm:(iv.length?iv[0][0]:null), nowM=mOf(nowMs), endM=bed!=null?bed:nowM;
  var awake=start!=null?Math.max(0,endM-start):0, cov=0, c2=start;
  if(start!=null) iv.forEach(function(x){ var lo=Math.max(x[0],c2), hi=Math.min(x[1],endM); if(hi>lo){ cov+=hi-lo; } c2=Math.max(c2,x[1]); });
  var breaks=Math.max(0,awake-cov);
  ivMs=ivMs.filter(function(x){ return x[1]>x[0]; }).sort(function(x,y){ return x[0]-y[0]; });
  var studiedS=Math.round(ivMs.reduce(function(s,x){ return s+(x[1]-x[0]); },0)/1000);
  var sMs=wm!=null?base+wm*60000:(ivMs.length?ivMs[0][0]:null), eMs=bed!=null?base+bed*60000:nowMs, awakeS=0, covS=0;
  if(sMs!=null){ awakeS=Math.max(0,Math.round((eMs-sMs)/1000)); var c3=sMs; ivMs.forEach(function(x){ var lo=Math.max(x[0],c3), hi=Math.min(x[1],eMs); if(hi>lo) covS+=(hi-lo)/1000; c3=Math.max(c3,x[1]); }); }
  var breaksS=Math.max(0,Math.round(awakeS-covS));
  var slept=null; if(sl&&sl.w&&sl.b){ slept=(((hm2m(sl.w)-hm2m(sl.b))%1440)+1440)%1440; }
  var run=null, paused=[];
  var free=ext.free||{}; function nm(id){ return free[id]&&free[id].n ? free[id].n : String(id).replace(/^[^:]*:/,"").trim(); }
  for(var id2 in actual){ var a2=actual[id2]; if(!a2||!a2.s||a2.e) continue; var name=nm(id2);
    if(isPaused(a2)) paused.push({id:id2,name:name}); else { var pp2=pauses(a2), act=Math.max(0,(nowMs-P(a2.s))/60000-pp2.reduce(function(s,x){ return s+(P(x.t||nowIso)-P(x.f))/60000; },0)); run={id:id2,free:/^x:/.test(id2),name:name,min:Math.round(act),sec:Math.round(act*60)}; } }
  var rb=null; for(var i=brk.length-1;i>=0;i--){ if(!brk[i].e){ rb=brk[i]; break; } }
  var BRK={lunch:["Lunch",45],dinner:["Dinner",45],series:["Series",30],nap:["Short nap",30],other:["Break",30]};
  var onBrk=rb?{name:rb.k==="other"&&rb.n?rb.n:(BRK[rb.k]||BRK.other)[0],min:Math.round((nowMs-P(rb.s))/60000),sec:Math.round((nowMs-P(rb.s))/1000),max:(BRK[rb.k]||BRK.other)[1],pid:rb.pid||null,pname:rb.pid?nm(rb.pid):null}:null;
  var doneToday=0; for(var k2 in (ext.dt||{})) if(ext.dt[k2]===T&&!/^x:/.test(k2)) doneToday++;
  var own=0; for(var k5 in free){ var a5=actual[k5]; if(a5&&a5.s) segs(a5).forEach(function(x){ own+=(x[1]-x[0])/1000; }); }
  var lastBrkEnd=null; brk.forEach(function(b){ if(b.e&&b.s&&dayOf(b.s)===T){ var e=P(b.e); if(lastBrkEnd==null||e>lastBrkEnd) lastBrkEnd=e; } });
  return {ivMs:ivMs,sMs:sMs,lastBrkEnd:lastBrkEnd,brkStart:rb?P(rb.s):null,today:T,awake:awake,studied:studied,breaks:breaks,awakeS:awakeS,studiedS:studiedS,breaksS:breaksS,woke:sl&&sl.w||null,slept:slept,sleeping:!!ext.bed,bedAt:ext.bed||null,run:run,paused:paused,ownS:Math.round(own),onBreak:onBrk,doneToday:doneToday,updatedAt:D.updatedAt||null};
}


// Turns neetCore() output into SwiftBar/xbar menu text.
function neetRender(c, info){
  function hm(m){ if(m==null) return "–"; m=Math.max(0,Math.round(m)); return Math.floor(m/60)+":"+String(m%60).padStart(2,"0"); }
  function hms(s){ if(s==null) return "–"; s=Math.max(0,Math.round(s)); return Math.floor(s/3600)+":"+String(Math.floor(s/60)%60).padStart(2,"0")+":"+String(s%60).padStart(2,"0"); }
  function long(m){ m=Math.max(0,Math.round(m)); var h=Math.floor(m/60), r=m%60; return h?(h+" h"+(r?" "+r+" min":"")):(r+" min"); }
  function clk(iso){ var d=new Date(Date.parse(iso)+19800000); return String(d.getUTCHours()).padStart(2,"0")+":"+String(d.getUTCMinutes()).padStart(2,"0"); }
  var L=[], F=" | font=Menlo size=13", url=info.url;
  function A(label,what,arg,extra){ return label+" | bash=\""+info.self+"\" param1=act param2="+what+" param3="+(arg?neetHex(arg):"x")+" terminal=false refresh=true"+(extra||""); }
  if(!c){ L.push("📖 ? | color=#D9822B"); L.push("---"); L.push(info.err||"Couldn't read the tracker file."); L.push("Open tracker | href="+url); L.push("Refresh | refresh=true"); return L.join("\n"); }
  var awakeTxt=(c.woke||c.awakeS)?hms(c.awakeS):"–";
  var title=c.sleeping?"😴 📖 "+hms(c.studiedS):c.onBreak?"☕ "+c.onBreak.name+" "+hms(c.onBreak.sec)+" · 📖 "+hms(c.studiedS):"📖 "+hms(c.studiedS)+" · ☀️ "+awakeTxt;
  var tcol=c.onBreak&&c.onBreak.min>c.onBreak.max?" | color=#D9363E":"";
  L.push(title+tcol+(tcol?" font=Menlo":" | font=Menlo"));
  L.push("---");
  L.push("NEET SS · "+c.today+" | size=12 color=#888888");
  L.push("Studied   "+hms(c.studiedS)+F);
  L.push("Awake     "+((c.woke||c.awakeS)?hms(c.awakeS)+(c.woke?"  (up since "+c.woke+")":""):"– tap I'm up now in the tracker")+F);
  var pct=c.awake?Math.round(100*c.breaks/c.awake):0;
  L.push("Breaks    "+hms(c.breaksS)+(c.awake?"  ("+pct+"% of awake)":"")+F+(c.awake>=120&&pct>30?" color=#D9822B":""));
  if(c.slept!=null) L.push("Slept     "+long(c.slept)+" last night"+F+(c.slept<360?" color=#D9363E":""));
  if(c.ownS) L.push("Own study "+hms(c.ownS)+"  (outside modules)"+F);
  if(c.awakeS){
    var r=c.studiedS/c.awakeS, col=r>=0.75?"#1F9D62":r>=0.5?"#D9822B":"#D9363E";
    L.push("Study ratio "+Math.round(100*r)+"% of awake time"+F+" color="+col);
    if(!c.sleeping){
      if(r<0.75){ var tgt=r<0.5?0.5:0.75, need=Math.ceil((tgt*c.awakeS-c.studiedS)/(1-tgt));
        var endMs=Date.now()+need*1000, at=clk(new Date(endMs).toISOString()), late=(endMs-Date.parse(c.today+"T00:00:00+05:30"))/60000>1380;
        L.push("To reach "+Math.round(tgt*100)+"%  "+hms(need)+" of non-stop study"+F+" color="+col);
        L.push("              "+(late?"→ "+at+", past 23:00 lights out":"→ by "+at+" if you start now")+" | font=Menlo size=12 color=#888888"); }
      else { var spare=Math.floor((4*c.studiedS-3*c.awakeS)/3);
        L.push("Above 75% ✓  you could take a "+hms(spare)+" break and stay above"+F+" color="+col); } } }
  L.push("---");
  if(c.sleeping){ L.push("😴 Sleeping since "+clk(c.bedAt)); L.push(A("☀️  I'm up now","wake")); }
  else if(!c.woke) L.push(A("☀️  I'm up now","wake"));
  if(c.onBreak){ L.push("☕ On "+c.onBreak.name+" · "+hms(c.onBreak.sec)+" (guide "+c.onBreak.max+" min)"+(c.onBreak.min>c.onBreak.max?" | color=#D9363E":""));
    L.push(A("■  End break"+(c.onBreak.pname&&c.paused.some(function(p){ return p.id===c.onBreak.pid; })?" & resume "+c.onBreak.pname:""),"brkEnd")); }
  if(c.run){ L.push((c.run.free?"📘 ":"▶ ")+c.run.name+" · "+hms(c.run.sec)+(c.run.free?" own study":" on this module")+(c.run.min>=180?"  (still running?) | color=#D9822B":""));
    L.push(A("⏸  Pause","p",c.run.id));
    L.push("☕  Take a break");
    [["lunch","Lunch"],["dinner","Dinner"],["series","Series"],["nap","Short nap"],["other","Other break"]].forEach(function(b){ L.push("--"+A(b[1],"brk",b[0])); });
    L.push(A(c.run.free?"■  End":"■  End now (ticks it done)","e",c.run.id)); }
  c.paused.forEach(function(p){ var held=c.onBreak&&c.onBreak.pid===p.id; L.push("⏸ "+p.name+" (paused)"); if(!held) L.push(A("▶  Resume "+p.name,"r",p.id)); });
  if(!c.run&&!c.onBreak&&!c.sleeping){ L.push("Nothing running right now | color=#888888"); if(c.woke){ L.push("☕  Take a break"); [["lunch","Lunch"],["dinner","Dinner"],["series","Series"],["nap","Short nap"],["other","Other break"]].forEach(function(b){ L.push("--"+A(b[1],"brk",b[0])); }); } }
  if(!c.sleeping) L.push(A("📘  Start own study…","own"));
  if(!c.sleeping&&c.woke) L.push(A("😴  Going to sleep","bed"));
  L.push("Modules ticked today: "+c.doneToday);
  L.push(A(info.notifOff?"🔕  Notifications off (click to turn on)":"🔔  Notifications on (click to turn off)","notif"));
  L.push("---");
  L.push("Open tracker | href="+url);
  if(c.updatedAt) L.push("Last saved "+clk(c.updatedAt)+" | size=11 color=#888888");
  L.push("Refresh | refresh=true");
  return L.join("\n");
}



ObjC.import('Foundation');
function readText(p){ try{ var s=$.NSString.stringWithContentsOfFileEncodingError(p,$.NSUTF8StringEncoding,null); var u=ObjC.unwrap(s); return (typeof u==="string")?u:null; }catch(e){ return null; } }
function writeText(p,txt){ try{ return !!$.NSString.alloc.initWithUTF8String(txt).writeToFileAtomicallyEncodingError(p,false,$.NSUTF8StringEncoding,null); }catch(e){ return false; } }
function listDir(p){ try{ return ObjC.deepUnwrap($.NSFileManager.defaultManager.contentsOfDirectoryAtPathError(p,null))||[]; }catch(e){ return []; } }
function findFile(){
  var home=ObjC.unwrap($.NSHomeDirectory()), cs=home+"/Library/CloudStorage", F="neet-ss-tracker-progress.json", cands=[];
  listDir(cs).filter(function(n){ return n.indexOf("GoogleDrive")===0; }).sort(function(a,b){ return (b.indexOf("sadananth")>=0)-(a.indexOf("sadananth")>=0); })
    .forEach(function(n){ cands.push(cs+"/"+n+"/My Drive/"+F); listDir(cs+"/"+n).forEach(function(m){ if(m!=="My Drive") cands.push(cs+"/"+n+"/"+m+"/"+F); }); });
  cands.push(home+"/Google Drive/My Drive/"+F);
  for(var i=0;i<cands.length;i++){ var t=readText(cands[i]); if(t) return {path:cands[i],txt:t}; }
  return null;
}
function statePath(){ return ObjC.unwrap($.NSHomeDirectory())+"/Library/Caches/neetss-notify.json"; }
function loadState(){ try{ _stTxt=readText(statePath())||"{}"; return JSON.parse(_stTxt); }catch(e){ return {}; } }
var _stTxt=null;
function saveState(s){ var j=JSON.stringify(s); if(j!==_stTxt){ writeText(statePath(),j); _stTxt=j; } }
function notify(msgs){ if(!msgs.length) return; try{ var app=Application.currentApplication(); app.includeStandardAdditions=true;
  msgs.forEach(function(m){ app.displayNotification(m.body,{withTitle:"NEET SS",subtitle:m.title,soundName:"Glass"}); }); }catch(e){} }
function run(argv){
  var self=argv[0]||"", info={url:"https://script.google.com/macros/s/AKfycbxJugNolxK03kTtyN_tRkYQI930QMcjd7_j5J-XZI60MQIElikv_n8H-pxbq3_FRC5M/exec",self:self}, f=findFile();
  if(argv[1]==="act" && argv[2]==="notif"){ var s0=loadState(); s0.off=!s0.off; saveState(s0); return ""; }
  if(argv[1]==="act"){
    if(!f) return "";
    var D; try{ D=JSON.parse(f.txt); }catch(e){ return ""; }
    var arg=argv[3]&&argv[3]!=="x"?neetUnhex(argv[3]):null;
    if(argv[2]==="own"){ try{ var app=Application.currentApplication(); app.includeStandardAdditions=true; app.activate();
      var r=app.displayDialog("What are you studying?",{defaultAnswer:"Harrison: ",buttons:["Cancel","Start"],defaultButton:"Start",cancelButton:"Cancel",withTitle:"NEET SS · Own study"}); arg=r.textReturned; }catch(e){ return ""; } }
    if(neetAct(D,argv[2],arg,Date.now())) writeText(f.path,JSON.stringify(D));
    return "";
  }
  if(!f){ info.err="Couldn't find neet-ss-tracker-progress.json in Google Drive. Is Google Drive for desktop running and signed in as dr.sadananth@gmail.com?"; return neetRender(null,info); }
  var D2; try{ D2=JSON.parse(f.txt); }catch(e){ info.err="The progress file is being synced. Try again in a moment."; return neetRender(null,info); }
  try{ var c=neetCore(D2,Date.now()), st=loadState(); info.notifOff=!!st.off;
    try{ var nres=neetNotify(c,Date.now(),st); notify(nres.msgs); saveState(nres.state); }catch(e){}
    return neetRender(c,info); }catch(e){ info.err="Error: "+e; return neetRender(null,info); }
}
JXA

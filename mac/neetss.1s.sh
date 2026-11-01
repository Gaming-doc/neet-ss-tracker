#!/bin/bash
# <xbar.title>NEET SS study timer</xbar.title>
# <xbar.desc>Live studied / awake / break time from the NEET SS tracker (reads the progress file Google Drive syncs to this Mac).</xbar.desc>
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
# <swiftbar.hideRunInTerminal>true</swiftbar.hideRunInTerminal>
# <swiftbar.hideLastUpdated>true</swiftbar.hideLastUpdated>
# <swiftbar.hideDisablePlugin>true</swiftbar.hideDisablePlugin>
# <swiftbar.hideSwiftBar>false</swiftbar.hideSwiftBar>
/usr/bin/osascript -l JavaScript <<'JXA'
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
  var iv=[], ivMs=[];
  for(var id in actual){ var a=actual[id]; if(!a||!a.s||dayOf(a.s)!==T) continue;
    var end=a.e||nowIso, cur=a.s;
    pauses(a).slice().sort(function(x,y){ return x.f<y.f?-1:1; }).forEach(function(p){ if(p.f>cur){ iv.push([mOf(P(cur)),mOf(P(p.f))]); ivMs.push([P(cur),P(p.f)]); } cur=p.t||end; });
    if(end>cur){ iv.push([mOf(P(cur)),mOf(P(end))]); ivMs.push([P(cur),P(end)]); } }
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
  for(var id2 in actual){ var a2=actual[id2]; if(!a2||!a2.s||a2.e) continue; var name=id2.replace(/^[^:]*:/,"").trim();
    if(isPaused(a2)) paused.push(name); else { var pp2=pauses(a2), act=Math.max(0,(nowMs-P(a2.s))/60000-pp2.reduce(function(s,x){ return s+(P(x.t||nowIso)-P(x.f))/60000; },0)); run={name:name,min:Math.round(act),sec:Math.round(act*60)}; } }
  var rb=null; for(var i=brk.length-1;i>=0;i--){ if(!brk[i].e){ rb=brk[i]; break; } }
  var BRK={lunch:["Lunch",45],dinner:["Dinner",45],series:["Series",30],nap:["Short nap",30],other:["Break",30]};
  var onBrk=rb?{name:rb.k==="other"&&rb.n?rb.n:(BRK[rb.k]||BRK.other)[0],min:Math.round((nowMs-P(rb.s))/60000),sec:Math.round((nowMs-P(rb.s))/1000),max:(BRK[rb.k]||BRK.other)[1]}:null;
  var doneToday=0; for(var k2 in (ext.dt||{})) if(ext.dt[k2]===T) doneToday++;
  return {today:T,awake:awake,studied:studied,breaks:breaks,awakeS:awakeS,studiedS:studiedS,breaksS:breaksS,woke:sl&&sl.w||null,slept:slept,sleeping:!!ext.bed,bedAt:ext.bed||null,run:run,paused:paused,onBreak:onBrk,doneToday:doneToday,updatedAt:D.updatedAt||null};
}


// Turns neetCore() output into SwiftBar/xbar menu text.
function neetRender(c, info){
  function hm(m){ if(m==null) return "–"; m=Math.max(0,Math.round(m)); return Math.floor(m/60)+":"+String(m%60).padStart(2,"0"); }
  function hms(s){ if(s==null) return "–"; s=Math.max(0,Math.round(s)); return Math.floor(s/3600)+":"+String(Math.floor(s/60)%60).padStart(2,"0")+":"+String(s%60).padStart(2,"0"); }
  function long(m){ m=Math.max(0,Math.round(m)); var h=Math.floor(m/60), r=m%60; return h?(h+" h"+(r?" "+r+" min":"")):(r+" min"); }
  function clk(iso){ var d=new Date(Date.parse(iso)+19800000); return String(d.getUTCHours()).padStart(2,"0")+":"+String(d.getUTCMinutes()).padStart(2,"0"); }
  var L=[], F=" | font=Menlo size=13", url=info.url;
  if(!c){ L.push("📖 ? | color=#D9822B"); L.push("---"); L.push(info.err||"Couldn't read the tracker file."); L.push("Open tracker | href="+url); L.push("Refresh | refresh=true"); return L.join("\n"); }
  var awakeTxt=c.awakeS?hms(c.awakeS):"–";
  var title=c.sleeping?"😴 📖 "+hms(c.studiedS):c.onBreak?"☕ "+c.onBreak.name+" "+hms(c.onBreak.sec)+" · 📖 "+hms(c.studiedS):"📖 "+hms(c.studiedS)+" · ☀️ "+awakeTxt;
  var tcol=c.onBreak&&c.onBreak.min>c.onBreak.max?" | color=#D9363E":"";
  L.push(title+tcol+(tcol?" font=Menlo":" | font=Menlo"));
  L.push("---");
  L.push("NEET SS · "+c.today+" | size=12 color=#888888");
  L.push("Studied   "+hms(c.studiedS)+F);
  L.push("Awake     "+(c.awakeS?hms(c.awakeS)+(c.woke?"  (up since "+c.woke+")":""):"– tap I'm up now in the tracker")+F);
  var pct=c.awake?Math.round(100*c.breaks/c.awake):0;
  L.push("Breaks    "+hms(c.breaksS)+(c.awake?"  ("+pct+"% of awake)":"")+F+(c.awake>=120&&pct>30?" color=#D9822B":""));
  if(c.slept!=null) L.push("Slept     "+long(c.slept)+" last night"+F+(c.slept<360?" color=#D9363E":""));
  if(c.awake&&c.studied) L.push("Study ratio "+Math.round(100*c.studied/c.awake)+"% of awake time"+F);
  L.push("---");
  if(c.sleeping) L.push("😴 Sleeping since "+clk(c.bedAt));
  if(c.onBreak) L.push("☕ On "+c.onBreak.name+" · "+long(c.onBreak.min)+" (guide "+c.onBreak.max+" min)"+(c.onBreak.min>c.onBreak.max?" | color=#D9363E":""));
  if(c.run) L.push("▶ "+c.run.name+" · "+hms(c.run.sec)+" on this module"+(c.run.min>=180?"  (still running? end it in the tracker) | color=#D9822B":""));
  c.paused.forEach(function(n){ L.push("⏸ "+n+" (paused)"); });
  if(!c.run&&!c.onBreak&&!c.sleeping) L.push("Nothing running right now | color=#888888");
  L.push("Modules ticked today: "+c.doneToday);
  L.push("---");
  L.push("Open tracker | href="+url);
  if(c.updatedAt) L.push("Last saved "+clk(c.updatedAt)+" | size=11 color=#888888");
  L.push("Refresh | refresh=true");
  return L.join("\n");
}



ObjC.import('Foundation');
function readText(p){ try{ var s=$.NSString.stringWithContentsOfFileEncodingError(p,$.NSUTF8StringEncoding,null); var u=ObjC.unwrap(s); return (typeof u==="string")?u:null; }catch(e){ return null; } }
function listDir(p){ try{ return ObjC.deepUnwrap($.NSFileManager.defaultManager.contentsOfDirectoryAtPathError(p,null))||[]; }catch(e){ return []; } }
function main(){
  var home=ObjC.unwrap($.NSHomeDirectory()), cs=home+"/Library/CloudStorage", F="neet-ss-tracker-progress.json", cands=[];
  listDir(cs).filter(function(n){ return n.indexOf("GoogleDrive")===0; })
    .forEach(function(n){ cands.push(cs+"/"+n+"/My Drive/"+F); listDir(cs+"/"+n).forEach(function(m){ if(m!=="My Drive") cands.push(cs+"/"+n+"/"+m+"/"+F); }); });
  cands.push(home+"/Google Drive/My Drive/"+F);
  var txt=null; for(var i=0;i<cands.length&&!txt;i++) txt=readText(cands[i]);
  var info={url:"https://script.google.com/macros/s/YOUR_DEPLOYMENT_ID/exec"};
  if(!txt){ info.err="Couldn't find "+F+" in Google Drive. Is Google Drive for desktop running and signed in to the Google account that owns the tracker?"; return neetRender(null,info); }
  var D; try{ D=JSON.parse(txt); }catch(e){ info.err="The progress file is being synced. Try again in a moment."; return neetRender(null,info); }
  try{ return neetRender(neetCore(D,Date.now()),info); }catch(e){ info.err="Error: "+e; return neetRender(null,info); }
}
main();
JXA

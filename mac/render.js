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
if(typeof module!=="undefined") module.exports=neetRender;

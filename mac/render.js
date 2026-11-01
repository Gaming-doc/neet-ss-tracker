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
if(typeof module!=="undefined") module.exports=neetRender;

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
if(typeof module!=="undefined") module.exports=neetNotify;

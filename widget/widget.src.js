// NEET SS widget for Scriptable (iPhone Home Screen + Lock Screen).
// Shows studied / awake time, study ratio and the 50% / 75% target, live from your tracker.
const FEED = "__FEED__";
const TRACKER = "__TRACKER__";

__CORE__

const COL = { red: new Color("#D9363E"), orange: new Color("#D9822B"), green: new Color("#1F9D62"), muted: new Color("#8A8FB0"), ink: Color.dynamic(new Color("#1B1E3A"), new Color("#ECEEFB")), bg: Color.dynamic(new Color("#F4F5FB"), new Color("#101225")) };
const fm = FileManager.local(), CACHE = fm.joinPath(fm.cacheDirectory(), "neetss-progress.json");

async function loadData(){
  try{ const r=new Request(FEED); r.timeoutInterval=20; const j=await r.loadJSON(); if(j && !j.error && j.actual){ fm.writeString(CACHE, JSON.stringify(j)); return {d:j, live:true}; } }catch(e){}
  try{ if(fm.fileExists(CACHE)) return {d:JSON.parse(fm.readString(CACHE)), live:false}; }catch(e){}
  return {d:null, live:false};
}
function hms(s){ s=Math.max(0,Math.round(s)); return Math.floor(s/3600)+":"+String(Math.floor(s/60)%60).padStart(2,"0"); }
function ratioColor(r){ return r>=0.75?COL.green:r>=0.5?COL.orange:COL.red; }
function target(c){
  if(!c.awakeS || c.sleeping) return null;
  const r=c.studiedS/c.awakeS;
  if(r>=0.75) return {txt:"Above 75% · "+hms(Math.floor((4*c.studiedS-3*c.awakeS)/3))+" break spare", col:COL.green};
  const t=r<0.5?0.5:0.75, need=Math.ceil((t*c.awakeS-c.studiedS)/(1-t));
  return {txt:"To "+Math.round(t*100)+"%: "+hms(need)+" study", col:ratioColor(r)};
}
function studyClock(stack, c, font, color){
  // ticks live while a module (or own study) is running; static otherwise
  if(c.run && !c.onBreak && !c.sleeping){ const d=stack.addDate(new Date(Date.now()-c.studiedS*1000)); d.applyTimerStyle(); d.font=font; if(color) d.textColor=color; return d; }
  const t=stack.addText(hms(c.studiedS)); t.font=font; if(color) t.textColor=color; return t;
}
function awakeClock(stack, c, font, color){
  if((c.woke||c.awakeS) && !c.sleeping){ const d=stack.addDate(new Date(Date.now()-c.awakeS*1000)); d.applyTimerStyle(); d.font=font; if(color) d.textColor=color; return d; }
  const t=stack.addText(c.sleeping?"asleep":"–"); t.font=font; if(color) t.textColor=color; return t;
}
function nowLine(c){
  if(c.sleeping) return "😴 Sleeping";
  if(c.onBreak) return "☕ "+c.onBreak.name+" "+c.onBreak.min+"m"+(c.onBreak.min>c.onBreak.max?" (over)":"");
  if(c.run) return (c.run.free?"📘 ":"▶ ")+c.run.name;
  if(c.paused.length) return "⏸ "+c.paused[0].name;
  return "Nothing running";
}

function build(c, live){
  const fam = config.widgetFamily || "medium", w = new ListWidget();
  w.url = TRACKER; w.refreshAfterDate = new Date(Date.now()+5*60*1000);
  if(!c){ const t=w.addText(fam.startsWith("accessory")?"NEET SS: no data":"NEET SS\nCouldn't load your tracker yet."); t.font=Font.systemFont(12); return w; }
  const r = c.awakeS ? c.studiedS/c.awakeS : 0, rc = ratioColor(r), pct = c.awakeS?Math.round(r*100)+"%":"–", tg = target(c);
  if(fam==="accessoryInline"){
    w.addText("📖 "+hms(c.studiedS)+" · "+pct+(c.onBreak?" · ☕":c.run?" · ▶":""));
    return w;
  }
  if(fam==="accessoryCircular"){
    w.addAccessoryWidgetBackground = true;
    const t=w.addText(pct); t.font=Font.boldSystemFont(16); t.centerAlignText();
    const l=w.addText("study"); l.font=Font.systemFont(9); l.centerAlignText();
    return w;
  }
  if(fam==="accessoryRectangular"){
    const top=w.addStack(); top.centerAlignContent();
    const a=top.addText("📖 "); a.font=Font.boldSystemFont(13); studyClock(top,c,Font.boldMonospacedSystemFont(13),null);
    const b=top.addText("  "+pct); b.font=Font.boldSystemFont(13);
    const n=w.addText(tg?tg.txt:nowLine(c)); n.font=Font.systemFont(11); n.lineLimit=1;
    const m=w.addText(nowLine(c)); m.font=Font.systemFont(11); m.lineLimit=1; m.textOpacity=0.8;
    return w;
  }
  // Home Screen: small / medium / large
  w.backgroundColor = COL.bg; w.setPadding(12,14,12,14);
  const head=w.addStack(); head.centerAlignContent();
  const h=head.addText("NEET SS"); h.font=Font.boldSystemFont(11); h.textColor=COL.muted;
  head.addSpacer();
  const dot=head.addText(live?"●":"○"); dot.font=Font.systemFont(9); dot.textColor=live?COL.green:COL.muted;
  w.addSpacer(4);
  const row=(label, fn)=>{ const s=w.addStack(); s.centerAlignContent(); const l=s.addText(label); l.font=Font.systemFont(12); l.textColor=COL.muted; s.addSpacer(); fn(s); };
  row("📖 Studied", s=>studyClock(s,c,Font.boldMonospacedSystemFont(fam==="small"?15:17),COL.ink));
  row("☀️ Awake", s=>awakeClock(s,c,Font.regularMonospacedSystemFont(fam==="small"?13:15),COL.ink));
  row("Ratio", s=>{ const t=s.addText(pct); t.font=Font.boldSystemFont(fam==="small"?15:17); t.textColor=rc; });
  w.addSpacer(4);
  if(tg){ const t=w.addText(tg.txt); t.font=Font.semiboldSystemFont(11); t.textColor=tg.col; t.lineLimit=1; t.minimumScaleFactor=0.7; }
  if(fam!=="small"){ const n=w.addText(nowLine(c)); n.font=Font.systemFont(11); n.textColor=COL.ink; n.lineLimit=1; n.minimumScaleFactor=0.7;
    if(c.slept!=null){ const sl=w.addText("Slept "+hms(c.slept*60)+" last night"); sl.font=Font.systemFont(10); sl.textColor=COL.muted; } }
  w.addSpacer();
  return w;
}

const {d, live} = await loadData();
let c=null; try{ c = d ? neetCore(d, Date.now()) : null; }catch(e){ c=null; }
const widget = build(c, live);
if(config.runsInWidget){ Script.setWidget(widget); }
else { await widget.presentMedium(); }
Script.complete();

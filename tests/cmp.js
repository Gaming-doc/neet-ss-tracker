const {chromium,open,fs}=require('./h.js'); const core=require('../mac/core.js');
const IST=(d,hm)=>new Date(`${d}T${hm}:00+05:30`).toISOString();
const real=fs.readFileSync('fixture-progress.json','utf8');
const syn=JSON.stringify({done:{},times:{},actual:{"m:A":{s:IST('2026-11-02','00:30'),p:[{f:IST('2026-11-02','01:00'),t:IST('2026-11-02','01:20')}],e:IST('2026-11-02','02:00')},"m:B":{s:IST('2026-11-02','11:00')}},ext:{sleep:{"2026-11-01":{w:"10:30",b:"04:22"},"2026-11-02":{w:"10:15",b:"02:30"}},bed:null,brk:[{k:"lunch",s:IST('2026-11-02','13:00')}]}});
(async()=>{ const b=await chromium.launch(); let bad=0;
 const cases=[[real,IST('2026-11-01','23:50')],[real,IST('2026-11-02','01:30')],[real,IST('2026-11-02','09:00')],[syn,IST('2026-11-02','01:40')],[syn,IST('2026-11-02','13:20')],[syn,IST('2026-11-02','05:00')]];
 for(const [d,t] of cases){ const pg=await open(b,{file:'sim2.html',time:t,data:d});
  const tr=await pg.evaluate(()=>{ const tl=dayTimeline(TODAY); return {today:TODAY,awake:tl?tl.awake:0,studied:tl?tl.studied:0,breaks:tl?tl.brk:0}; });
  const c=core(JSON.parse(d),Date.parse(t)); const same=tr.today===c.today&&Math.abs(tr.awake-c.awake)<=1&&Math.abs(tr.studied-c.studied)<=1&&Math.abs(tr.breaks-c.breaks)<=1;
  if(!same) bad++; console.log(same?'SAME':'DIFF',t,JSON.stringify(tr),JSON.stringify({today:c.today,awake:c.awake,studied:c.studied,breaks:c.breaks,run:c.run,onBreak:c.onBreak})); await pg.close(); }
 console.log(bad?bad+' differ':'all match'); await b.close(); })();

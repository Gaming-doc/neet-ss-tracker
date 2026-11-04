// A module started on one day, paused overnight and resumed the next day: today's part must count today,
// on the page (dayTimeline) and in the menu bar core (neetCore), and yesterday keeps only yesterday's part.
const {chromium,open,gasSim,fs}=require('./h.js'); const core=require('../mac/core.js');
const IST=(d,hm)=>new Date(`${d}T${hm}:00+05:30`).toISOString();
gasSim(require('path').join(__dirname,'..','dist','NEET SS Tracker app.html'),'sim5.html');
let pass=0,fail=0; const ok=(c,m)=>{ if(c) pass++; else { fail++; console.log('FAIL',m); } };
const D={done:{"m:Neuro: Migraine & Headache":1},times:{},actual:{
  "m:Neuro: Migraine & Headache":{s:IST('2026-11-03','11:45'),e:IST('2026-11-03','12:42')},
  "m:Neuro: Nerve & Muscle P1 (Q1-70)":{s:IST('2026-11-03','14:50'),p:[{f:IST('2026-11-03','21:18'),t:IST('2026-11-04','11:28')}]}},
  ext:{sleep:{"2026-11-03":{w:"07:49",b:"23:19"},"2026-11-04":{w:"10:45",b:"23:26"}},bed:null,brk:[]},updatedAt:IST('2026-11-04','11:28')};
(async()=>{ const b=await chromium.launch();
  for(const [t,expToday,label] of [['12:00',32,'running'],['12:30',62,'still running'],['11:00',0,'before resuming']]){
    const now=IST('2026-11-04',t), pg=await open(b,{file:'sim5.html',time:now,data:JSON.stringify(D)});
    const r=await pg.evaluate(()=>{ const a=dayTimeline(TODAY), y=dayTimeline('2026-11-03'); return {T:TODAY,st:a?a.studied:0,aw:a?a.awake:0,br:a?a.brk:0,y:y?y.studied:0}; });
    const c=core(JSON.parse(JSON.stringify(D)),Date.parse(now));
    ok(r.T==='2026-11-04'&&c.today==='2026-11-04',label+' today '+r.T+' '+c.today);
    ok(Math.abs(r.st-expToday)<=1,label+': page studied today '+r.st+' (want '+expToday+')');
    ok(Math.abs(c.studiedS/60-expToday)<=1,label+': menu bar studied today '+c.studiedS/60+' (want '+expToday+')');
    ok(Math.abs(r.aw-c.awake)<=1&&Math.abs(r.br-c.breaks)<=1,label+': awake/breaks match '+JSON.stringify([r.aw,c.awake,r.br,c.breaks]));
    ok(Math.abs(r.y-(57+388))<=1,label+': yesterday keeps only yesterday '+r.y);
    if(t==='12:00') ok(c.run&&/Nerve & Muscle P1/.test(c.run.name),'menu bar shows it running');
    ok(pg.errs.length===0,'errors '+pg.errs.join('|')); await pg.close(); }
  console.log('pass',pass,'fail',fail); await b.close(); })();

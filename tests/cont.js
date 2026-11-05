// An ended module can be continued: the gap becomes a pause, it runs again, and ending it again works.
const {chromium,open}=require('./h.js'); const path=require('path');
const IST=(d,hm)=>new Date(`${d}T${hm}:00+05:30`).toISOString();
let pass=0,fail=0; const ok=(c,m)=>{ if(c) pass++; else { fail++; console.log('FAIL',m); } };
const id="m:Neuro: Migraine & Headache";
const D={done:{[id]:1},times:{},actual:{[id]:{s:IST('2026-11-04','10:00'),e:IST('2026-11-04','11:00')}},ext:{sleep:{"2026-11-04":{w:"07:00"}},bed:null,brk:[]},updatedAt:IST('2026-11-04','11:00')};
(async()=>{ const b=await chromium.launch();
  const pg=await open(b,{file:path.join(__dirname,'sim5.html'),time:IST('2026-11-04','12:00'),data:JSON.stringify(D)});
  const r=await pg.evaluate(id=>{ const had=actHTML(id).includes('data-act="c"'); act(id,'c'); const a=actual[id];
    return {had,run:!a.e&&!isPaused(a),p:pauses(a).length,m:Math.round(activeM(a)),btn:actHTML(id).includes('data-act="e"')}; },id);
  ok(r.had,'ended card has Continue'); ok(r.run,'running again'); ok(r.p===1,'gap is one pause'); ok(r.m===60,'studied stays 60 min, got '+r.m); ok(r.btn,'End button shows');
  const s=await pg.evaluate(id=>{ actual[id]={s:new Date().toISOString()}; delete done[id]; act(id,'p'); const o="m:other"; actual[o]={s:new Date().toISOString()}; bedNow(); return {a:!!actual[id].e,b:!!actual[o].e,pa:isPaused(actual[id]),pb:isPaused(actual[o])}; },id);
  ok(!s.a&&!s.b,'going to sleep does not end an unfinished module'); ok(s.pa&&s.pb,'both are paused, ready to resume tomorrow');
  ok(pg.errs.length===0,'errors '+pg.errs.join('|'));
  console.log('pass',pass,'fail',fail); await b.close(); })();

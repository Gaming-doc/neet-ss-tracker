// An ended module shows no Continue button, and going to sleep pauses unfinished modules instead of ending them.
const {chromium,open}=require('./h.js'); const path=require('path');
const IST=(d,hm)=>new Date(`${d}T${hm}:00+05:30`).toISOString();
let pass=0,fail=0; const ok=(c,m)=>{ if(c) pass++; else { fail++; console.log('FAIL',m); } };
const id="m:Neuro: Migraine & Headache";
const D={done:{[id]:1},times:{},actual:{[id]:{s:IST('2026-11-04','10:00'),e:IST('2026-11-04','11:00')}},ext:{sleep:{"2026-11-04":{w:"07:00"}},bed:null,brk:[]},updatedAt:IST('2026-11-04','11:00')};
(async()=>{ const b=await chromium.launch();
  const pg=await open(b,{file:path.join(__dirname,'sim5.html'),time:IST('2026-11-04','12:00'),data:JSON.stringify(D)});
  const s=await pg.evaluate(id=>{ const had=actHTML(id).includes('data-act="c"'); const o="m:other", q="m:paused";
    actual[o]={s:new Date().toISOString()}; actual[q]={s:new Date().toISOString()}; act(q,'p'); bedNow();
    return {had,a:!!actual[o].e,b:!!actual[q].e,pa:isPaused(actual[o]),pb:isPaused(actual[q])}; },id);
  ok(!s.had,'ended card has no Continue'); ok(!s.a&&!s.b,'going to sleep does not end an unfinished module'); ok(s.pa&&s.pb,'both stay paused');
  ok(pg.errs.length===0,'errors '+pg.errs.join('|'));
  console.log('pass',pass,'fail',fail); await b.close(); })();

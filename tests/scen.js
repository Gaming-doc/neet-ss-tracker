const {chromium,open,lastSave,localState,fs}=require('./h.js');
const FILE=process.argv[2]||'sim.html', CFILE=process.argv[3]||'claude.html'; const res=[]; const ok=(c,m,x)=>res.push((c?'PASS ':'FAIL ')+m+(c?'':'  -> '+JSON.stringify(x)));
const IST=(d,hm)=>new Date(`${d}T${hm}:00+05:30`).toISOString();
const it=id=>`.item[data-id="${id}"]`;
(async()=>{
 const b=await chromium.launch();
 let pg=await open(b,{file:FILE,time:IST('2026-11-02','09:00')});
 const ev=f=>pg.evaluate(f);
 ok(await ev(()=>TODAY)==='2026-11-02','S1 fresh 09:00 Nov 2 => TODAY Nov 2', await ev(()=>TODAY));
 ok((await pg.textContent('#sheet h2'))==='Neurology II','S1 sheet Neurology II', await pg.textContent('#sheet h2'));
 ok(/Synced|Saved|Ready/.test(await pg.textContent('#sync')),'S1 sync status', await pg.textContent('#sync'));
 // S2 wake
 await pg.click('#coach .sl-act[data-a="wake"]'); await pg.waitForTimeout(100);
 ok(await ev(()=>ext.sleep['2026-11-02']&&ext.sleep['2026-11-02'].w)==='09:00','S2 wake logged 09:00', await ev(()=>ext.sleep));
 // S3 autofill
 const MD='m:Neuro: Movement Disorders', SC='m:Neuro: Spinal Cord', AD='m:Neuro: Alzheimer & Dementia';
 await pg.fill(it(MD)+' .tm-in[data-f="s"]','09:15'); await pg.dispatchEvent(it(MD)+' .tm-in[data-f="s"]','change'); await pg.waitForTimeout(100);
 const T=await ev(()=>times);
 ok(T[MD].e==='13:00'&&T[SC].s==='13:00'&&T[SC].e==='13:30'&&T[AD].s==='13:30'&&T[AD].e==='18:30','S3 autofill 30min/10Q chain', {md:T[MD],sc:T[SC],ad:T[AD]});
 // S4 manual end overrides & refills
 await pg.fill(it(MD)+' .tm-in[data-f="e"]','12:00'); await pg.dispatchEvent(it(MD)+' .tm-in[data-f="e"]','change'); await pg.waitForTimeout(100);
 const T2=await ev(()=>times);
 ok(T2[MD].e==='12:00'&&T2[SC].s==='12:00'&&T2[SC].e==='12:30'&&T2[AD].e==='17:30','S4 manual end re-chains', {md:T2[MD],sc:T2[SC],ad:T2[AD]});
 // S5 start A, pause, start B, end B, resume A, end A
 await pg.click(it(MD)+' .ab[data-act="s"]'); await pg.clock.fastForward(20*60000);
 await pg.click(it(MD)+' .ab[data-act="p"]');
 await pg.click(it(SC)+' .ab[data-act="s"]'); await pg.clock.fastForward(30*60000);
 ok(await ev(()=>isPaused(actual["m:Neuro: Movement Disorders"])),'S5 A stays paused while B runs');
 await pg.click(it(SC)+' .ab[data-act="e"]'); await pg.waitForTimeout(50);
 ok(await ev(()=>!!done["m:Neuro: Spinal Cord"]),'S5 End now marks B done');
 await pg.click(it(MD)+' .ab[data-act="r"]'); await pg.clock.fastForward(10*60000);
 await pg.click(it(MD)+' .ab[data-act="e"]'); await pg.waitForTimeout(50);
 const sp=await ev(()=>{ const a=actual["m:Neuro: Movement Disorders"]; return {act:Math.round(activeM(a)),...pauseSplit(a,"m:Neuro: Movement Disorders")}; });
 ok(sp.act===30 && Math.round(sp.oth)===30 && Math.round(sp.brk)===0,'S5 A studied 30, pause 30 all on other module', sp);
 const tl=await ev(()=>{ const t=dayTimeline(TODAY); return {studied:t.studied,brk:t.brk,awake:t.awake}; });
 ok(tl.studied===60 && tl.brk===0 && tl.awake===60,'S5 timeline studied 60, break 0, awake 60', tl);
 // S6 break via module menu
 await pg.click(it(AD)+' .ab[data-act="s"]'); await pg.clock.fastForward(5*60000);
 await pg.selectOption(it(AD)+' .bk-sel','lunch'); await pg.waitForTimeout(50);
 ok(await ev(()=>isPaused(actual["m:Neuro: Alzheimer & Dementia"])&&runningBrk()&&runningBrk().k==='lunch'),'S6 lunch pauses module');
 await pg.clock.fastForward(50*60000); await pg.waitForTimeout(50);
 ok(/Lunch.*past the 45-minute guide/.test(await pg.textContent('#coach .co-list')),'S6 coach warns lunch over 45', (await pg.textContent('#coach .co-list')).slice(0,200));
 await pg.click(it(AD)+' .ab[data-act="brkEnd"]'); await pg.waitForTimeout(50);
 ok(await ev(()=>!isPaused(actual["m:Neuro: Alzheimer & Dementia"])&&!runningBrk()),'S6 end break resumes module');
 // S7 break auto-ended by starting a module
 await pg.click('#coach .bk[data-k="series"]'); await pg.clock.fastForward(12*60000);
 await pg.click(it('s4:Neuro SS: Dementia')+' .ab[data-act="s"]'); await pg.waitForTimeout(50);
 ok(await ev(()=>!runningBrk() && ext.brk[ext.brk.length-1].k==='series' && !!ext.brk[ext.brk.length-1].e),'S7 starting a module ends the series break');
 ok(await ev(()=>isPaused(actual["m:Neuro: Alzheimer & Dementia"])),'S7 module paused by series stays paused (other module started)');
 // S7b past break add + delete
 await pg.$eval('#coach .brk-past',d=>d.open=true); await pg.selectOption('#coach .bp-k','other'); await pg.fill('#coach .bp-n','Gym'); await pg.fill('#coach .bp-s','07:00'); await pg.fill('#coach .bp-e','07:45'); await pg.click('#coach .bp-add'); await pg.waitForTimeout(50);
 ok(!(await ev(()=>ext.brk.find(x=>x.n==='Gym'))),'S7b break before wake-up rejected');
 await pg.$eval('#coach .brk-past',d=>d.open=true); await pg.fill('#coach .bp-s','10:00'); await pg.fill('#coach .bp-e','10:30'); await pg.click('#coach .bp-add'); await pg.waitForTimeout(50);
 const g=await ev(()=>ext.brk.find(x=>x.n==='Gym'));
 ok(g && g.s===new Date('2026-11-02T10:00:00+05:30').toISOString() && g.e===new Date('2026-11-02T10:30:00+05:30').toISOString(),'S7b past break Gym 10:00-10:30 stored', g);
 ok(await ev(()=>/Gym/.test(brkSummary(TODAY,dayTimeline(TODAY)))),'S7b Gym appears in breakdown', await ev(()=>brkSummary(TODAY,dayTimeline(TODAY))));
 const nb=await ev(()=>ext.brk.length); await pg.$eval('#coach .brk-past',d=>d.open=true); await pg.click('#coach .bp-del >> nth=0'); await pg.waitForTimeout(50);
 ok(await ev(()=>ext.brk.length)===nb-1,'S7b delete past break');
 // S8 bed late, next morning
 await pg.clock.setSystemTime(new Date(IST('2026-11-02','23:30'))); await pg.clock.fastForward(1000);
 await pg.evaluate(()=>renderAll());
 const bedBtn=await pg.$('#coach .sl-act[data-a="bed"]'); ok(!!bedBtn,'S8 Going to sleep button at 23:30');
 if(bedBtn) await bedBtn.click(); await pg.waitForTimeout(50);
 ok(await ev(()=>!!ext.bed && !Object.values(actual).some(a=>a.s&&!a.e&&!isPaused(a))),'S8 bed pauses running modules');
 await pg.clock.setSystemTime(new Date(IST('2026-11-03','01:00'))); await pg.clock.fastForward(31000); await pg.waitForTimeout(50);
 ok(await ev(()=>TODAY)==='2026-11-02','S8 01:00 still Nov 2', await ev(()=>TODAY));
 await pg.clock.setSystemTime(new Date(IST('2026-11-03','08:00'))); await pg.clock.fastForward(31000); await pg.waitForTimeout(50);
 ok(await ev(()=>TODAY)==='2026-11-03','S8 08:00 rolls to Nov 3', await ev(()=>TODAY));
 ok((await pg.textContent('#sheet h2'))==='Neurology III','S8 sheet switched to Neurology III', await pg.textContent('#sheet h2'));
 await pg.click('#coach .sl-act[data-a="wake"]'); await pg.waitForTimeout(50);
 const s3=await ev(()=>({s:ext.sleep['2026-11-03'],d:sleepOf('2026-11-03')}));
 ok(s3.s&&s3.s.b==='23:30'&&s3.s.w==='08:00'&&s3.d.dur===510,'S8 sleep 23:30->08:00 = 8h30', s3);
 const tl2=await ev(()=>{ const t=dayTimeline('2026-11-02'); return {bed:t.bed,end:t.end}; });
 ok(tl2.bed===1410,'S8 Nov 2 timeline bed 23:30', tl2);
 // S9 move + untick
 const MH='m:Neuro: Migraine & Headache';
 await pg.selectOption(it(MH)+' .mv', {index:1}); await pg.waitForTimeout(50);
 ok(await ev(()=>!!ext.moved["m:Neuro: Migraine & Headache"]),'S9 move to next day', await ev(()=>ext.moved));
 // tick/untick toggle on a module
 await pg.click(it('m:Neuro: ALS & MND')+' .tick'); ok(await ev(()=>!!done['m:Neuro: ALS & MND'] && ext.dt['m:Neuro: ALS & MND']==='2026-11-03'),'S9 tick sets dt');
 await pg.click(it('m:Neuro: ALS & MND')+' .tick'); ok(await ev(()=>!done['m:Neuro: ALS & MND'] && !ext.dt['m:Neuro: ALS & MND']),'S9 untick clears');
 // S10 accuracy clamp
 await pg.click(it('m:Neuro: ALS & MND')+' .tick');
 await pg.fill(it('m:Neuro: ALS & MND')+' .acc-in','150'); await pg.dispatchEvent(it('m:Neuro: ALS & MND')+' .acc-in','change'); await pg.waitForTimeout(50);
 ok(await ev(()=>ext.acc['m:Neuro: ALS & MND'])===100,'S10 accuracy clamps to Q count', await ev(()=>ext.acc));
 // S11 saves to GAS contain everything
 await pg.clock.fastForward(2000); await pg.waitForTimeout(100);
 const sv=await lastSave(pg);
 ok(sv && sv.ext && Array.isArray(sv.ext.brk) && sv.ext.sleep['2026-11-03'] && sv.done['m:Neuro: ALS & MND'],'S11 GAS save payload complete', sv&&Object.keys(sv.ext));
 const ls=await localState(pg);
 ok(pg.errs.length===0,'S-all no page errors (session 1)', pg.errs);
 await pg.close();
 // S11b reload offline (GAS fails) keeps local
 pg=await open(b,{file:FILE,time:IST('2026-11-03','09:00'),local:ls}); await pg.evaluate(()=>{});
 ok(await pg.evaluate(()=>!!done['m:Neuro: ALS & MND'] && ext.brk.length>0),'S11b reload keeps local state');
 ok(pg.errs.length===0,'S11b no errors', pg.errs); await pg.close();
 // S12 old data shapes
 const old=JSON.stringify({done:{"m:Neuro: CVA":1},times:{},actual:{"m:Neuro: CVA":{s:"2026-11-01T06:00:00Z",p:[{f:"2026-11-01T06:10:00Z"}]}}});
 pg=await open(b,{file:FILE,time:IST('2026-11-01','20:00'),data:old});
 ok(pg.errs.length===0 && await pg.evaluate(()=>Array.isArray(ext.brk)&&typeof ext.sleep==='object'),'S12 old data without ext loads', pg.errs); await pg.close();
 const weird=JSON.stringify({done:{},times:{"bogus":{s:"25:99"}},actual:{"nope:id":{s:"2026-11-01T06:00:00Z"}},ext:{acc:{"nope":5},moved:{"m:Neuro: CVA":"p9:99"},sleep:{"2026-11-01":{w:"10:00"}},brk:[{k:"weird",s:"2026-11-01T07:00:00Z"}]}});
 pg=await open(b,{file:FILE,time:IST('2026-11-01','20:00'),data:weird});
 for(const tb of ['p1','p2','hy','mar','stats','clock']){ await pg.click('#tab-'+tb); }
 ok(pg.errs.length===0,'S12b junk/unknown ids + unknown break type load without errors', pg.errs); await pg.close();
 // S13 Claude mode
 pg=await open(b,{mode:'claude',file:CFILE,time:IST('2026-11-01','20:00'),data:fs.readFileSync('fixture-progress.json','utf8')});
 ok(/Synced/.test(await pg.textContent('#sync')),'S13 claude db sync', await pg.textContent('#sync'));
 await pg.click('#coach .bk[data-k="dinner"]'); await pg.clock.fastForward(2000); await pg.waitForTimeout(50);
 const cs=await lastSave(pg); ok(cs && cs.ext && cs.ext.brk && cs.ext.brk.length===1,'S13 claude save has brk', cs&&cs.ext);
 const ai=await pg.$('.co-ai-btn'); ok(!!ai,'S13 Ask Claude button present'); if(ai){ await ai.click(); await pg.waitForTimeout(100); ok(/AI says hi/.test(await pg.textContent('.co-ai-out')),'S13 Ask Claude output'); }
 ok(pg.errs.length===0,'S13 no errors', pg.errs); await pg.close();
 // S14 Gemini button (gas)
 pg=await open(b,{file:FILE,time:IST('2026-11-01','20:00'),data:fs.readFileSync('fixture-progress.json','utf8')});
 const gem=await pg.$('.co-gem'); ok(!!gem,'S14 Gemini button present');
 if(gem){ await pg.evaluate(()=>{ document.querySelector('.co-gem').addEventListener('click',e=>e.preventDefault()); }); await gem.click(); await pg.waitForTimeout(100); const n=await pg.textContent('.co-gem-note'); ok(/Copied|Couldn't copy/.test(n),'S14 Gemini note shown', n); const ta=await pg.$eval('.co-gem-txt textarea',t=>t.value.length); ok(ta>300,'S14 summary text filled', ta); }
 ok(pg.errs.length===0,'S14 no errors', pg.errs); await pg.close();
 // S16 stale paused module overnight must not block rollover; S17 module left running overnight
 const stale=JSON.stringify({done:{},times:{},actual:{"s3:Neuro SS: Stroke":{s:IST('2026-11-01','23:37'),p:[{f:IST('2026-11-01','23:50')}]}},ext:{sleep:{"2026-11-01":{w:"10:30"}}}});
 pg=await open(b,{file:FILE,time:IST('2026-11-02','09:00'),data:stale});
 ok(await pg.evaluate(()=>TODAY)==='2026-11-02','S16 paused-since-23:50 module: 09:00 rolls to Nov 2', await pg.evaluate(()=>TODAY)); await pg.close();
 const left=JSON.stringify({done:{},times:{},actual:{"s3:Neuro SS: Stroke":{s:IST('2026-11-01','23:37')}},ext:{sleep:{"2026-11-01":{w:"10:30"}}}});
 pg=await open(b,{file:FILE,time:IST('2026-11-02','09:00'),data:left});
 ok(await pg.evaluate(()=>TODAY)==='2026-11-02','S17 module left running since 23:37: 09:00 rolls to Nov 2', await pg.evaluate(()=>TODAY)); await pg.close();
 const allnight=JSON.stringify({done:{},times:{},actual:{"s3:Neuro SS: Stroke":{s:IST('2026-11-02','05:30')}},ext:{sleep:{"2026-11-01":{w:"10:30"}}}});
 pg=await open(b,{file:FILE,time:IST('2026-11-02','06:30'),data:allnight});
 ok(await pg.evaluate(()=>TODAY)==='2026-11-01','S18 all-nighter (module started 05:30, still running at 06:30) stays Nov 1', await pg.evaluate(()=>TODAY)); await pg.close();
 // S15 gas load failure message
 pg=await b.newPage(); await pg.addInitScript(()=>{ window.__gasFail=1; }); await pg.close();
 console.log(res.join('\n')); console.log('\n'+res.filter(r=>r.startsWith('FAIL')).length+' failures of '+res.length);
 await b.close();
})();

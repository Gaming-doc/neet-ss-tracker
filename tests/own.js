const {chromium,open,lastSave,fs}=require('./h.js');
const res=[]; const ok=(c,m,x)=>res.push((c?'PASS ':'FAIL ')+m+(c?'':'  -> '+JSON.stringify(x)));
const IST=(d,hm)=>new Date(`${d}T${hm}:00+05:30`).toISOString();
(async()=>{ const b=await chromium.launch();
 for(const w of [1300,380]){
 const pg=await open(b,{file:'sim4.html',time:IST('2026-11-02','10:00'),width:w,data:JSON.stringify({done:{},times:{},actual:{},ext:{sleep:{"2026-11-02":{w:"09:00",b:"01:00"}}}})});
 ok(!!await pg.$('#ownStudy .own-name'),w+' own-study form shown today');
 const MD='m:Neuro: Movement Disorders';
 await pg.click(`.item[data-id="${MD}"] .ab[data-act="s"]`); await pg.clock.fastForward(20*60000);
 await pg.fill('#ownStudy .own-name','Harrison ch. 435 Parkinson disease'); await pg.selectOption('#ownStudy .own-kind','read'); await pg.click('#ownStudy .own-go'); await pg.waitForTimeout(80);
 const id=await pg.evaluate(()=>Object.keys(ext.free)[0]);
 ok(id&&id.startsWith('x:'),w+' own session created',id);
 ok(await pg.evaluate(m=>isPaused(actual[m]),MD),w+' running module paused by own study');
 ok(/Own study: Harrison ch. 435/.test(await pg.textContent('#coachPop')),w+' coach pop for own study', (await pg.textContent('#coachPop')).slice(0,120));
 await pg.clock.fastForward(30*60000); await pg.waitForTimeout(50);
 const q=`.item[data-id="${id}"]`;
 await pg.click(q+' .ab[data-act="p"]'); await pg.clock.fastForward(5*60000);
 await pg.click(q+' .ab[data-act="r"]'); await pg.clock.fastForward(10*60000);
 await pg.click(q+' .ab[data-act="e"]'); await pg.waitForTimeout(50);
 const st=await pg.evaluate(id=>({act:Math.round(activeM(actual[id])),done:!!done[id],dt:!!ext.dt[id],tl:(()=>{const t=dayTimeline(TODAY); return {studied:t.studied,brk:t.brk,kinds:t.iv.map(x=>x.k)};})()}),id);
 ok(st.act===40 && !st.done && !st.dt,w+' own study 40 min, not ticked', st);
 ok(st.tl.studied===60 && st.tl.kinds.includes('free'),w+' timeline: 20 module + 40 own = 60 studied, free segment', st.tl);
 ok(/Own study logged/.test(await pg.textContent('#coachPop')),w+' end pop');
 ok(/40 min today/.test(await pg.textContent('#ownStudy')),w+' own-study total shown', await pg.textContent('#ownStudy .block-h'));
 // starting a module ends own study? start new own then module resume
 await pg.fill('#ownStudy .own-name',''); await pg.click('#ownStudy .own-go'); await pg.waitForTimeout(50);
 const id2=await pg.evaluate(()=>Object.keys(ext.free)[1]); ok(await pg.evaluate(id=>ext.free[id].n,id2)==='Harrison reading',w+' empty name uses kind label', await pg.evaluate(id=>ext.free[id],id2));
 await pg.clock.fastForward(5*60000); await pg.click(`.item[data-id="${MD}"] .ab[data-act="r"]`); await pg.waitForTimeout(50);
 ok(await pg.evaluate(id=>isPaused(actual[id]),id2),w+' resuming module pauses own study');
 await pg.click(`.item[data-id="${id2}"] .ab[data-act="x"]`); await pg.waitForTimeout(50);
 ok(await pg.evaluate(id=>!ext.free[id]&&!actual[id],id2),w+' × deletes own session');
 await pg.clock.fastForward(2000); const sv=await lastSave(pg); ok(sv&&sv.ext.free&&sv.ext.free[id],w+' saved to Drive payload');
 // break while on own study
 await pg.fill('#ownStudy .own-name','Notes cardio'); await pg.selectOption('#ownStudy .own-kind','notes'); await pg.click('#ownStudy .own-go'); await pg.waitForTimeout(50);
 const id3=await pg.evaluate(()=>Object.keys(ext.free).find(k=>ext.free[k].n==='Notes cardio'));
 await pg.selectOption(`.item[data-id="${id3}"] .bk-sel`,'lunch'); await pg.waitForTimeout(50);
 ok(await pg.evaluate(id=>isPaused(actual[id])&&runningBrk().pid===id,id3),w+' break from own study pauses it');
 const ov=await pg.evaluate(()=>document.documentElement.scrollWidth-innerWidth); ok(ov<=2,w+' no overflow',ov);
 await (await pg.$('#ownStudy')).screenshot({path:`own_${w}.png`});
 // reload: own sessions persist & show
 ok(pg.errs.length===0,w+' no errors',pg.errs); await pg.close(); }
 console.log(res.join('\n')); console.log(res.filter(r=>r.startsWith('FAIL')).length+' failures'); await b.close(); })();

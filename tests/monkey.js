const {chromium,gasSim,open,fs}=require('./h.js');
const real=fs.readFileSync('fixture-progress.json','utf8');
const TIMES={pre:'2026-10-28T06:00:00Z',day3:'2026-11-01T08:00:00Z',night:'2026-11-01T20:00:00Z',p2:'2026-11-30T06:00:00Z',post:'2026-12-12T06:00:00Z'};
(async()=>{
  const b=await chromium.launch(); const report=[];
  const files={gas:'sim2.html',claude:'claude2.html'};
  const COMBOS=[['gas','real','day3',1300],['gas','real','day3',380],['gas','real','night',1300],['gas','empty','pre',1300],['gas','real','p2',380],['gas','empty','post',1300],['claude','real','night',1300]];
  for(const [mode,dk,tk,w] of COMBOS){ const time=TIMES[tk];
    const pg=await open(b,{mode,file:files[mode],data:dk==='real'?real:null,time,width:w});
    const tag=`${mode}/${dk}/${tk}/${w}`;
    for(const tabn of ['p1','p2','hy','mar','stats','clock','p1']){
      await pg.click(`#tab-${tabn}`).catch(e=>pg.errs.push('tabclick '+tabn));
      await pg.waitForTimeout(80);
      const ov=await pg.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
      if(ov>2) pg.errs.push(`OVERFLOW ${ov}px on tab ${tabn}`);
      // open all details
      await pg.$$eval('details',ds=>ds.forEach(d=>d.open=true));
      let clicks=0;
      for(let round=0;round<2;round++){
        const n=await pg.$$eval('#planView button, #hyView button, #marView button, #statsView button, #clockView button, #coach button',x=>x.length);
        for(let k=0;k<n && clicks<30;k++){
          const els=await pg.$$('#planView button, #hyView button, #marView button, #statsView button, #clockView button, #coach button'); const el=els[k]; if(!el) break;
          const vis=await el.isVisible().catch(()=>false); if(!vis) continue;
          const txt=(await el.textContent()||'').trim(); if(/Send to Gemini/.test(txt)) continue;
          await el.click({timeout:1500}).catch(()=>{}); clicks++; await pg.clock.fastForward(7*60000); await pg.waitForTimeout(15);
          const ov2=await pg.evaluate(()=>document.documentElement.scrollWidth-innerWidth); if(ov2>2) { pg.errs.push(`OVERFLOW ${ov2}px after "${txt.slice(0,30)}" tab ${tabn}`); }
        }
        const sels=await pg.$$('#planView select, #coach select, #statsView select');
        for(const s of sels.slice(0,6)){ if(!(await s.isVisible().catch(()=>false))) continue; const opts=await s.$$eval('option',o=>o.map(x=>x.value).filter(Boolean)); if(opts.length) await s.selectOption(opts[Math.min(1,opts.length-1)]).catch(()=>{}); await pg.waitForTimeout(15); }
        const ins=await pg.$$('#planView input[type=number], #statsView input[type=number], #planView .acc-in');
        for(const s of ins.slice(0,6)){ if(!(await s.isVisible().catch(()=>false))) continue; await s.fill(String(Math.floor(Math.random()*40))).catch(()=>{}); await s.dispatchEvent('change').catch(()=>{}); }
        const tms=await pg.$$('#planView input[type=time]');
        for(const s of tms.slice(0,6)){ if(!(await s.isVisible().catch(()=>false))) continue; await s.fill(['09:00','13:30','23:40','00:30'][Math.floor(Math.random()*4)]).catch(()=>{}); await s.dispatchEvent('change').catch(()=>{}); }
      }
      await pg.clock.fastForward(31000); await pg.waitForTimeout(30);
    }
    // reload persistence check
    const st=await pg.evaluate(()=>({done:Object.keys(done).length,ext:JSON.stringify(ext).length}));
    console.log(`${tag}: ${pg.errs.length?'ERRORS\n  '+[...new Set(pg.errs)].slice(0,8).join('\n  '):'ok'} (done ${st.done})`);
    await pg.close();
  }
  console.log(report.join('\n')); await b.close();
})();

const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{ const b=await chromium.launch(); const p=await (await b.newContext({viewport:{width:1440,height:900}})).newPage();
 const css=fs.readFileSync('/tmp/site/style.css','utf8').replace(/\/\*[\s\S]*?\*\//g,m=>m.replace(/[^\n]/g,' '));
 // sélecteurs avec leur ligne
 const sels=[]; let depth=0, buf='', line=1, start=1;
 for (const ch of css){ if(ch==='\n')line++; if(ch==='{'){ const s=buf.trim(); if(!s.startsWith('@')&&!/^\d+%|from|to/.test(s)) sels.push({s,line:start}); buf=''; depth++; } else if(ch==='}'){ buf=''; depth--; start=line;} else if(ch===';'){buf=''; start=line;} else { if(!buf.trim()) start=line; buf+=ch; } }
 const used=new Map(sels.map(x=>[x.s+'@'+x.line,false]));
 for (const pg of ['','fonctionnalites/','guides/','versions/','confidentialite/']){
  await p.goto('https://gildasfremont.github.io/callrecorder/'+pg,{waitUntil:'networkidle'});
  const r=await p.evaluate(list=>list.map(x=>x.s.split(',').some(s=>{ s=s.replace(/::?(before|after|hover|focus-visible|focus|active|-webkit-details-marker|disabled)\b/g,'').replace(/:has\([^)]*\)/,'').trim()||'*'; try{return !!document.querySelector(s);}catch(e){return true;} })),sels);
  r.forEach((u,i)=>{ if(u) used.set(sels[i].s+'@'+sels[i].line,true); });
 }
 const dead=sels.filter(x=>!used.get(x.s+'@'+x.line));
 fs.writeFileSync(process.argv[2]+'/css-mort.csv','selecteur,ligne\n'+dead.map(d=>'"'+d.s.replace(/"/g,'""')+'",'+d.line).join('\n'));
 console.log('règles',sels.length,'mortes',dead.length); console.log(dead.map(d=>d.line+' '+d.s).join('\n'));
 // sommaire sous la barre
 await p.goto('https://gildasfremont.github.io/callrecorder/fonctionnalites/',{waitUntil:'networkidle'});
 await p.mouse.wheel(0,2500); await p.waitForTimeout(500); await p.mouse.wheel(0,-300); await p.waitForTimeout(600);
 const o=await p.evaluate(()=>{const n=document.querySelector('.nav').getBoundingClientRect(); const t=document.querySelector('.toc nav').getBoundingClientRect(); const a=document.querySelector('.toc a').getBoundingClientRect(); return {nav_bas:n.bottom,toc_haut:t.top,premier_lien:[a.top,a.bottom], cache:!document.querySelector('.nav').classList.contains('hidden')};});
 console.log(JSON.stringify(o)); await p.screenshot({path:'/tmp/claude-0/ev-toc.png',clip:{x:150,y:0,width:700,height:330}});
 await b.close();})();

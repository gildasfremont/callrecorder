const { chromium } = require('playwright'); const fs=require('fs');
const axeSrc = fs.readFileSync(require.resolve('axe-core/axe.min.js'),'utf8');
(async()=>{ const b=await chromium.launch(); const out=[];
for (const w of [375,1440]) { const p=await (await b.newContext({viewport:{width:w,height:900}})).newPage();
 for (const pg of (process.env.PAGES?process.env.PAGES.split(','):['','fonctionnalites/','guides/','versions/','confidentialite/'])) {
  await p.goto((process.env.BASE||'https://gildasfremont.github.io/callrecorder/')+pg,{waitUntil:'networkidle'});
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=800){scrollTo(0,y);await new Promise(r=>setTimeout(r,30));}});
  if(pg.startsWith('guides')) await p.evaluate(()=>document.querySelectorAll('details').forEach(d=>d.open=true));
  await p.addScriptTag({content:axeSrc});
  const r=await p.evaluate(async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa','best-practice']}}));
  for (const v of r.violations) out.push({page:pg.replace('/','').replace('.html','')||'accueil',largeur:w,regle:v.id,impact:v.impact,aide:v.help,url_regle:v.helpUrl,noeuds:v.nodes.length,exemples:v.nodes.slice(0,4).map(n=>({cible:n.target.join(' '),resume:n.failureSummary.replace(/\s+/g,' ').slice(0,220)}))});
  console.log(w,pg,r.violations.map(v=>v.id+':'+v.nodes.length).join(' '), 'passes', r.passes.length, 'incomplete', r.incomplete.map(v=>v.id+':'+v.nodes.length).join(' '));
 }}
fs.writeFileSync(process.argv[2]+'/'+(process.env.NOM||'axe')+'.json',JSON.stringify(out,null,1)); await b.close();})();

const {open,close}=require('./lib');
(async()=>{
for(const [u,re] of [['https://linear.app/pricing','month|year|annual'],['https://www.notion.com/fr/pricing','mensuel|annuel'],['https://linear.app','^(Plan|Build|Diffs|Monitor|Intake)']]){
 const {p,ctx}=await open(u);
 const r=await p.evaluate((re)=>[...document.querySelectorAll('button,a,label,[role]')].filter(e=>new RegExp(re,'i').test((e.innerText||'').trim())&&(e.innerText||'').length<40).map(e=>{const r=e.getBoundingClientRect();return [e.tagName,e.getAttribute('role'),e.className.toString().slice(0,50),(e.innerText||'').trim(),Math.round(r.width),Math.round(r.height),[...e.attributes].filter(a=>a.name.startsWith('aria')||a.name.startsWith('data')).map(a=>a.name+'='+a.value).join(' ')]}).slice(0,10),re);
 console.log(u,JSON.stringify(r,null,0));await ctx.close();}
await close();})();

const {open,close}=require('./lib');
(async()=>{
for(const u of process.argv.slice(2)){
 const {p,ctx}=await open(u,{width:375,height:812,wait:3000});
 for(let i=0;i<6;i++){await p.mouse.wheel(0,800);await p.waitForTimeout(400);} await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(800);
 const r=await p.evaluate(()=>{const els=[...document.querySelectorAll('img,svg,picture,[style*=background-image]')].map(e=>{const r=e.getBoundingClientRect();return {w:Math.round(r.width),h:Math.round(r.height),y:Math.round(r.top+scrollY),x:Math.round(r.left),src:(e.currentSrc||e.getAttribute('src')||e.tagName).slice(-40),alt:e.getAttribute('alt')}}).filter(o=>o.w>=20&&o.w<=140&&Math.abs(o.w-o.h)<=4);
  const rows={};els.forEach(o=>{(rows[o.y]=rows[o.y]||[]).push(o)});
  return Object.entries(rows).filter(([y,a])=>a.length>=2).slice(0,12).map(([y,a])=>[y,a.length,a.map(o=>o.w+'@'+o.x).join(' '),a[0].src,a[0].alt]);});
 console.log(u);r.forEach(x=>console.log('  ',JSON.stringify(x)));await ctx.close();}
await close();})();

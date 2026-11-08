const {open,close}=require('./lib');
(async()=>{
for(const u of process.argv.slice(2)){
 const {p,ctx}=await open(u,{width:375,height:812,wait:3000});
 for(let i=0;i<8;i++){await p.mouse.wheel(0,700);await p.waitForTimeout(300);}
 const r=await p.evaluate(()=>{const els=[...document.querySelectorAll('img,svg,canvas,video')].map(e=>{const r=e.getBoundingClientRect();return {e,w:Math.round(r.width),h:Math.round(r.height),y:Math.round(r.top+scrollY),x:Math.round(r.left)}}).filter(o=>o.w>=20&&o.w<=150&&Math.abs(o.w-o.h)<=6&&o.x>=0&&o.x<375);
  const hist={};els.forEach(o=>hist[o.w]=(hist[o.w]||0)+1);
  const top=Object.entries(hist).sort((a,b)=>b[1]-a[1]).slice(0,4);
  const W=+top[0][0];const sel=els.filter(o=>o.w===W).sort((a,b)=>a.y-b.y);
  const rows=[];sel.forEach(o=>{const r=rows.find(r=>Math.abs(r.y-o.y)<8);r?r.n.push(o.x):rows.push({y:o.y,n:[o.x]})});
  const ex=sel[2]||sel[0];let card=ex.e;for(let i=0;i<4;i++)card=card.parentElement;
  return {hist:top,rows:rows.slice(0,6).map(r=>r.n.length+'@y'+r.y+' x:'+r.n.join(',')),exAlt:ex.e.getAttribute('alt'),cardText:card.innerText.slice(0,120).replace(/\n/g,' | ')};});
 console.log(u,JSON.stringify(r,null,1));await ctx.close();}
await close();})();

const {open,close,OUT}=require('./lib');const fs=require('fs');const res=[];
(async()=>{
for(const spec of process.argv.slice(2)){const [n,u]=spec.split('|');
 const {p,ctx}=await open(u,{width:1440,height:900,wait:2500});
 for(let i=0;i<8;i++){await p.mouse.wheel(0,900);await p.waitForTimeout(400);}
 await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(500);
 const r=await p.evaluate(()=>{
  const imgs=[...document.querySelectorAll('main img, article img, img, video')].map(e=>{const r=e.getBoundingClientRect();return {tag:e.tagName,w:Math.round(r.width),h:Math.round(r.height),nw:e.naturalWidth||e.videoWidth||0,nh:e.naturalHeight||e.videoHeight||0,x:Math.round(r.left),y:Math.round(r.top+scrollY),src:(e.currentSrc||e.src||e.poster||'').split('?')[0].slice(-50)}}).filter(o=>o.w>=300&&o.y>100).slice(0,12);
  return imgs;});
 const ws=r.map(o=>o.w);const xs=r.map(o=>o.x);
 res.push({site:n,url:u,images:r});console.log(n);r.forEach(o=>console.log('  ',JSON.stringify(o)));
 // capture: first 2 images region? capture each of first 3 images scaled later
 await p.evaluate(()=>{document.querySelectorAll('*').forEach(e=>{const c=getComputedStyle(e);if((c.position==='fixed'||c.position==='sticky')&&e.getBoundingClientRect().top<150&&e.getBoundingClientRect().height<200)e.style.visibility='hidden'})});
 for(let k=0;k<Math.min(2,r.length);k++){const o=r[k];await p.evaluate(y=>scrollTo(0,y-40),o.y);await p.waitForTimeout(900);await p.evaluate(()=>{document.querySelectorAll('*').forEach(e=>{const c=getComputedStyle(e);if((c.position==='fixed'||c.position==='sticky')&&e.getBoundingClientRect().top<150&&e.getBoundingClientRect().height<200)e.style.visibility='hidden'})});const sy=await p.evaluate(()=>scrollY);
  await p.screenshot({path:OUT+`${n}-changelog-${k+1}-1440.png`,clip:{x:Math.max(0,o.x-8),y:Math.max(0,o.y-sy-8),width:Math.min(1440-Math.max(0,o.x-8),o.w+16),height:Math.min(860,o.h+16)}});}
 await ctx.close();}
fs.writeFileSync('q7.json',JSON.stringify(res,null,1));await close();})();

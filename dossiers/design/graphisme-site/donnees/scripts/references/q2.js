const {open,shot,close}=require('./lib');const fs=require('fs');
const sites=[['apple','https://www.apple.com/fr/macos/'],['raycast','https://www.raycast.com'],['linear','https://linear.app'],['things','https://culturedcode.com/things/'],['notion','https://www.notion.com/fr']];
const res=[];
(async()=>{
for(const [n,u] of sites){
 const {p,ctx}=await open(u);
 await p.mouse.click(5,5).catch(()=>{}); // focus document
 await p.evaluate(()=>{document.activeElement&&document.activeElement.blur&&document.activeElement.blur();window.scrollTo(0,0)});
 const items=[];let captured=false;
 for(let i=0;i<6;i++){
  await p.keyboard.press('Tab');await p.waitForTimeout(350);
  const info=await p.evaluate(()=>{const e=document.activeElement;if(!e||e===document.body)return null;const c=getComputedStyle(e);const r=e.getBoundingClientRect();
   return {tag:e.tagName,text:(e.innerText||e.getAttribute('aria-label')||'').trim().slice(0,40),focusVisible:e.matches(':focus-visible'),outlineStyle:c.outlineStyle,outlineColor:c.outlineColor,outlineWidth:c.outlineWidth,outlineOffset:c.outlineOffset,boxShadow:c.boxShadow,borderRadius:c.borderRadius,visible:r.width>0&&r.top>=0&&r.top<innerHeight,x:r.x,y:r.y,w:r.width,h:r.height}});
  items.push(info);
  if(info&&info.visible&&!captured&&(info.outlineStyle!=='none'||info.boxShadow!=='none')&&info.w>10){
    await p.evaluate(()=>{window.__tag=document.activeElement;document.activeElement.setAttribute('data-focus-cap','1')});
    const el=p.locator('[data-focus-cap]');const bb=await el.boundingBox();
    if(bb){const pad=14;await p.screenshot({path:require('./lib').OUT+`${n}-focus-1440.png`,clip:{x:Math.max(0,bb.x-pad),y:Math.max(0,bb.y-pad),width:bb.width+2*pad,height:bb.height+2*pad}});captured=`${n}-focus-1440.png`;}
  }
 }
 res.push({site:n,url:u,items,capture:captured||null});
 console.log(n,captured);items.forEach(x=>console.log('  ',JSON.stringify(x)));
 await ctx.close();
}
fs.writeFileSync('q2.json',JSON.stringify(res,null,1));await close();})();

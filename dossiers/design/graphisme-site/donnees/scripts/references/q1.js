const {open,shot,close}=require('./lib');const fs=require('fs');
const sites=[['brew','https://brew.sh','.install-command pre','.install-command','.install-command button'],
['rustup','https://rustup.rs','pre.rustup-command:visible','.copy-container:visible','.copy-container:visible button'],
['tailscale','https://tailscale.com/download/linux','code.whitespace-pre','code.whitespace-pre >> xpath=..','button[aria-label=copy]']];
const res=[];
(async()=>{
for(const [n,u,cs,boxs,bs] of sites) for(const w of [375,1440]){
 const {p,ctx}=await open(u,{width:w});
 const code=p.locator(cs).first(); const btn=p.locator(bs).first();
 await p.mouse.move(0,0);
 const m=await code.evaluate(e=>{const c=getComputedStyle(e);return {text:e.innerText.trim(),fontSize:c.fontSize,fontFamily:c.fontFamily.slice(0,50),whiteSpace:c.whiteSpace,overflowX:c.overflowX,textOverflow:c.textOverflow,wordBreak:c.wordBreak,clientWidth:e.clientWidth,scrollWidth:e.scrollWidth,height:e.getBoundingClientRect().height,lineHeight:c.lineHeight}});
 let parentOverflow=await code.evaluate(e=>{let x=e.parentElement,o=[];for(let i=0;i<3&&x;i++,x=x.parentElement){const c=getComputedStyle(x);o.push(c.overflowX+'/'+x.clientWidth+'/'+x.scrollWidth)}return o});
 const bvis=async()=>btn.evaluate(e=>{const c=getComputedStyle(e);const r=e.getBoundingClientRect();return {opacity:c.opacity,visibility:c.visibility,display:c.display,w:r.width,h:r.height}}).catch(()=>null);
 const before=await bvis();
 await code.hover().catch(()=>{});await p.waitForTimeout(400);
 const after=await bvis();
 await p.mouse.move(0,0);await p.waitForTimeout(300);
 const box=p.locator(boxs).first();
 const cap=await shot(p,box,`${n}-commande-${w}.png`,12);
 res.push({site:n,url:u,largeur:w,m,parentOverflow,btnAvantSurvol:before,btnAuSurvol:after,capture:cap});
 console.log(n,w,JSON.stringify(m),parentOverflow,JSON.stringify(before),JSON.stringify(after));
 await ctx.close();
}
fs.writeFileSync('q1.json',JSON.stringify(res,null,1));await close();})();

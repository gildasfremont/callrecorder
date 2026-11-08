const { chromium } = require('playwright');
const OUT='/home/user/callrecorder-app/design/recos/graphisme-site/images/references/';
async function open(url,{width=1440,height=900,scheme='light',wait=2500}={}){
  if(!global.__b) global.__b=await chromium.launch();
  const ctx=await global.__b.newContext({viewport:{width,height},deviceScaleFactor:1,colorScheme:scheme,locale:'fr-FR'});
  const p=await ctx.newPage();
  await p.goto(url,{waitUntil:'domcontentloaded',timeout:45000});
  try{await p.waitForLoadState('networkidle',{timeout:8000});}catch(e){}
  await p.waitForTimeout(wait);
  return {p,ctx};
}
async function shot(p,sel,name,pad=16){
  const el=typeof sel==='string'?p.locator(sel).first():sel;
  await el.scrollIntoViewIfNeeded().catch(()=>{});
  await p.waitForTimeout(300);
  const bb=await el.boundingBox();
  if(!bb) {console.log('nobb',name);return null;}
  const vw=p.viewportSize().width;
  const clip={x:Math.max(0,bb.x-pad),y:Math.max(0,bb.y-pad)};
  clip.width=Math.min(vw-clip.x,bb.width+2*pad); clip.height=Math.min(1600,bb.height+2*pad);
  await p.screenshot({path:OUT+name,clip});
  return name;
}
async function close(){ if(global.__b) await global.__b.close(); }
module.exports={open,shot,close,OUT};

const {open,close,OUT}=require('./lib');const fs=require('fs');
// [site,url,iconSelector(js filter), caption height]
const sites=[
 ['raycast','https://www.raycast.com/store',32],
 ['linear','https://linear.app/integrations',40],
 ['notion','https://www.notion.com/fr/integrations',48],
 ['apple','https://www.apple.com/fr/apps/',56],
];
const res=[];
(async()=>{
for(const [n,u,W] of sites){
 const {p,ctx}=await open(u,{width:375,height:812,wait:3000});
 for(let i=0;i<8;i++){await p.mouse.wheel(0,700);await p.waitForTimeout(300);}
 const info=await p.evaluate((W)=>{
  const els=[...document.querySelectorAll('img,svg')].filter(e=>{const r=e.getBoundingClientRect();return Math.round(r.width)===W&&Math.abs(r.height-r.width)<=8&&r.left>=0&&r.left<375});
  els.sort((a,b)=>a.getBoundingClientRect().top-b.getBoundingClientRect().top);
  const e=els[Math.min(2,els.length-1)];
  // climb to card: element whose width >= 250
  let card=e;while(card.parentElement&&card.getBoundingClientRect().width<250)card=card.parentElement;
  // name text: first text node line in card
  const txt=card.innerText.split('\n').filter(Boolean).slice(0,4);
  // icon tile (parent with background)
  let tile=e.parentElement,tw=null;for(let i=0;i<3&&tile;i++,tile=tile.parentElement){const c=getComputedStyle(tile);if(c.backgroundColor!=='rgba(0, 0, 0, 0)'&&tile.getBoundingClientRect().width<160){tw=Math.round(tile.getBoundingClientRect().width);break;}}
  const rb=card.getBoundingClientRect();
  // count per row among same-size icons near e's top
  const t=e.getBoundingClientRect().top;const sameRow=els.filter(x=>Math.abs(x.getBoundingClientRect().top-t)<8&&x.getBoundingClientRect().left<375).length;
  card.setAttribute('data-card','1');
  return {iconPx:W,tuile:tw,parRangee:sameRow,nbIcones:els.length,carteLargeur:Math.round(rb.width),carteHauteur:Math.round(rb.height),texteCarte:txt,alt:e.getAttribute('alt')};
 },W);
 const el=p.locator('[data-card]').first();await el.scrollIntoViewIfNeeded();await p.waitForTimeout(800);
 const bb=await el.boundingBox();
 await p.screenshot({path:OUT+`${n}-icones-375.png`,clip:{x:0,y:Math.max(0,bb.y-12),width:375,height:Math.min(500,bb.height+24)}});
 info.capture=`${n}-icones-375.png`;
 res.push({site:n,url:u,...info});console.log(n,JSON.stringify(info));await ctx.close();
}
fs.writeFileSync('q4.json',JSON.stringify(res,null,1));await close();})();

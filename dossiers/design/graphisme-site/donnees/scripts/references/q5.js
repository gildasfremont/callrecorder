const {open,close,OUT}=require('./lib');const fs=require('fs');
const urls=process.argv.slice(2);const res=[];
(async()=>{
for(const spec of urls){const [n,u]=spec.split('|');
 const {p,ctx}=await open(u,{width:1440,height:900,wait:2500});
 const r=await p.evaluate(()=>{
  const h1=document.querySelector('main h1, article h1, h1');const R=e=>{const r=e.getBoundingClientRect();return {x:Math.round(r.left),droite:Math.round(r.right),w:Math.round(r.width),y:Math.round(r.top+scrollY)}};
  const h1r=R(h1);const h1c=getComputedStyle(h1);
  // text range for h1 content
  const rg=document.createRange();rg.selectNodeContents(h1);const tr=rg.getBoundingClientRect();
  const ps=[...document.querySelectorAll('main p, article p, p')].filter(p=>p.innerText.trim().length>40&&p.getBoundingClientRect().width>200);
  const p0=ps[0];const pr=p0?R(p0):null;
  // sidebar: nav or aside on the left with many links
  const navs=[...document.querySelectorAll('nav,aside,[role=navigation],[class*=sidebar],[class*=toc],[class*=Sidebar]')].map(e=>({e,r:e.getBoundingClientRect(),n:e.querySelectorAll('a').length})).filter(o=>o.n>=5&&o.r.width>120&&o.r.width<450&&o.r.height>300);
  navs.sort((a,b)=>b.n-a.n);
  const sb=navs.map(o=>({x:Math.round(o.r.left),droite:Math.round(o.r.right),w:Math.round(o.r.width),liens:o.n,cls:String(o.e.className).slice(0,40),tag:o.e.tagName}));
  return {h1:{texte:h1.innerText.trim().slice(0,60),...h1r,texteX:Math.round(tr.left),textAlign:h1c.textAlign,fontSize:h1c.fontSize},paragraphe:pr,sommaires:sb.slice(0,3)};
 });
 await p.screenshot({path:OUT+`${n}-sommaire-1440.png`,clip:{x:0,y:0,width:1440,height:620}});
 // shrink later
 res.push({site:n,url:u,...r,capture:`${n}-sommaire-1440.png`});console.log(n,JSON.stringify(r));await ctx.close();}
fs.writeFileSync('q5.json',JSON.stringify(res,null,1));await close();})();

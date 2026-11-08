const {open,close,OUT}=require('./lib');const fs=require('fs');const res=[];
(async()=>{
for(const spec of process.argv.slice(2)){const [n,u]=spec.split('|');
 const {p,ctx}=await open(u,{width:1440,wait:3000});
 const r=await p.evaluate(()=>{const vis=e=>e.getBoundingClientRect().height>0;const q=s=>[...document.querySelectorAll('main '+s+', article '+s)].filter(vis);const Q=s=>{const a=q(s);return a.length?a:[...document.querySelectorAll(s)].filter(vis).filter(e=>!e.closest('header,footer,nav'))};
  const h=t=>Q(t).map(e=>e.innerText.trim().replace(/\s+/g,' ').slice(0,60));
  const main=document.querySelector('main')||document.body;
  const h2=h('h2'),h3=h('h3');const h1=h('h1');
  const h2s=Q('h2');const h2c=h2s[0]?getComputedStyle(h2s[0]):null;
  return {h1,nbH2:h2.length,nbH3:h3.length,nbH4:h('h4').length,h2:h2.slice(0,12),h3exemples:h3.slice(0,5),tableaux:Q('table').length,listes:Q('ul,ol').filter(e=>!e.closest('nav,header,footer')).length,details:Q('details').length,mots:main.innerText.split(/\s+/).length,h2Style:h2c?{fontSize:h2c.fontSize,fontWeight:h2c.fontWeight,marginTop:h2c.marginTop}:null,sommaire:!!document.querySelector('[class*=toc],[class*=TableOfContents],nav[aria-label*=ontents i]')}});
 const firstH2=p.locator('main h2, article h2, h2').first();
 try{await firstH2.scrollIntoViewIfNeeded();await p.evaluate(()=>{document.querySelectorAll('*').forEach(e=>{const c=getComputedStyle(e);if((c.position==='fixed'||c.position==='sticky')&&e.getBoundingClientRect().height<200)e.style.visibility='hidden'})});const bb=await firstH2.boundingBox();await p.evaluate(y=>scrollBy(0,y-60),bb.y);await p.waitForTimeout(800);const b2=await firstH2.boundingBox();
 await p.screenshot({path:OUT+`${n}-confidentialite-1440.png`,clip:{x:Math.max(0,b2.x-40),y:Math.max(0,b2.y-30),width:Math.min(900,1440-Math.max(0,b2.x-40)),height:560}});r.capture=`${n}-confidentialite-1440.png`;}catch(e){r.capture=null}
 res.push({site:n,url:u,...r});console.log(n,JSON.stringify(r));await ctx.close();}
fs.writeFileSync('q10.json',JSON.stringify(res,null,1));await close();})();

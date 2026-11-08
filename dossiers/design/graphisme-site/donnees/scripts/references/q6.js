const {open,close,OUT}=require('./lib');const fs=require('fs');
const res=[];
(async()=>{
for(const spec of process.argv.slice(2)){const [n,u,tsel]=spec.split('|');
 const {p,ctx}=await open(u,{width:1440,height:900,wait:2500});
 for(let i=0;i<10;i++){await p.mouse.wheel(0,900);await p.waitForTimeout(250);}
 const r=await p.evaluate((tsel)=>{
  const Q=tsel||'summary,button[aria-expanded],[role=button][aria-expanded]';let trig=[...document.querySelectorAll(Q)].filter(e=>{const t=(e.innerText||'').trim();return t.length>15&&t.length<200&&/\?|$/.test(t)&&e.getBoundingClientRect().width>300});
  if(trig.length<3) return {trouve:trig.length};
  // item = ancestor that differs per trigger: climb while parent contains only one trigger
  const item=t=>{let e=t;while(e.parentElement&&[...e.parentElement.querySelectorAll(Q)].filter(x=>trig.includes(x)).length===1)e=e.parentElement;return e};
  const items=trig.slice(0,4).map(item);
  const S=e=>{const c=getComputedStyle(e);const r=e.getBoundingClientRect();return {tag:e.tagName,y:Math.round(r.top+scrollY),h:Math.round(r.height),x:Math.round(r.left),w:Math.round(r.width),bt:c.borderTopWidth+' '+c.borderTopStyle+' '+c.borderTopColor,bb:c.borderBottomWidth+' '+c.borderBottomStyle+' '+c.borderBottomColor,bg:c.backgroundColor,radius:c.borderRadius,boxShadow:c.boxShadow}};
  const st=items.map(S);
  // also check trigger itself and its direct parent for borders
  const trigS=S(trig[0]);
  const gaps=[];for(let i=1;i<st.length;i++)gaps.push(st[i].y-(st[i-1].y+st[i-1].h));
  // hr elements between?
  const hrs=items[0].parentElement.querySelectorAll('hr').length;
  items[0].parentElement.setAttribute('data-faq','1');
  return {trouve:trig.length,question1:trig[0].innerText.trim().slice(0,60),items:st,declencheur:trigS,ecarts:gaps,hr:hrs,pseudo:getComputedStyle(items[0],'::after').borderTopWidth+'/'+getComputedStyle(items[0],'::before').borderTopWidth+'/'+getComputedStyle(items[0],'::after').height+'/'+getComputedStyle(items[0],'::after').backgroundColor};
 },tsel);
 if(r.items){const el=p.locator('[data-faq]').first();await el.scrollIntoViewIfNeeded();await p.waitForTimeout(600);const bb=await el.boundingBox();
  const it=r.items;const y0=it[0].y, y1=it[Math.min(3,it.length-1)].y+it[Math.min(3,it.length-1)].h;
  const sy=await p.evaluate(()=>scrollY);await p.evaluate(()=>{document.querySelectorAll('*').forEach(e=>{const c=getComputedStyle(e);if((c.position==='fixed'||c.position==='sticky')&&e.getBoundingClientRect().top<150)e.style.visibility='hidden'})});await p.evaluate(y=>scrollTo(0,y-20),y0);await p.waitForTimeout(500);const sy2=await p.evaluate(()=>scrollY);
  await p.screenshot({path:OUT+`${n}-faq-1440.png`,clip:{x:Math.max(0,it[0].x-16),y:y0-sy2-12,width:Math.min(1440,it[0].w+32),height:Math.min(700,y1-y0+24)}});r.capture=`${n}-faq-1440.png`;}
 res.push({site:n,url:u,...r});console.log(n,JSON.stringify(r));await ctx.close();}
fs.writeFileSync('q6-'+Date.now()+'.json',JSON.stringify(res,null,1));await close();})();

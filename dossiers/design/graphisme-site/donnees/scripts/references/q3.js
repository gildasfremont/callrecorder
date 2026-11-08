const {open,shot,close,OUT}=require('./lib');const fs=require('fs');
const props=e=>{const c=getComputedStyle(e);return {bg:c.backgroundColor,color:c.color,opacity:c.opacity,border:c.borderColor+' '+c.borderWidth,boxShadow:c.boxShadow,textDecoration:c.textDecorationLine,cursor:c.cursor}};
const sites=[
 ['apple','https://www.apple.com/fr/macbook-air/','a[role=tab]:has-text("Presse-papiers universel")','a[role=tab][aria-selected=true]:has-text("Répondre à des appels")'],
 ['raycast','https://www.raycast.com/pricing','button[aria-pressed=false]:has-text("Plus") >> nth=0','button[aria-pressed=true]:has-text("Pro") >> nth=0'],
 ['notion','https://www.notion.com/fr/pricing','label:has-text("Facturation mensuelle")','label:has-text("Facturation annuelle")'],
];
const res=[];
(async()=>{
for(const [n,u,un,sel] of sites){
 const {p,ctx}=await open(u);
 const U=p.locator(un).first(),S=p.locator(sel).first();
 await U.scrollIntoViewIfNeeded();await p.mouse.move(0,0);await p.waitForTimeout(600);
 // also check inner child props for notion labels (bg may be on parent)
 const g=async(l)=>l.evaluate((e)=>{const P=e=>{const c=getComputedStyle(e);return {bg:c.backgroundColor,color:c.color,opacity:c.opacity,boxShadow:c.boxShadow}};return {self:P(e),parent:P(e.parentElement),child:e.firstElementChild?P(e.firstElementChild):null,checked:e.querySelector('input')?e.querySelector('input').checked:null}});
 const selP=await g(S);const before=await g(U);
 const grp=U.locator('xpath=..');
 const gbb=await U.evaluate(e=>{let x=e.parentElement;for(let i=0;i<3;i++){if(x.getBoundingClientRect().width>e.getBoundingClientRect().width*1.6)break;x=x.parentElement}x.setAttribute('data-grp','1');return true});
 await shot(p,'[data-grp]',`${n}-onglets-repos-1440.png`,10);
 await U.hover();await p.waitForTimeout(800);
 const after=await g(U);
 await shot(p,'[data-grp]',`${n}-onglets-survol-1440.png`,10);
 res.push({site:n,url:u,selectionne:selP,nonChoisiRepos:before,nonChoisiSurvol:after});
 console.log(n,JSON.stringify({selP,before,after}));
 await ctx.close();
}
fs.writeFileSync('q3.json',JSON.stringify(res,null,1));await close();})();

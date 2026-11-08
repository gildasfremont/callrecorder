const {open,close}=require('./lib');const fs=require('fs');const res=[];
const sites=[['apple','https://www.apple.com/fr/macos/'],['applesupport','https://support.apple.com/fr-fr/guide/mac-help/mchlp1066/mac'],['applesupport-accueil','https://support.apple.com/fr-fr/guide/mac-help/welcome/mac'],['notion','https://www.notion.com/fr'],['notion-tarifs','https://www.notion.com/fr/pricing']];
(async()=>{
for(const [n,u] of sites){const {p,ctx}=await open(u,{width:1440});
 const t=await p.evaluate(()=>document.body.innerText);
 const c=(re)=>(t.match(re)||[]).length;
 const avant={};for(const s of [':',';','?','!']){const e='\\'+s;avant[s]={U00A0:c(new RegExp(' '+e,'g')),U202F:c(new RegExp(' '+e,'g')),espace:c(new RegExp(' '+e,'g')),collé:c(new RegExp('[A-Za-zÀ-ÿ0-9)»’]'+e+'(?=\\s|$)','gm'))};}
 const o={site:n,url:u,caracteres:t.length,apostropheCourbe:c(/’/g),apostropheDroite:c(/'/g),guillemetsFrancais:c(/«/g),guillemetsAnglaisCourbes:c(/[“”]/g),guillemetsDroits:c(/"/g),apresOuvrant:{U00A0:c(/« /g),U202F:c(/« /g),espace:c(/« /g)},avant,
  exemplesDroite:(t.match(/.{0,12}'.{0,12}/g)||[]).slice(0,3),exemplesColle:(t.match(/.{0,15}[A-Za-zÀ-ÿ0-9][?!:](?=\s|$)/gm)||[]).slice(0,3)};
 res.push(o);console.log(JSON.stringify(o));await ctx.close();}
fs.writeFileSync('q9.json',JSON.stringify(res,null,1));await close();})();

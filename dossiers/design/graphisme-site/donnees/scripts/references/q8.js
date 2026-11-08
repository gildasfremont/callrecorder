const {open,close,OUT}=require('./lib');const fs=require('fs');const {execSync}=require('child_process');const res=[];
const sites=[['brew','https://brew.sh'],['rustup','https://rustup.rs'],['raycast','https://www.raycast.com'],['things','https://culturedcode.com/things/'],['apple','https://www.apple.com/fr/macos/'],['applesupport','https://support.apple.com/fr-fr/guide/mac-help/welcome/mac'],['linear','https://linear.app'],['notion','https://www.notion.com/fr'],['obsidian','https://obsidian.md'],['tailscale','https://tailscale.com']];
(async()=>{
for(const [n,u] of sites){const o={site:n,url:u};
 for(const sch of ['light','dark']){
  const {p,ctx}=await open(u,{width:1440,height:900,scheme:sch,wait:2500});
  o[sch]=await p.evaluate(()=>{const bg=e=>{while(e){const c=getComputedStyle(e).backgroundColor;if(c!=='rgba(0, 0, 0, 0)')return c;e=e.parentElement}return 'transparent'};
   const el=document.elementFromPoint(720,450);const pe=[...document.querySelectorAll('p')].find(p=>p.innerText.trim().length>30&&p.getBoundingClientRect().top<1400)||document.body;
   const mq=[...document.styleSheets].reduce((a,s)=>{try{return a+[...s.cssRules].filter(r=>r.media&&/prefers-color-scheme:\s*dark/.test(r.media.mediaText)).length}catch(e){return a}},0);
   return {fondBody:bg(document.body),fondCentre:bg(el),couleurTexte:getComputedStyle(pe).color,colorScheme:getComputedStyle(document.documentElement).colorScheme,reglesDark:mq,metaCS:(document.querySelector('meta[name=color-scheme]')||{}).content||null}});
  await p.screenshot({path:`/tmp/claude-0/refs-scripts/${n}-${sch}.png`,clip:{x:0,y:0,width:1440,height:600}});
  await ctx.close();}
 o.change=JSON.stringify([o.light.fondBody,o.light.fondCentre,o.light.couleurTexte])!==JSON.stringify([o.dark.fondBody,o.dark.fondCentre,o.dark.couleurTexte]);
 // pixel diff
 o.diffPixels=execSync(`python3 -c "from PIL import Image,ImageChops,ImageStat;a=Image.open('/tmp/claude-0/refs-scripts/${n}-light.png').convert('L');b=Image.open('/tmp/claude-0/refs-scripts/${n}-dark.png').convert('L');print(round(ImageStat.Stat(a).mean[0]),round(ImageStat.Stat(b).mean[0]))"`).toString().trim();
 execSync(`python3 -c "from PIL import Image;a=Image.open('/tmp/claude-0/refs-scripts/${n}-light.png');b=Image.open('/tmp/claude-0/refs-scripts/${n}-dark.png');c=Image.new('RGB',(1440,1210),'red');c.paste(a,(0,0));c.paste(b,(0,610));c=c.resize((720,605));c.save('${OUT}${n}-clair-sombre-1440.png',optimize=True)"`);
 o.capture=`${n}-clair-sombre-1440.png`;
 res.push(o);console.log(n,o.change,o.diffPixels,JSON.stringify(o.light),JSON.stringify(o.dark));}
fs.writeFileSync('q8.json',JSON.stringify(res,null,1));await close();})();

const {open,close}=require('./lib');
(async()=>{
for(const u of ['https://www.apple.com/fr/macos/','https://www.raycast.com','https://www.raycast.com/pricing','https://linear.app','https://linear.app/pricing','https://www.notion.com/fr/pricing','https://www.apple.com/fr/macbook-air/','https://www.notion.com/fr']){
 const {p,ctx}=await open(u);
 const r=await p.evaluate(()=>[...document.querySelectorAll('[role=tab],[role=radio],[aria-selected],[aria-pressed]')].map(e=>{const r=e.getBoundingClientRect();return [e.tagName,e.getAttribute('role'),e.getAttribute('aria-selected')||e.getAttribute('aria-pressed')||e.getAttribute('aria-checked'),(e.innerText||e.getAttribute('aria-label')||'').trim().slice(0,30),Math.round(r.width),Math.round(r.height),e.offsetParent!==null]}).slice(0,14));
 console.log(u,JSON.stringify(r));await ctx.close();}
await close();})();

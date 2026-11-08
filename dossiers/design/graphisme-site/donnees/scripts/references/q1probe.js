const {open,close}=require('./lib');
(async()=>{
for(const u of ['https://brew.sh','https://rustup.rs','https://tailscale.com/download/linux']){
 const {p}=await open(u);
 const r=await p.evaluate(()=>{const out=[];document.querySelectorAll('pre,code,kbd,input,[class*=copy],[class*=Copy],button').forEach(e=>{const t=(e.innerText||e.value||'').trim();if(/curl|install|copy|Copy|copier/i.test(t+e.className+(e.getAttribute('aria-label')||'')))out.push([e.tagName,String(e.className).slice(0,60),t.slice(0,120),e.getAttribute('aria-label')])});return out.slice(0,25)});
 console.log(u);console.log(JSON.stringify(r,null,0));
}
await close();})();

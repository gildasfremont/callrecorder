const { chromium } = require('playwright');
const urls = process.argv.slice(2);
(async()=>{const b=await chromium.launch();const p=await b.newPage();
for(const u of urls){try{const r=await p.goto(u,{waitUntil:'domcontentloaded',timeout:30000});console.log(r.status(),u,await p.title());}catch(e){console.log('ERR',u,e.message.split('\n')[0]);}}
await b.close();})();

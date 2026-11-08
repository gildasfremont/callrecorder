const {open,close}=require('./lib');
(async()=>{const [u,w,y,out]=process.argv.slice(2);
 const {p}=await open(u,{width:+w,height:900,wait:3000});
 await p.evaluate(y=>scrollTo(0,y),+y);await p.waitForTimeout(1500);
 await p.screenshot({path:out});await close();})();

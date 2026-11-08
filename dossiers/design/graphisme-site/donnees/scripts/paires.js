// Avant / après, même cadrage : une capture de chaque prototype, réunies côte à côte par paires.py.
const { chromium } = require('playwright');
const fs = require('fs');
const OUT = process.argv[2];
const B = 'http://localhost:8765/';
const shots = [
  { id: 'p01-fonctionnalites-reunions', page: 'fonctionnalites', w: 1440, sel: 'section#reunions' },
  { id: 'p02-ligne-375', page: 'accueil', w: 375, sel: '.cmdline' },
  { id: 'p03-versions-1440', page: 'versions', w: 1440, sel: '.versions-page', h: 1500 },
  { id: 'p05-docks-375', page: 'accueil', w: 375, sel: ['.cta + .dock-label', '.llm-dock'] },
  { id: 'p06-sources-1440', page: 'accueil', w: 1440, sel: '.claude[data-tab="appel"] .mail' },
  { id: 'p07-focus-onglets', page: 'accueil', w: 1440, sel: '.about + .tabs', tabs: 4 },
  { id: 'p10-cartes-1440', page: 'accueil', w: 1440, sel: '.benefits', h: 1700 },
  { id: 'p12-sous-titre-versions-375', page: 'versions', w: 375, sel: '.page-head' },
  { id: 'p13-confidentialite-1440', page: 'confidentialite', w: 1440, sel: '.legal', h: 1300 },
  { id: 'p14-guides-1440', page: 'guides', w: 1440, sel: '.col', h: 900 },
  { id: 'p16-titre-fonctionnalites-1440', page: 'fonctionnalites', w: 1440, sel: ['.page-head', '.feature:first-of-type h2'] },
  { id: 'p17-accueil-bords-1440', page: 'accueil', w: 1440, sel: ['.follow', '#installation .install'], h: 2600, scale: .5 },
  { id: 'p21-titre-1440', page: 'accueil', w: 1440, sel: '.about h1' },
  { id: 'p23-accueil-sombre-1440', page: 'accueil', w: 1440, sel: ['.about', '.stage'], q: '?theme=sombre' },
];
(async () => {
  const b = await chromium.launch();
  for (const s of shots) for (const v of ['avant', 'apres']) {
    const ctx = await b.newContext({ viewport: { width: s.w, height: 900 }, deviceScaleFactor: s.scale ? 1 : 2 });
    const p = await ctx.newPage();
    await p.goto(`${B}${v}/${s.page}.html${v === 'apres' && s.q ? s.q : ''}`, { waitUntil: 'networkidle' });
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } scrollTo(0, 0); });
    await p.evaluate(() => document.fonts.ready);
    await p.addStyleTag({ content: '.nav{position:relative!important}' });
    if (s.tabs) { for (let i = 0; i < s.tabs; i++) await p.keyboard.press('Tab'); }
    const sels = Array.isArray(s.sel) ? s.sel : [s.sel];
    const r = await p.evaluate(({ sels, w }) => { let x1 = 1e9, y1 = 1e9, x2 = -1e9, y2 = -1e9; for (const q of sels) { const e = [...document.querySelectorAll(q)].find(e => e.getBoundingClientRect().width > 0); if (!e) continue; const r = e.getBoundingClientRect(); x1 = Math.min(x1, r.left); y1 = Math.min(y1, r.top + scrollY); x2 = Math.max(x2, r.right); y2 = Math.max(y2, r.bottom + scrollY); } return { x: Math.max(0, x1 - 16), y: Math.max(0, y1 - 16), width: Math.min(w, x2 - x1 + 32), height: y2 - y1 + 32 }; }, { sels, w: s.w });
    if (s.h) r.height = Math.min(r.height, s.h);
    await p.screenshot({ path: `${OUT}/${s.id}-${v}.png`, fullPage: true, clip: r });
    await ctx.close();
  }
  await b.close();
})();

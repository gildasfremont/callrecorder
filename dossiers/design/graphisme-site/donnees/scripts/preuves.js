// Captures de preuve, recadrées, avec la position des éléments à annoter (en px de la capture, à l'échelle 2).
const { chromium } = require('playwright');
const fs = require('fs');
const OUT = process.argv[2];
const B = 'https://gildasfremont.github.io/callrecorder/';
const S = 2;
const shots = [
  { id: 'e01-fonctionnalites-reunion-1440', url: 'fonctionnalites/', w: 1440, clip: '#reunions figure, .feature:nth-of-type(3) figure', pad: 16, notes: [{ sel: 'img[src*="appels-reunion"]', txt: 'Image de 2560 px affichée sur 812 px : ×0,63. Texte de l’app ≈ 8 px.' }] },
  { id: 'e02-fonctionnalites-reunion-375', url: 'fonctionnalites/', w: 375, clip: 'img[src*="appels-reunion"]', pad: 16, notes: [{ sel: 'img[src*="appels-reunion"]', txt: '×0,27 : texte ≈ 3,5 px' }] },
  { id: 'e03-versions-0-24-0-1440', url: 'versions/', w: 1440, clip: '.version:nth-child(1)', pad: 8, notes: [{ sel: '.version:nth-child(1) a.thumb img', txt: '600 px affichés sur 568 : ×1,89, agrandie' }] },
  { id: 'e04-versions-0-20-0-19-1440', url: 'versions/', w: 1440, clip: ['.version:nth-child(5)', '.version:nth-child(6)'], pad: 8, notes: [{ sel: '.version:nth-child(5) a.thumb img', txt: '×0,62' }, { sel: '.version:nth-child(6) a.thumb img', txt: '×0,51, en sombre' }] },
  { id: 'e05-ligne-installation-375', url: '', w: 375, clip: '.cmdline', pad: 12, notes: [{ sel: '.cmdline', txt: '« | zsh » n’est jamais visible' }] },
  { id: 'e05-ligne-installation-1440', url: '', w: 1440, clip: '.cmdline', pad: 12, hover: '.cmdline', notes: [{ sel: '.cmdline .hint', txt: 'au survol, « Copier » couvre la fin' }] },
  { id: 'e06-cartes-iphone-1440', url: '', w: 1440, clip: ['.benefits li.o-reunion', '.benefits li.o-telephone'], pad: 8, notes: [{ sel: '.benefits li.o-telephones', txt: 'seule carte sans objet' }, { sel: '.benefits li.o-telephone img', txt: 'se lit comme l’image de la carte du dessus' }] },
  { id: 'e07-docks-375', url: '', w: 375, clip: ['.cta + .dock-label', '.llm-dock'], pad: 8, notes: [{ sel: '.dock:not(.llm-dock) .app:nth-child(8)', txt: '22 px, nom au survol seulement' }] },
  { id: 'e08-sources-claude-1440', url: '', w: 1440, clip: '.claude[data-tab="appel"] .mail', pad: 8, notes: [{ sel: '.claude[data-tab="appel"] .quotes li:nth-child(1) .sub', txt: '3,69:1' }] },
  { id: 'e09-chevron-guides-1440', url: 'guides/', w: 1440, clip: '.group', pad: 8, notes: [{ sel: 'details.row:first-child summary', txt: 'chevron #93a0b4 : 2,65:1' }] },
  { id: 'e10-focus-onglets-1440', url: '', w: 1440, tabs: 4, clip: '.about + .tabs', pad: 14, notes: [] },
  { id: 'e10-focus-lien-1440', url: '', w: 1440, tabs: 2, clip: '.nav .links', pad: 12, notes: [] },
  { id: 'e10-focus-installer-1440', url: '', w: 1440, focus: '.cta .button.hero', clip: '.cta', pad: 14, notes: [] },
  { id: 'e10-focus-ligne-1440', url: '', w: 1440, focus: '.cmdline', clip: '.cmdline', pad: 12, notes: [] },
  { id: 'e10-survol-onglets-1440', url: '', w: 1440, hover: '.about + .tabs button[data-tab=reunion]', clip: '.about + .tabs', pad: 14, notes: [{ sel: '.about + .tabs button[data-tab=reunion]', txt: 'survolé : rien ne change' }] },
  { id: 'e11-filets-guides-1440', url: 'guides/', w: 1440, clip: ['.group-label', '.group'], pad: 8, notes: [{ sel: 'details.row:nth-child(2)', txt: 'filet #d9e2ee' }, { sel: '.group-label', txt: 'libellé à 14 px, lignes à 20' }] },
  { id: 'e12-sous-titre-versions-375', url: 'versions/', w: 375, clip: '.page-head p', pad: 10, notes: [{ sel: '.page-head p', txt: '« vous- / même », « › » en début de ligne' }] },
  { id: 'e13-titre-fonctionnalites-1440', url: 'fonctionnalites/', w: 1440, viewport: { x: 0, y: 60, width: 1440, height: 420 }, lines: [{ x: 720, c: 'r', t: 'axe du titre : 720' }, { x: 432, c: 'g', t: 'bord du texte : 432' }], notes: [] },
  { id: 'e14-bords-accueil-1440', url: '', w: 1440, full: true, scale: 0.5, lines: [{ x: 196, c: 'r', t: '196' }, { x: 290, c: 'r', t: '290' }, { x: 326, c: 'r', t: '326' }, { x: 340, c: 'r', t: '340' }], notes: [] },
  { id: 'e15-trait-union-1440', url: '', w: 1440, clip: '.about h1', pad: 8, notes: [] },
  { id: 'e16-confidentialite-1440', url: 'confidentialite/', w: 1440, viewport: { x: 280, y: 60, width: 880, height: 820 }, notes: [] },
  { id: 'e17-lien-dans-texte-guides-1440', url: 'guides/', w: 1440, open: true, clip: 'details#mises-a-jour .answer p', pad: 8, notes: [{ sel: 'details#mises-a-jour .answer p a', txt: 'lien : 1,11:1 avec le texte autour' }] },
  { id: 'e18-pied-375', url: '', w: 375, clip: 'footer .links', pad: 10, notes: [{ sel: 'footer .links a:nth-child(3)', txt: '23 px de haut, voisin à 16 px' }] },
  { id: 'e19-citations-375', url: '', w: 375, clip: '.claude[data-tab="appel"] .quotes', pad: 6, notes: [{ sel: '.claude[data-tab="appel"] .quotes li:nth-child(1)', txt: '« · » en bout de ligne' }] },
  { id: 'e20-chemins-confidentialite-1440', url: 'confidentialite/', w: 1440, clip: '.legal p:nth-child(2)', pad: 8, notes: [] },
];
(async () => {
  const b = await chromium.launch();
  const meta = {};
  for (const s of shots) {
    const ctx = await b.newContext({ viewport: { width: s.w, height: 900 }, deviceScaleFactor: s.full ? 1 : S });
    const p = await ctx.newPage();
    await p.goto(B + s.url, { waitUntil: 'networkidle' });
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 30)); } scrollTo(0, 0); });
    await p.evaluate(() => document.fonts.ready);
    if (s.open) await p.evaluate(() => document.querySelectorAll('details').forEach(d => d.open = true));
    // La barre du haut se cache et revient : on la fige pour ne pas qu'elle couvre la capture.
    await p.addStyleTag({ content: '.nav{position:relative!important}' });
    let clip;
    if (s.full) {
      const path = `${OUT}/${s.id}.png`;
      await p.screenshot({ path, fullPage: true });
      meta[s.id] = { full: true, scale: s.scale, lines: s.lines, w: s.w };
      await ctx.close(); continue;
    }
    if (s.viewport) {
      await p.evaluate(y => scrollTo(0, 0), 0);
      clip = s.viewport;
    } else {
      const sels = Array.isArray(s.clip) ? s.clip : [s.clip];
      await p.locator(sels[0]).first().scrollIntoViewIfNeeded();
      await p.evaluate(() => scrollBy(0, -120));
      await p.waitForTimeout(250);
      const r = await p.evaluate(({ sels, pad }) => { let x1 = 1e9, y1 = 1e9, x2 = -1e9, y2 = -1e9; for (const q of sels) { const e = [...document.querySelectorAll(q)].find(e => e.getBoundingClientRect().width > 0); if (!e) continue; const r = e.getBoundingClientRect(); x1 = Math.min(x1, r.left); y1 = Math.min(y1, r.top + scrollY); x2 = Math.max(x2, r.right); y2 = Math.max(y2, r.bottom + scrollY); } return { x: Math.max(0, x1 - pad), y: y1 - pad, width: x2 - x1 + 2 * pad, height: y2 - y1 + 2 * pad }; }, { sels, pad: s.pad });
      clip = r;
    }
    if (s.tabs) { for (let i = 0; i < s.tabs; i++) await p.keyboard.press('Tab'); }
    if (s.focus) { await p.evaluate(q => { const e = document.querySelector(q); e.scrollIntoView({ block: 'center' }); }, s.focus); await p.keyboard.press('Tab'); await p.keyboard.press('Shift+Tab'); await p.focus(s.focus); await p.evaluate(q => { /* focus-visible au clavier */ }, s.focus); }
    if (s.hover) { await p.hover(s.hover); await p.waitForTimeout(300); }
    // Recalcule la zone après les gestes (la page a pu défiler) et prend une capture de page entière, recadrée ensuite.
    const sy = await p.evaluate(() => scrollY);
    const rect = s.viewport ? { x: clip.x, y: clip.y, width: clip.width, height: clip.height } : clip;
    const notes = await p.evaluate(({ notes, rect }) => notes.map(n => { const e = [...document.querySelectorAll(n.sel)].find(e => e.getBoundingClientRect().width > 0); if (!e) return null; const r = e.getBoundingClientRect(); return { txt: n.txt, x: r.left - rect.x, y: r.top + scrollY - rect.y, w: r.width, h: r.height }; }).filter(Boolean), { notes: s.notes, rect });
    const path = `${OUT}/${s.id}.png`;
    await p.screenshot({ path, fullPage: true, clip: { x: rect.x, y: rect.y, width: rect.width, height: rect.height } });
    meta[s.id] = { notes, scale: S, lines: s.lines ? s.lines.map(l => ({ ...l, x: l.x - rect.x })) : null };
    await ctx.close();
  }
  fs.writeFileSync(`${OUT}/preuves.json`, JSON.stringify(meta, null, 1));
  await b.close();
})();

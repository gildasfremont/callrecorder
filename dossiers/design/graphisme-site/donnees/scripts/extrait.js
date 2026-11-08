// Extraction exhaustive du site en ligne : textes, styles calculés, contrastes WCAG 2 et APCA, cibles, images.
// node extrait.js <dossier-donnees>
const { chromium } = require('playwright');
const fs = require('fs');
const OUT = process.argv[2];
const BASE = process.env.BASE || 'https://gildasfremont.github.io/callrecorder/';
const PAGES = process.env.PAGES ? process.env.PAGES.split(',') : ['', 'fonctionnalites/', 'guides/', 'versions/', 'confidentialite/'];
const WIDTHS = [375, 768, 1440];

const inPage = () => {
  const parse = (s) => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 }; };
  const over = (top, bot) => { const a = top.a + bot.a * (1 - top.a); if (a === 0) return { r: 0, g: 0, b: 0, a: 0 }; return { r: (top.r * top.a + bot.r * bot.a * (1 - top.a)) / a, g: (top.g * top.a + bot.g * bot.a * (1 - top.a)) / a, b: (top.b * top.a + bot.b * bot.a * (1 - top.a)) / a, a }; };
  const hex = (c) => '#' + [c.r, c.g, c.b].map(v => Math.round(v).toString(16).padStart(2, '0')).join('');
  const lin = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const L = (c) => 0.2126 * lin(c.r) + 0.7152 * lin(c.g) + 0.0722 * lin(c.b);
  const wcag = (a, b) => { const x = L(a), y = L(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
  // APCA 0.0.98G-4g (W3 « Silver » draft, apca-w3 0.1.9)
  const apca = (txt, bg) => {
    const Y = (c) => 0.2126729 * Math.pow(c.r / 255, 2.4) + 0.7151522 * Math.pow(c.g / 255, 2.4) + 0.0721750 * Math.pow(c.b / 255, 2.4);
    const clamp = (y) => y < 0.022 ? y + Math.pow(0.022 - y, 1.414) : y;
    const t = clamp(Y(txt)), b = clamp(Y(bg));
    if (Math.abs(b - t) < 0.0005) return 0;
    if (b > t) { const s = (Math.pow(b, 0.56) - Math.pow(t, 0.57)) * 1.14; return s < 0.1 ? 0 : (s - 0.027) * 100; }
    const s = (Math.pow(b, 0.65) - Math.pow(t, 0.62)) * 1.14; return s > -0.1 ? 0 : (s + 0.027) * 100;
  };
  const visible = (el) => { const r = el.getBoundingClientRect(); if (r.width === 0 || r.height === 0) return false; const cs = getComputedStyle(el); return cs.visibility !== 'hidden' && cs.display !== 'none' && +cs.opacity > 0 && !el.closest('[hidden]'); };
  const sel = (el) => { const parts = []; let e = el; for (let i = 0; i < 4 && e && e !== document.body; i++, e = e.parentElement) { let s = e.tagName.toLowerCase(); if (e.id) s += '#' + e.id; if (e.classList.length) s += '.' + [...e.classList].join('.'); parts.unshift(s); } return parts.join(' > '); };
  const background = (el) => {
    const stack = []; let complex = '';
    for (let e = el; e; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.backgroundImage && cs.backgroundImage !== 'none' && !complex) complex = cs.backgroundImage.slice(0, 40);
      const c = parse(cs.backgroundColor); if (c && c.a > 0) { stack.push(c); if (c.a >= 1) break; }
    }
    let base = { r: 255, g: 255, b: 255, a: 1 };
    for (let i = stack.length - 1; i >= 0; i--) base = over(stack[i], base);
    return { c: base, complex };
  };
  const apcaNeed = (fs, w) => fs >= 36 || (fs >= 24 && w >= 600) ? 45 : (fs >= 24 || (fs >= 16 && w >= 600) || (fs >= 18)) ? 60 : 75;
  const texts = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  while (walker.nextNode()) {
    const n = walker.currentNode; const t = n.textContent.replace(/\s+/g, ' ').trim(); if (!t) continue;
    const el = n.parentElement; if (!el || seen.has(el) || ['SCRIPT', 'STYLE'].includes(el.tagName)) continue;
    if (!visible(el)) continue; seen.add(el);
    const cs = getComputedStyle(el); const r = el.getBoundingClientRect();
    let fg = parse(cs.color); const bg = background(el); fg = over(fg, bg.c);
    const fsz = parseFloat(cs.fontSize), w = +cs.fontWeight;
    const large = fsz >= 24 || (fsz >= 18.66 && w >= 700);
    const ratio = wcag(fg, bg.c), lc = Math.abs(apca(fg, bg.c));
    texts.push({ sel: sel(el), tag: el.tagName.toLowerCase(), texte: el.innerText.replace(/\s+/g, ' ').trim().slice(0, 140), famille: cs.fontFamily.split(',')[0].replace(/"/g, ''), taille: fsz, graisse: w, interligne: cs.lineHeight === 'normal' ? 'normal' : +(parseFloat(cs.lineHeight) / fsz).toFixed(3), approche: cs.letterSpacing, couleur: hex(fg), fond: hex(bg.c), fond_complexe: bg.complex, wcag: +ratio.toFixed(2), wcag_seuil: large ? 3 : 4.5, wcag_ok: ratio >= (large ? 3 : 4.5), apca_lc: +lc.toFixed(1), apca_seuil: apcaNeed(fsz, w), apca_ok: lc >= apcaNeed(fsz, w), x: Math.round(r.left), y: Math.round(r.top + scrollY), l: Math.round(r.width), h: Math.round(r.height), lignes: Math.max(1, Math.round(r.height / (parseFloat(cs.lineHeight) || fsz * 1.2))) });
  }
  // Cibles : tout ce qui se clique ou se focalise.
  const targets = [...document.querySelectorAll('a[href], button, summary, textarea, input, [role=tab], [tabindex]')].filter(visible).map(el => { const r = el.getBoundingClientRect(); const pcs = el.parentElement ? getComputedStyle(el.parentElement) : null; const inline = getComputedStyle(el).display === 'inline' && el.parentElement && /^(P|LI|SPAN|DIV)$/.test(el.parentElement.tagName) && (el.parentElement.innerText || '').trim().length > (el.innerText || '').trim().length + 20; return { sel: sel(el), dans_phrase: inline, texte: (el.innerText || el.getAttribute('aria-label') || el.getAttribute('title') || '').replace(/\s+/g, ' ').trim().slice(0, 60), l: +r.width.toFixed(1), h: +r.height.toFixed(1), cx: r.left + r.width / 2, cy: r.top + scrollY + r.height / 2 }; });
  targets.forEach((t, i) => { let d = 9999; targets.forEach((u, j) => { if (i !== j) d = Math.min(d, Math.hypot(t.cx - u.cx, t.cy - u.cy)); }); t.dist_voisin = Math.round(d); t.min = Math.min(t.l, t.h); t.wcag_258 = t.min >= 24 || d >= 24; t.hig_44 = t.min >= 44; }); targets.forEach(t => { delete t.cx; delete t.cy; });
  const imgs = [...document.querySelectorAll('img')].map(img => { const r = img.getBoundingClientRect(); const cs = getComputedStyle(img); return { sel: sel(img), src: img.getAttribute('src'), nat_l: img.naturalWidth, nat_h: img.naturalHeight, aff_l: Math.round(r.width), aff_h: Math.round(r.height), echelle_2x: img.naturalWidth ? +(r.width * 2 / img.naturalWidth).toFixed(2) : null, visible: visible(img), attr_l: img.getAttribute('width'), attr_h: img.getAttribute('height'), loading: img.getAttribute('loading') || '', alt: img.getAttribute('alt'), decoupe: img.classList.contains('decoupe'), filtre: cs.filter !== 'none', ombre_boite: cs.boxShadow !== 'none', bord: cs.borderTopWidth !== '0px' ? cs.borderTopWidth + ' ' + cs.borderTopColor : '', rayon: cs.borderRadius }; });
  return { texts, targets, imgs, hauteur: document.documentElement.scrollHeight, largeur_doc: document.documentElement.scrollWidth };
};

(async () => {
  const b = await chromium.launch();
  const all = { textes: [], cibles: [], images: [], pages: [] };
  for (const w of WIDTHS) {
    const ctx = await b.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1 });
    const p = await ctx.newPage();
    for (const pg of PAGES) {
      const name = pg.replace('/', '').replace('.html', '') || 'accueil';
      await p.goto(BASE + pg, { waitUntil: 'networkidle' });
      await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); } scrollTo(0, 0); });
      await p.evaluate(() => document.fonts.ready);
      // Les états : chaque variante qu'un visiteur peut voir sur la page.
      const states = [['repos', null]];
      if (name === 'accueil') states.push(['onglet-reunions', async () => p.click('.tabs:not(.install-tabs) button[data-tab=reunion]')], ['onglet-notes', async () => p.click('.tabs:not(.install-tabs) button[data-tab=note]')], ['installation-sans-claude', async () => p.click('.install-tabs button[data-scenario=seul]')]);
      if (name === 'guides') states.push(['tout-deplie', async () => p.evaluate(() => document.querySelectorAll('details').forEach(d => d.open = true))]);
      states.push(['message-ouvert', async () => p.evaluate(() => document.querySelector('.open-message')?.click())]);
      for (const [st, act] of states) {
        if (act) { await act(); await p.waitForTimeout(250); await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 900) { scrollTo(0, y); await new Promise(r => setTimeout(r, 25)); } scrollTo(0, 0); }); }
        const r = await p.evaluate(inPage);
        const tag = (o) => ({ page: name, largeur: w, etat: st, ...o });
        all.textes.push(...r.texts.map(tag)); all.cibles.push(...r.targets.map(tag)); all.images.push(...r.imgs.map(tag));
        all.pages.push({ page: name, largeur: w, etat: st, hauteur: r.hauteur, largeur_doc: r.largeur_doc });
      }
    }
    await ctx.close();
  }
  await b.close();
  fs.writeFileSync(OUT + '/' + (process.env.NOM || 'extraction') + '.json', JSON.stringify(all));
  console.log('textes', all.textes.length, 'cibles', all.cibles.length, 'images', all.images.length);
})();

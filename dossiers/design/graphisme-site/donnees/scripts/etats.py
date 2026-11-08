# Planche des états : chaque composant du site dans chacun de ses états, avant et après.
# Les états sont forcés : un petit script recopie les règles :hover, :focus-visible et :active vers .is-hover, .is-focus, .is-active.
import sys
P = sys.argv[1]
LIVE = 'https://gildasfremont.github.io/callrecorder/'
FORCE = """<script>
// Recopie chaque règle d'état en une classe, pour montrer l'état sans souris ni clavier.
addEventListener('DOMContentLoaded', () => {
  for (const sheet of document.styleSheets) {
    let rules; try { rules = sheet.cssRules; } catch (e) { continue; }
    const add = [];
    const walk = (list, media) => { for (const r of list) {
      if (r.cssRules && r.media) { walk(r.cssRules, r.media.mediaText); continue; }
      if (!r.selectorText || !/:(hover|focus-visible|focus|active)/.test(r.selectorText)) continue;
      const sel = r.selectorText.replace(/:hover/g, '.is-hover').replace(/:focus-visible/g, '.is-focus').replace(/:focus(?![-\\w])/g, '.is-focus').replace(/:active/g, '.is-active');
      add.push((media ? '@media ' + media + '{' : '') + sel + '{' + r.style.cssText + '}' + (media ? '}' : ''));
    } };
    walk(rules, '');
    add.forEach(t => { try { sheet.insertRule(t, sheet.cssRules.length); } catch (e) {} });
  }
  if (/theme=sombre/.test(location.search)) document.documentElement.dataset.theme = 'sombre';
});
</script>"""
# Chromium n'a pas d'anneau par défaut sur une classe : on reproduit celui du navigateur pour l'avant.
AVANT_FOCUS = '<style>.is-focus{outline:auto 2px -webkit-focus-ring-color;outline:2px solid #101010;outline-offset:1px}</style>'
ST = lambda t: f'<p class="etiquette">{t}</p>'
def cell(label, html): return f'<div class="cas">{html}{ST(label)}</div>'
def row(title, cells): return f'<section class="composant"><h2 class="titre-composant">{title}</h2><div class="cases">{"".join(cells)}</div></section>'
B = []
B.append(row('Lien de la barre', [cell(s, f'<nav class="nav" style="position:static;padding:8px 0;background:none;box-shadow:none;clip-path:none;transform:none"><div class="links"><a class="{c}" href="#">Fonctionnalités</a></div></nav>') for s, c in [('repos', ''), ('survol', 'is-hover'), ('focus clavier', 'is-focus')]]))
B.append(row('Bouton de la barre', [cell(s, f'<a class="button {c}" href="#">Installer</a>') for s, c in [('repos', ''), ('survol', 'is-hover'), ('focus', 'is-focus'), ('appui', 'is-active')]]))
B.append(row('Bouton principal', [cell(s, f'<a class="button hero {c}" href="#">Installer Callrecorder</a>') for s, c in [('repos', ''), ('survol', 'is-hover'), ('focus', 'is-focus'), ('appui', 'is-active is-hover')]]))
tabs = lambda sel, c: f'<div class="tabs" style="margin:0"><button aria-selected="true" class="{c if sel else ""}">Appels et visios</button><button aria-selected="false" class="{"" if sel else c}">Réunions</button><button aria-selected="false">Notes vocales</button></div>'
B.append(row('Contrôle segmenté', [cell('repos', tabs(True, '')), cell('survol d’un segment', tabs(False, 'is-hover')), cell('appui', tabs(False, 'is-active is-hover')), cell('focus', tabs(True, 'is-focus'))]))
cmd = lambda c, copied='': f'<div class="install" style="margin:0;width:100%"><button class="cmdline {c}" type="button" style="margin:20px 0 0"><code>curl -fsSL https://github.com/<wbr>gildasfremont/<wbr>callrecorder/<wbr>releases/<wbr>latest/<wbr>download/<wbr>install.sh&nbsp;|&nbsp;zsh</code><span class="hint" aria-hidden="true">Copier</span>{copied}</button></div>'
B.append(row('Ligne d’installation', [cell(s, cmd(c, k)) for s, c, k in [('repos', '', ''), ('survol', 'is-hover', ''), ('focus', 'is-focus', ''), ('copiée', '', '<span class="copied" style="animation:none;opacity:1;rotate:-6deg">Copié</span>')]]))
dock = lambda c: f'<div class="dock" style="margin:40px 0 0"><span class="app tile {c}" data-name="Microsoft Teams" tabindex="0"><img src="{LIVE}img/pile/teams.png" alt="Microsoft Teams"></span><span class="app tile" data-name="Zoom"><img src="{LIVE}img/pile/zoom.png" alt="Zoom"></span><span class="app" data-name="FaceTime"><img src="{LIVE}img/logos/facetime.png" alt="FaceTime"></span></div>'
B.append(row('Icône du dock', [cell(s, dock(c)) for s, c in [('repos', ''), ('survol', 'is-hover'), ('focus clavier ou toucher', 'is-focus')]]))
det = lambda c, o='': f'<div class="group" style="width:100%"><details class="row" {o}><summary class="{c}">Donner à Claude l’accès à vos appels</summary><div class="answer"><p>Quittez et relancez Claude, puis demandez-lui : « Qu’est-ce que j’ai promis à Paul jeudi ? » Voir <a href="#">Versions</a>.</p></div></details><details class="row"><summary>Relier vos appels à un autre assistant</summary></details></div>'
B.append(row('Question des Guides', [cell(s, det(c, o)) for s, c, o in [('fermée', '', ''), ('survol', 'is-hover', ''), ('focus', 'is-focus', ''), ('ouverte', '', 'open')]]))
B.append(row('Lien dans une phrase', [cell(s, f'<details class="row" open style="list-style:none"><summary style="display:none"></summary><div class="answer" style="padding:0"><p>Rien ne change pour vous : voir <a class="{c}" href="#">Versions</a> pour le détail.</p></div></details>') for s, c in [('repos', ''), ('survol', 'is-hover'), ('focus', 'is-focus')]]))
rec = lambda c, t='Dicter': f'<div class="author"><div class="says" style="margin:0"><div class="bubble"><form class="message"><div class="message-actions"><button class="rec-toggle {c}" type="button">{t}</button><button class="button send" type="button" {"disabled" if t == "Dicter" else ""}>Envoyer</button></div></form></div></div></div>'
B.append(row('Message pour Gildas', [cell(s, rec(c, t)) for s, c, t in [('repos, Envoyer inactif', '', 'Dicter'), ('survol de Dicter', 'is-hover', 'Dicter'), ('focus', 'is-focus', 'Dicter'), ('dictée en cours', 'on', 'Pause')]]))
B.append(row('Sommaire des Fonctionnalités', [cell(s, f'<div class="toc" style="display:block;position:static;padding:0"><nav style="display:flex;flex-direction:column"><a class="{c}" href="#" {"aria-current=true" if s == "page en cours" else ""} style="font-size:15px;padding:6px 12px;border-radius:7px">Réunions</a></nav></div>') for s, c in [('repos', ''), ('survol', 'is-hover'), ('page en cours', ''), ('focus', 'is-focus')]]))
B.append(row('Liens du pied', [cell(s, f'<footer style="padding:0"><div class="links"><a href="#" class="{c}">Fonctionnalités</a><a href="#">Guides</a><a href="#">Versions</a></div></footer>') for s, c in [('repos', ''), ('survol', 'is-hover'), ('focus', 'is-focus')]]))
B.append(row('Badge et version', [cell('repos', '<div class="group" style="width:100%"><div class="row version"><div class="num">0.24.0<span class="latest">Dernière</span><small>7 novembre 2026</small></div><div><p>Le téléphone Android arrive, en bêta.</p></div></div></div>')]))
B.append(row('Source d’une citation', [cell('repos', '<div class="claude" style="position:static;width:100%;font-size:15px"><div class="body"><div class="mail"><ul class="quotes"><li>« On renouvelle, mais avec un covenant sur la dette nette. » <span class="sub">· Banque Aurore, 28 oct.</span></li></ul></div></div></div>')]))
STYLE = """<style>
body{padding:24px 20px 60px} .composant{margin:0 0 28px} .titre-composant{font:600 13px/1.3 -apple-system,sans-serif;color:var(--secondary,#566175);text-transform:none;margin:0 0 8px;font-family:-apple-system,BlinkMacSystemFont,sans-serif}
.cases{display:flex;flex-wrap:wrap;gap:12px 20px;align-items:flex-start}.cas{min-width:180px;max-width:520px;flex:1}.etiquette{font:12px/1.3 -apple-system,sans-serif;color:#7a8597;margin:6px 0 0}
</style>"""
def page(apres):
    css = '<link rel="stylesheet" href="css/site-953f6d3.css">' + ('\n<link rel="stylesheet" href="css/apres.css">' if apres else AVANT_FOCUS)
    body = ''.join(B)
    if not apres: body = body.replace('&nbsp;|&nbsp;', ' | ').replace('<wbr>', '').replace('Qu’est', "Qu'est").replace('j’ai', "j'ai")
    else: body = body.replace('<span class="sub">· ', '<span class="sub">')
    return f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>États {"après" if apres else "avant"}</title>{css}{STYLE}{FORCE}</head><body>{body}</body></html>'
open(f'{P}/etats-avant.html', 'w').write(page(False))
open(f'{P}/etats-apres.html', 'w').write(page(True))
print('ok')

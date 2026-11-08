"""Prototypes : chaque écran en HTML/CSS, 1 px CSS = 1 dp, avec les vraies valeurs de Look.kt (avant) et du système (après)."""
from commun import *
import re, glob, os

RES = '/home/user/callrecorder-app/phone/android/app/src/main/res/drawable'

def load_icons():
    out = {}
    for f in glob.glob(RES + '/*.xml'):
        t = open(f).read(); name = os.path.basename(f)[:-4]
        vb = re.search(r'viewportWidth="([\d.]+)"', t).group(1) if 'viewportWidth' in t else '24'
        paths = []
        for m in re.finditer(r'<path([^>]*)/?>', t, re.S):
            a = m.group(1)
            d = re.search(r'pathData="([^"]+)"', a).group(1)
            sw_ = re.search(r'strokeWidth="([\d.]+)"', a); fc = re.search(r'fillColor="(#[0-9A-Fa-f]+)"', a); sc = re.search(r'strokeColor="(#[0-9A-Fa-f]+)"', a)
            fill = fc and fc.group(1)[-8:-6] != '00' if fc else False
            stroke = sc is not None
            paths.append((d, float(sw_.group(1)) if sw_ else 0, fill, stroke, sc.group(1) if sc else None))
        out[name] = (vb, paths)
    return out

ICONS = load_icons()

def ico(name, size=24, color='currentColor', v='av', baked=True):
    vb, paths = ICONS[name]
    ps = []
    for d, s, fill, stroke, scol in paths:
        sw_ = s
        if v == 'ap' and stroke and s: sw_ = 2
        op = ''
        if baked and scol and scol[1:3] not in ('FF',) and v == 'av':
            op = f' stroke-opacity="{int(scol[1:3], 16) / 255:.2f}"'
        ps.append(f'<path d="{d}" fill="{color if fill else "none"}" stroke="{color if stroke else "none"}" stroke-width="{sw_}" stroke-linecap="round" stroke-linejoin="round"{op}/>')
    return f'<svg width="{size}" height="{size}" viewBox="0 0 {vb} {vb}" aria-hidden="true">{"".join(ps)}</svg>'

THEMES = {
 ('l', 'av'): dict(bg='#F5F5F5', tx='#1D1D1F', sec='rgba(0,0,0,.6)', title='rgba(0,0,0,.56)', at='rgba(0,0,0,.5)', card='rgba(0,0,0,.05)', btn='rgba(0,0,0,.07)',
     touch='rgba(0,0,0,.12)', float='rgba(255,255,255,.94)', acc='#0064D2', accfill='#0064D2', onacc='#fff', me='#0064D2', them='#A0470A', mefill='rgba(0,100,210,.12)', themfill='rgba(160,71,10,.12)',
     live='#C41E14', warn='#A0470A', chev='rgba(0,0,0,.16)', next='rgba(0,0,0,.24)', kind='rgba(0,0,0,.55)', wa='#25D366', sig='#3B45FD', tg='#26A5E4', meet='#00897B', neutral='rgba(0,0,0,.45)',
     v1='#A0470A', v2='#A0470A', v1fill='rgba(160,71,10,.12)', v2fill='rgba(160,71,10,.12)', livefill='rgba(0,0,0,.07)', accplate='rgba(0,100,210,.12)', dot='#D32F2F'),
 ('l', 'ap'): dict(bg='#F5F5F5', tx='#1D1D1F', sec='rgba(0,0,0,.6)', title='rgba(0,0,0,.6)', at='rgba(0,0,0,.6)', card='rgba(0,0,0,.05)', btn='rgba(0,0,0,.07)',
     touch='rgba(0,0,0,.12)', float='rgba(255,255,255,.94)', acc='#0064D2', accfill='#0064D2', onacc='#fff', me='#0058C0', them='#8A3D06', mefill='rgba(0,88,192,.12)', themfill='rgba(138,61,6,.12)',
     live='#C41E14', warn='#A0470A', chev='rgba(0,0,0,.6)', next='rgba(0,0,0,.6)', kind='rgba(0,0,0,.6)', wa='#0F8A4B', sig='#3B45FD', tg='#1C7FB8', meet='#00897B', neutral='rgba(0,0,0,.45)',
     v1='#16692E', v2='#7E35B0', v1fill='rgba(22,105,46,.12)', v2fill='rgba(126,53,176,.12)', livefill='rgba(196,30,20,.12)', accplate='rgba(0,100,210,.12)', dot='#C41E14'),
 ('d', 'av'): dict(bg='#1E1E1E', tx='#F5F5F7', sec='rgba(255,255,255,.62)', title='rgba(255,255,255,.62)', at='rgba(255,255,255,.5)', card='rgba(255,255,255,.05)', btn='rgba(255,255,255,.07)',
     touch='rgba(255,255,255,.12)', float='rgba(44,44,46,.94)', acc='#0064D2', accfill='#0064D2', onacc='#fff', me='#409CFF', them='#FF9F0A', mefill='rgba(64,156,255,.12)', themfill='rgba(255,159,10,.12)',
     live='#FF453A', warn='#FF9F0A', chev='rgba(255,255,255,.16)', next='rgba(255,255,255,.25)', kind='rgba(255,255,255,.55)', wa='#25D366', sig='#3B45FD', tg='#26A5E4', meet='#00897B', neutral='rgba(255,255,255,.45)',
     v1='#FF9F0A', v2='#FF9F0A', v1fill='rgba(255,159,10,.12)', v2fill='rgba(255,159,10,.12)', livefill='rgba(255,255,255,.07)', accplate='rgba(0,100,210,.12)', dot='#D32F2F'),
 ('d', 'ap'): dict(bg='#1E1E1E', tx='#F5F5F7', sec='rgba(255,255,255,.7)', title='rgba(255,255,255,.7)', at='rgba(255,255,255,.7)', card='rgba(255,255,255,.05)', btn='rgba(255,255,255,.07)',
     touch='rgba(255,255,255,.12)', float='rgba(44,44,46,.94)', acc='#409CFF', accfill='#409CFF', onacc='#1E1E1E', me='#7AB8FF', them='#FFC79A', mefill='rgba(122,184,255,.2)', themfill='rgba(255,199,154,.2)',
     live='#FF453A', warn='#FF9F0A', chev='rgba(255,255,255,.7)', next='rgba(255,255,255,.7)', kind='rgba(255,255,255,.7)', wa='#25D366', sig='#8E95FF', tg='#26A5E4', meet='#2BB3A6', neutral='rgba(255,255,255,.45)',
     v1='#4CD474', v2='#D0A8FF', v1fill='rgba(76,212,116,.2)', v2fill='rgba(208,168,255,.2)', livefill='rgba(255,69,58,.2)', accplate='rgba(64,156,255,.2)', dot='#FF453A'),
}
# Avant, sombre : les endroits qui gardent #0064D2 (P02)
THEMES[('d', 'av')]['acctext'] = '#0064D2'; THEMES[('d', 'ap')]['acctext'] = '#409CFF'
THEMES[('l', 'av')]['acctext'] = '#0064D2'; THEMES[('l', 'ap')]['acctext'] = '#0064D2'

def theme_css():
    out = []
    for (m, v), t in THEMES.items():
        out.append(f'.ph.{m}.{v}{{' + ';'.join(f'--{k}:{c}' for k, c in t.items()) + '}')
    return '\n'.join(out)

PCSS = r"""
.protos{display:grid;grid-template-columns:repeat(4,max-content);gap:16px 14px;overflow-x:auto;padding:6px 2px 14px}
.protos.two{grid-template-columns:repeat(2,max-content)}
.pcap{font-size:13px;color:var(--muted);font-weight:600;margin-bottom:6px}
.ph{zoom:.62;width:412px;background:var(--bg);color:var(--tx);font-family:Roboto,"Google Sans Text",system-ui,sans-serif;font-size:16px;line-height:1.17;border-radius:28px;overflow:hidden;position:relative;box-shadow:0 0 0 1px rgba(127,127,127,.3)}
.ph *{box-sizing:border-box}
.ph .scr{min-height:var(--h,600px);position:relative;padding-bottom:4px}
.ph .row{display:flex;align-items:center}
.ph .grow{flex:1;min-width:0}
.ph .one{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ph .sec{color:var(--sec)} .ph .med{font-weight:500}
.ph .tn{font-variant-numeric:tabular-nums}
.ph .ib{width:48px;height:48px;display:flex;align-items:center;justify-content:center;border-radius:24px;flex:none}
.ph .bar{display:flex;align-items:center;min-height:64px;padding:0 4px}
.ph .plate{display:flex;align-items:center;justify-content:center;flex:none;background:var(--btn)}
.ph .day{font-size:14px;font-weight:500;color:var(--title);padding:12px 12px 6px}
.ph .trow{display:flex;align-items:center;min-height:64px;padding:8px;border-radius:12px}
.ph .trow .plate{width:44px;height:44px;border-radius:8px}
.ph .trow .t{font-size:16px} .ph .trow .m{font-size:14px;color:var(--sec);margin-top:2px}
.ph .foot{padding:8px 12px 16px} .ph .frow{display:flex;align-items:center;min-height:48px;padding:0 12px 0 8px;font-size:16px;color:var(--sec);gap:8px}
.ph .switch{display:flex;background:var(--card);border-radius:26px;padding:2px;gap:2px}
.ph .switch .ib{width:52px;border-radius:24px}
.ph .card{background:var(--card);border-radius:12px}
.ph .mark{border-radius:999px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:500;flex:none}
.ph .line{display:flex;padding-bottom:16px}
.ph .said{font-size:16px;line-height:1.35}
.ph .tools{position:absolute;bottom:24px;left:50%;transform:translateX(-50%);display:flex;background:var(--float);border-radius:24px;padding:4px;box-shadow:0 3px 10px rgba(0,0,0,.18)}
.ph .tool{min-width:76px;min-height:56px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:12px;gap:3px;border-radius:20px}
.ph .status{height:28px;display:flex;align-items:center;justify-content:space-between;padding:0 18px;font-size:13px}
"""

def P(v, m): return f'<div class="ph {m} {v}">'

def bar(title, detail='', lead=None, end=None, v='av', detail_html=None):
    lead_html = f'<div class="plate" style="width:36px;height:36px;border-radius:{6.5 if v == "av" else 8}px;margin:0 6px 0 4px">{lead}</div>' if lead else ''
    tsz = '17px;font-weight:400' if v == 'av' else '16px;font-weight:500'
    dsz = '13px' if v == 'av' else '14px'
    return (f'<div class="bar"><div class="ib">{ico("ic_retour", 22, "var(--tx)", v)}</div>{lead_html}<div class="grow" style="margin-left:4px">'
            f'<div class="one" style="font-size:{tsz}">{title}</div>' + (f'<div class="one sec" style="font-size:{dsz}">{detail_html or detail}</div>' if (detail or detail_html) else '') +
            f'</div>{end or ""}</div>')

def kind(name, color, size=20, v='av'): return ico(name, size, color, v)

def more(v): return f'<div class="ib">{ico("ic_plus", 22, "var(--sec)", v)}</div>'

def accueil(v, m, state='liste'):
    t = THEMES[(m, v)]
    rows = []
    if state == 'ecoute':
        rows.append(f'<div class="trow"><div class="plate" style="background:var(--accplate)">{kind("ic_onde", "var(--acctext)", 20, v)}</div><div class="grow" style="margin-left:12px"><div class="t">Journal</div><div class="m" style="color:var(--acctext)">● Écoute depuis 08:12</div></div></div>')
    if state == 'enregistre':
        rows.append('<div class="day">Aujourd\'hui · dimanche 8 novembre</div>')
        rows.append(f'<div class="trow"><div class="plate" style="background:var(--livefill)">{kind("ic_micro", "var(--live)", 20, v)}</div><div class="grow" style="margin-left:12px"><div class="t">Réunion</div><div class="m {"tn" if v == "ap" else ""}" style="color:var(--live)">10:02 · ● En cours · {"9 s" if v == "av" else "11 s"}</div></div></div>')
    rows.append('<div class="day">Samedi 7 novembre</div>')
    names = 'Sophie Marchand, Karim Benali, Julie Roussel'
    rows.append(f'<div class="trow"><div class="plate">{kind("ic_reunion", "var(--kind)", 20, v)}</div><div class="grow" style="margin-left:12px"><div class="t one">Revue budgétaire</div><div class="m one {"tn" if v == "ap" else ""}">15:48 · 34 min · {names if v == "av" else "Sophie Marchand +2"}</div></div></div>')
    rows.append(f'<div class="trow"><div class="plate">{kind("ic_whatsapp", "var(--wa)", 20, v)}</div><div class="grow" style="margin-left:12px"><div class="t one">Paul Mercier · expert-comptable</div><div class="m one">14:00 · 9 min · Paul Mercier</div></div></div>')
    rows.append(f'<div class="trow"><div class="plate">{kind("ic_telegram", "var(--tg)", 20, v)}</div><div class="grow" style="margin-left:12px"><div class="t one">Marc Lefort</div><div class="m one">11:20 · 5 min · Marc Lefort</div></div></div>')
    rows.append('<div class="day">Vendredi 6 novembre</div>')
    rows.append(f'<div class="trow"><div class="plate">{kind("ic_signal", "var(--sig)", 20, v)}</div><div class="grow" style="margin-left:12px"><div class="t one">Claire Duval</div><div class="m one">17:15 · 12 min · Claire Duval</div></div></div>')
    rows.append(f'<div class="trow"><div class="plate">{kind("ic_telephone", "var(--kind)", 20, v)}</div><div class="grow" style="margin-left:12px"><div class="t one">Caisse Régionale Sud · crédit</div><div class="m one">17:15 · 7 min · Pierre Lenoir</div></div></div>')
    listsel = 'var(--acc)' if v == 'ap' else 'var(--tx)'
    top = (f'<div class="row" style="height:64px;padding:0 12px"><div class="switch"><div class="ib" style="background:var(--touch)">{ico("ic_liste", 22, listsel, v)}</div><div class="ib">{ico("ic_calendrier", 22, "var(--sec)", v)}</div></div><div class="grow"></div><div class="ib">{ico("ic_chercher", 22, "var(--sec)", v)}</div></div>')
    if state == 'enregistre':
        foot = f'<div class="frow" style="color:var(--live)">{ico("ic_arreter", 24, "var(--live)", v)}Arrêter l\'enregistrement</div><div class="frow">{ico("ic_photo", 24, "var(--sec)", v)}Prendre une photo</div>'
    else:
        foot = f'<div class="frow">{ico("ic_enregistrer", 24, "var(--sec)", v)}Enregistrer une réunion</div><div class="frow">{ico("ic_reglages", 24, "var(--sec)", v)}Réglages</div>'
    return f'{P(v, m)}<div class="scr" style="--h:720px;display:flex;flex-direction:column">{top}<div style="padding:4px 12px;flex:1">{"".join(rows)}</div><div class="foot">{foot}</div></div></div>'

def calendrier(v, m):
    cells = []
    days = list(range(1, 31)); lead = 6
    has = {5, 6, 7, 8}
    grid = [''] * lead + days
    pad = 8 if v == 'av' else 0
    for i, d in enumerate(grid):
        if d == '': cells.append('<div></div>'); continue
        today = d == 8; sel = d == 6 if v == 'ap' else d == 8
        if v == 'av':
            bg = 'var(--touch)' if sel else 'transparent'; col = 'var(--acctext)' if today else 'var(--tx)'; wt = 700 if today else 400; ring = ''
        else:
            bg = 'var(--accfill)' if sel else 'transparent'; col = 'var(--onacc)' if sel else ('var(--acctext)' if today else 'var(--tx)'); wt = 500 if (sel or today) else 400
            ring = 'box-shadow:inset 0 0 0 1px var(--acc);' if today and not sel else ''
        dot = f'<span style="width:4px;height:4px;border-radius:2px;background:{"var(--neutral)" if d in has else "transparent"};margin-top:2px"></span>'
        cells.append(f'<div style="height:48px;display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:24px;background:{bg};{ring}color:{col};font-weight:{wt};font-size:{15 if v == "av" else 16}px" class="{"tn" if v == "ap" else ""}">{d}{dot}</div>')
    prev = ico('ic_retour', 18, 'var(--sec)', v) if v == 'av' else f'<span style="transform:scaleX(-1);display:flex">{ico("chevron", 18, "var(--next)", v, baked=False)}</span>'
    nxt = ico('chevron', 18, 'var(--sec)', v, baked=True) if v == 'av' else ico('chevron', 18, 'var(--next)', v, baked=False)
    if v == 'av':
        nxt = f'<span style="opacity:.4;display:flex">{ico("chevron", 18, "var(--sec)", v, baked=False)}</span>'
    head = f'<div class="row"><div class="ib">{prev}</div><div class="grow" style="text-align:center;font-size:16px;font-weight:500">Novembre 2026</div><div class="ib">{nxt}</div></div>'
    wd = ''.join(f'<div style="text-align:center;font-size:12px;color:var(--title)">{x}</div>' for x in 'LMMJVSD')
    top = (f'<div class="row" style="height:64px;padding:0 12px"><div class="switch"><div class="ib">{ico("ic_liste", 22, "var(--sec)", v)}</div><div class="ib" style="background:var(--touch)">{ico("ic_calendrier", 22, "var(--acc)" if v == "ap" else "var(--tx)", v)}</div></div><div class="grow"></div><div class="ib">{ico("ic_chercher", 22, "var(--sec)", v)}</div></div>')
    return f'{P(v, m)}<div class="scr" style="--h:470px">{top}<div style="padding:4px {12 + pad}px">{head}<div style="display:grid;grid-template-columns:repeat(7,1fr);margin:4px 0">{wd}</div><div style="display:grid;grid-template-columns:repeat(7,1fr)">{"".join(cells)}</div></div></div></div>'

def reply(v, who, t, said, kind_='them', initials='', me=False):
    color = {'me': 'var(--me)', 'them': 'var(--them)', 'v1': 'var(--v1)', 'v2': 'var(--v2)'}[kind_]
    fill = {'me': 'var(--mefill)', 'them': 'var(--themfill)', 'v1': 'var(--v1fill)', 'v2': 'var(--v2fill)'}[kind_]
    namec = color if me else 'var(--tx)'
    nsz = '15px' if v == 'av' else '14px'
    tsz = '13px' if v == 'av' else '14px'
    msz = '13px' if v == 'av' else '14px'
    return (f'<div class="line"><div class="mark" style="width:36px;height:36px;background:{fill};color:{color};font-size:{msz}">{initials}</div>'
            f'<div class="grow" style="margin-left:12px"><div class="row" style="align-items:baseline"><span class="med" style="font-size:{nsz};color:{namec}">{who}</span>'
            f'<span class="{"tn" if v == "ap" else ""}" style="font-size:{tsz};color:var(--at);margin-left:8px">{t}</span></div><div class="said" style="margin-top:2px">{said}</div></div></div>')

def player(v):
    if v == 'av':
        seek = '<div style="position:relative;height:26px;margin-top:-2px"><div style="position:absolute;left:0;right:0;top:12px;height:2px;background:var(--touch)"></div><div style="position:absolute;left:-8px;top:5px;width:16px;height:16px;border-radius:8px;background:var(--acctext);clip-path:inset(0 0 0 8px)"></div></div>'
        tm = '<div style="font-size:12px;color:var(--sec)">00:00 / 47:00</div>'
        btn = 44
    else:
        seek = '<div style="position:relative;height:48px;margin:-11px 0"><div style="position:absolute;left:8px;right:8px;top:23px;height:2px;background:var(--touch)"></div><div style="position:absolute;left:0;top:16px;width:16px;height:16px;border-radius:8px;background:var(--acc)"></div></div>'
        tm = '<div class="tn" style="font-size:12px;color:var(--sec);padding-left:8px">00:00 / 47:00</div>'
        btn = 48
    return (f'<div class="card row" style="margin:4px 12px 0;padding:10px 12px"><div style="width:{btn}px;height:{btn}px;border-radius:{btn / 2}px;background:var(--accfill);display:flex;align-items:center;justify-content:center;flex:none">{ico("ic_lire", 16, "var(--onacc)" if v == "ap" else "#fff", v)}</div>'
            f'<div class="grow" style="margin-left:12px">{seek}{tm}</div></div>')

def tools(v, which=('ic_chercher:Rechercher', 'ic_copier:Copier', 'ic_telecharger:Télécharger', 'ic_details:Détails'), disabled=(), big=False):
    out = []
    for w in which:
        n, lab = w.split(':')
        if lab in disabled and v == 'ap': continue
        op = 'opacity:.4;' if lab in disabled else ''
        label = '' if (big and v == 'ap') else f'<span style="font-size:{24 if big else 12}px;{"font-weight:500" if v == "ap" else ""}">{lab}</span>'
        out.append(f'<div class="tool" style="{op}">{ico(n, 22 if v == "av" else 24, "var(--tx)", v)}{label}</div>')
    radius = 24 if v == 'av' else 32
    return f'<div class="tools" style="border-radius:{radius}px">{"".join(out)}</div>'

def conversation(v, m):
    names = 'Sophie Marchand, Karim Benali' if v == 'av' else 'Sophie Marchand +1'
    lead = kind('ic_reunion', 'var(--kind)', 18, v)
    more = f'<div class="ib">{ico("ic_plus", 22, "var(--sec)", v)}</div>'
    body = (reply(v, 'Sophie Marchand', '00:04', 'On commence par la feuille de route. Où en est la page des réglages&#8239;?', 'them', 'SM') +
            reply(v, 'Moi', '00:11', 'Elle est prête, il reste les textes à relire.', 'me', 'M', True) +
            reply(v, 'Karim Benali', '00:19', 'Je peux m\'en occuper d\'ici lundi.', 'them', 'KB'))
    return f'{P(v, m)}<div class="scr" style="--h:560px">{bar("Point produit", f"<span class={chr(39)}tn{chr(39)}>23:57 · 47 min · {names}</span>" if v == "ap" else f"23:57 · 47 min · {names}", lead, more, v)}{player(v)}<div style="padding:14px 16px 108px">{body}</div>{tools(v)}</div></div>'

def reunion(v, m):
    lead = kind('ic_micro', 'var(--kind)', 18, v)
    i1 = 'V1' if v == 'av' else '1'; i2 = 'V2' if v == 'av' else '2'
    body = (reply(v, 'Moi', '00:04', 'On a eu quatorze livraisons en retard en octobre.', 'me', 'M', True) +
            reply(v, 'Voix 1', '00:12', 'Je sais. On a perdu deux chauffeurs sur la tournée de Lyon.', 'v1', i1) +
            reply(v, 'Voix 2', '00:19', 'Et les palettes arrivent mal filmées.', 'v2', i2) +
            reply(v, 'Voix 1', '00:26', 'Je vous mets un chauffeur dédié dès le 4 novembre.', 'v1', i1))
    return f'{P(v, m)}<div class="scr" style="--h:520px">{bar("Revue mensuelle · Transports Morel", "10:00 · 45 min", lead, more(v), v)}<div style="padding:14px 16px 108px">{body}</div>{tools(v)}</div></div>'

def direct(v, m):
    lead = kind('ic_micro', 'var(--live)', 18, v)
    det = ('10:02 · ● En cours · 12 min' if v == 'av' else '<span class="tn">10:02 · <span style="color:var(--live)">● En cours</span> · 12 min</span>')
    plate_bg = 'var(--btn)' if v == 'av' else 'var(--livefill)'
    b = bar('Réunion', '', None, None, v, detail_html=det)
    b = b.replace('<div class="grow" style="margin-left:4px">', f'<div class="plate" style="width:36px;height:36px;border-radius:{6.5 if v == "av" else 8}px;margin:0 6px 0 4px;background:{plate_bg}">{lead}</div><div class="grow" style="margin-left:4px">', 1)
    ind = 0 if v == 'av' else 48
    lines = ''.join(f'<div style="padding-left:{ind}px;padding-bottom:16px"><div class="{"tn" if v == "ap" else ""}" style="font-size:{13 if v == "av" else 14}px;color:var(--at)">{t}</div><div class="said" style="margin-top:2px;{c}">{s}</div></div>'
                    for t, s, c in [('10:02', 'on commence par le budget', ''), ('10:03', 'et la suite pour vendredi', ''), ('', 'il faudrait revoir', 'color:var(--sec)')])
    return f'{P(v, m)}<div class="scr" style="--h:330px">{b}<div style="padding:14px 16px">{lines}</div></div></div>'

def vide(v, m):
    lead = kind('ic_reunion', 'var(--kind)', 18, v)
    txt = f'<div style="text-align:center;padding:32px;font-size:{15 if v == "av" else 16}px;color:var(--sec)">Pas encore arrivée sur MacBook Air.</div>'
    return f'{P(v, m)}<div class="scr" style="--h:330px">{bar("Réunion", "10:02 · 10 min", lead, more(v), v)}{txt}{tools(v, disabled=("Copier", "Télécharger"))}</div></div>'

def reglages(v, m):
    t = THEMES[(m, v)]
    hp = 4 if v == 'av' else 16
    def radio(name, what, on=False, extra=''):
        rp = 10 if v == 'av' else 16; gp = 8 if v == 'av' else 0
        ring = f'<span style="width:20px;height:20px;border-radius:10px;box-shadow:inset 0 0 0 2px var(--acctext);display:flex;align-items:center;justify-content:center;flex:none;margin-top:2px">{"<span style=&quot;width:10px;height:10px;border-radius:5px;background:var(--acctext)&quot;></span>" if on else ""}</span>'
        return (f'<div style="display:flex;gap:{32 - 20 if v == "av" else 16}px;padding:12px {12}px 12px {rp + gp}px;align-items:center">{ring}<div><div>{name}</div><div style="font-size:14px;color:var(--sec);margin-top:2px">{what}</div>{extra}</div></div>')
    missing = (f'<div style="font-size:14px;color:var(--warn);margin-top:10px">Aucun calendrier relié&nbsp;: rien ne se déclenchera.</div>'
               f'<div style="font-size:14px;font-weight:500;color:var(--acctext);min-height:48px;display:flex;align-items:center">Relier un calendrier</div>')
    group = ('<div class="card" style="padding:4px 0">' + radio('Manuel', 'Quand vous touchez Enregistrer une réunion, ici ou sur le Mac.') +
             radio('Événements du calendrier', 'Pendant vos rendez-vous, une heure au plus.', True, missing) +
             radio('Tout le temps', 'Toute la journée, rangée dans le Journal. Les personnes autour sont enregistrées aussi.') + '</div>')
    cp = 12 if v == 'av' else 16
    calls = (f'<div class="card row" style="margin-top:8px;padding:8px {cp}px;min-height:48px"><div class="grow"><div>Enregistrer les appels</div><div style="font-size:{13 if v == "av" else 14}px;color:var(--sec);margin-top:2px">Tous les appels, téléphone ou app.</div></div>'
             f'<span style="width:36px;height:20px;border-radius:10px;background:var(--touch);position:relative;flex:none"><span style="position:absolute;left:2px;top:2px;width:16px;height:16px;border-radius:8px;background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.3)"></span></span></div>')
    ip = 4 if v == 'av' else 0; rp = 12 if v == 'av' else 16
    chev = f'<span style="display:flex;margin-left:6px">{ico("chevron", 16, "var(--chev)" if v == "ap" else "var(--sec)", v, baked=(v == "av"))}</span>' if v == 'ap' else f'<span style="display:flex;margin-left:6px;opacity:.4">{ico("chevron", 16, "var(--sec)" if m == "l" else "var(--sec)", v, baked=True)}</span>'
    integ = (f'<div class="card" style="padding:4px {ip}px">' + ''.join(
        f'<div class="row" style="min-height:48px;padding:0 8px 0 {rp}px"><div class="grow">{n}</div><span style="font-size:{15 if v == "av" else 14}px;color:{c}">{val}</span>{chev}</div>'
        for n, val, c in [('Calendrier', 'Non relié', 'var(--warn)'), ('Mac', 'MacBook Air', 'var(--sec)')]) + '</div>')
    head = lambda s, top: f'<div style="font-size:14px;font-weight:500;color:var(--title);padding:{top}px {hp}px 8px">{s}</div>'
    title = '<div class="one" style="font-size:17px">Réglages</div>' if v == 'av' else '<div class="one" style="font-size:16px;font-weight:500">Réglages</div>'
    return f'{P(v, m)}<div class="scr" style="--h:640px"><div class="bar"><div class="ib">{ico("ic_retour", 22, "var(--tx)", v)}</div><div style="margin-left:4px">{title}</div></div><div style="padding:4px 16px 24px">{head("Enregistrement", 12)}{group}{calls}{head("Intégrations", 24)}{integ}</div></div></div>'

def setup(v, m):
    nb = '&nbsp;' if v == 'ap' else ' '
    title = ('<div style="font-size:17px;font-weight:500;margin-top:14px">Aucun Mac relié</div>' if v == 'av' else '<div style="font-size:24px;line-height:32px;margin-top:16px">Aucun Mac relié</div>')
    txt = f'Sur le Mac{nb}: Réglages{nb}› Paramètres{nb}› Téléphones{nb}› Ajouter un téléphone.'
    return (f'{P(v, m)}<div class="scr" style="--h:420px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 32px">'
            f'<div style="width:64px;height:64px;border-radius:32px;background:#fff;display:flex;align-items:center;justify-content:center"><div style="width:22px;height:22px;border-radius:5px;background:linear-gradient(#8e8e93 0 52%,#c41e14 52% 56%,#2c2c2e 56%)"></div></div>'
            f'{title}<div style="font-size:{15 if v == "av" else 14}px;line-height:1.35;color:var(--sec);margin-top:14px;max-width:{318 if v == "av" else 300}px">{txt}</div>'
            f'<div style="margin-top:20px;height:48px;padding:0 20px;border-radius:24px;background:var(--accfill);color:var(--onacc);display:flex;align-items:center;gap:8px;font-weight:500">{ico("ic_scanner", 18, "var(--onacc)", v)}Scanner le code du Mac</div></div></div>')

def notification(v, m):
    t = THEMES[(m, v)]
    shade = '#E8EAED' if m == 'l' else '#121212'; card = '#FFFFFF' if m == 'l' else '#2B2B2E'; tx = '#202124' if m == 'l' else '#E8EAED'; sx = '#5F6368' if m == 'l' else '#AFB3B8'
    acc = '#0064D2'
    when = '14:02' if v == 'av' else '<span class="tn">12:34</span>'
    body = (f'<div style="font-size:15px;font-weight:500;color:{tx};margin-top:8px">Enregistre</div>' +
            (f'<div style="font-size:14px;color:{sx}">Depuis 14:02</div><div style="height:4px;border-radius:2px;background:rgba(0,100,210,.2);margin-top:10px;position:relative;overflow:hidden"><div style="position:absolute;left:28%;width:36%;top:0;bottom:0;background:{acc};border-radius:2px"></div></div>' if v == 'av' else '') +
            f'<div style="display:flex;gap:16px;margin-top:12px;font-size:14px;font-weight:500;color:{acc if m == "l" else "#8AB4F8"}">Arrêter</div>')
    return (f'<div class="ph {m} {v}" style="background:{shade}"><div class="scr" style="--h:170px;padding:16px">'
            f'<div style="background:{card};border-radius:24px;padding:14px 16px;color:{tx}"><div class="row" style="gap:8px;font-size:12px;color:{sx}"><span style="width:20px;height:20px;border-radius:10px;background:{acc};display:flex;align-items:center;justify-content:center">{ico("micro_notif", 14, "#fff", v)}</span>{"CallRecorder" if v == "av" else "Callrecorder"} · {when}</div>{body}</div></div></div>')

def toolbar200(v, m):
    return f'{P(v, m)}<div class="scr" style="--h:150px">{tools(v, big=True)}</div></div>'

def pastille(v, m):
    dot = 'var(--dot)'
    y = 36 if v == 'av' else 58
    sb = f'<div class="status" style="height:52px"><span>14:02</span><span style="width:16px;height:16px;border-radius:8px;background:#000"></span><span class="row" style="gap:6px"><span style="width:8px;height:8px;border-radius:4px;background:#1E8E3E"></span><span style="width:22px;height:11px;border-radius:3px;box-shadow:inset 0 0 0 1.5px var(--tx)"></span></span></div>'
    return (f'{P(v, m)}<div class="scr" style="--h:240px">{sb}<span style="position:absolute;right:12px;top:{y}px;width:12px;height:12px;border-radius:6px;background:{dot}"></span>'
            f'<div style="position:absolute;right:8px;top:120px;display:flex;background:var(--float);border-radius:24px;box-shadow:0 {2 if v == "av" else 3}px {6 if v == "av" else 10}px rgba(0,0,0,.25)"><div class="ib">{ico("ic_photo", 24, "var(--sec)", v)}</div><div class="ib">{ico("ic_arreter", 24, "var(--live)", v)}</div></div></div></div>')

SCREENS = [
    ('accueil', 'Accueil', lambda v, m: accueil(v, m), 'P13 traits, P14 logos, P21 « +1 », P24 choix Liste'),
    ('ecoute', 'Accueil en écoute', lambda v, m: accueil(v, m, 'ecoute'), 'P02 accent sombre'),
    ('encours', 'Accueil, enregistrement en cours', lambda v, m: accueil(v, m, 'enregistre'), 'P05 vignette en cours, P10 chiffres'),
    ('calendrier', 'Calendrier', calendrier, 'P12 flèches, aujourd\'hui (8) et jour choisi (6), P09 cellules'),
    ('conversation', 'Conversation', conversation, 'P04 lecteur, P07 heures, P21 « +1 », P23 tailles'),
    ('reunion', 'Réunion à plusieurs voix', reunion, 'P01 voix'),
    ('direct', 'Conversation en direct', direct, 'P05 « En cours », P15 retrait'),
    ('vide', 'Conversation sans texte', vide, 'P22 outils inutiles'),
    ('reglages', 'Réglages', reglages, 'P11 bords, P13 chevron, P02 accent'),
    ('setup', 'Mise en route', setup, 'P16 insécables, P23 titre'),
    ('notification', 'Notification d\'enregistrement', notification, 'P06 chronomètre'),
    ('pastille', 'Pastille et point des appels', pastille, 'P19 point rouge'),
    ('barre200', 'Barre du bas, texte à 200 %', toolbar200, 'P03'),
]

def build():
    b = ['<h1>Prototypes</h1><p class="lede">Chaque écran retouché, en HTML et CSS, avec les vraies valeurs : un pixel CSS vaut un dp (affiché ici à 62 %), les tailles, opacités, rayons et marges viennent de <code>Look.kt</code> et des écrans (avant) ou du <a href="systeme.html">système</a> (après), les icônes sont les tracés des fichiers <code>res/drawable</code>. De gauche à droite : avant clair, après clair, avant sombre, après sombre.</p>']
    b.append('<p class="small">Police : Roboto si elle est installée, sinon celle du système. Les captures du banc (<a href="inventaire.html#etats">Inventaire</a>) restent la référence de l\'avant.</p>')
    b.append('<ul class="toc">' + ''.join(f'<li><a href="#{k}">{t}</a> <span class="small">{r}</span></li>' for k, t, f, r in SCREENS) + '</ul>')
    for k, t, f, r in SCREENS:
        b.append(f'<h2 id="{k}">{t}</h2><p class="small">{r}</p><div class="protos">')
        for v, m, lab in (('av', 'l', 'Avant · clair'), ('ap', 'l', 'Après · clair'), ('av', 'd', 'Avant · sombre'), ('ap', 'd', 'Après · sombre')):
            b.append(f'<div><div class="pcap">{lab}</div>{f(v, m)}</div>')
        b.append('</div>')
    page('prototypes.html', 'Prototypes', '\n'.join(b), extra_css=PCSS + theme_css())
    return len(SCREENS) * 4

if __name__ == '__main__':
    print(build())

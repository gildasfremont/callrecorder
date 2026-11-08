"""Page « Prototypes » : chaque écran retouché, en HTML/CSS aux valeurs de Look.kt et du système proposé, 1 dp = 1 px,
avant (le banc) et après, en clair et en sombre."""
import os
from PIL import Image
from commun import *
from icones import sprite, ic

BANC = "phone/android/app/build/dossier"
H = 915  # hauteur montrée, en dp : tout l'écran du banc

def avant(nom):
    """Le rendu du banc, recadré aux H premiers dp, en WebP."""
    os.makedirs(f"{DOSSIER}/images/avant", exist_ok=True)
    src = f"{BANC}/{nom}.png"; dst = f"images/avant/{nom}.webp"
    if os.path.exists(src):
        im = Image.open(src).convert("RGB").crop((0, 0, 1236, H * 3))
        im.resize((618, H * 3 // 2), Image.LANCZOS).save(f"{DOSSIER}/{dst}", "WEBP", quality=90, method=6)
    return dst

CSS_TEL = """
<style>
.scene{background:var(--card);border-radius:14px;padding:18px 20px;margin:0 0 22px;scroll-margin-top:70px}
.scene h2{margin-top:0}
.rang{display:flex;flex-wrap:wrap;gap:14px;align-items:flex-start}
.cad{display:flex;flex-direction:column;gap:4px;font-size:12.5px;color:var(--sec)}
.cad>b{color:var(--text);font-weight:600}
.cad.apres>b{color:var(--good)}
.cad img{width:214px;height:476px;border-radius:12px;box-shadow:0 0 0 1px var(--line);display:block}
.z{zoom:.52;width:412px}
.tel{width:412px;height:915px;overflow:hidden;position:relative;border-radius:20px;box-shadow:0 0 0 1.6px var(--line);font-family:Roboto,"Roboto Flex",system-ui,sans-serif;
  display:flex;flex-direction:column;background:var(--t-bg);color:var(--t-ink);-webkit-font-smoothing:antialiased}
.tel.clair{--t-bg:#F5F5F5;--t-ink:#1D1D1F;--t-sec:rgba(0,0,0,.6);--t-title:rgba(0,0,0,.56);--t-mass:rgba(0,0,0,.05);--t-chip:rgba(0,0,0,.07);--t-sel:rgba(0,0,0,.12);--t-dis:rgba(0,0,0,.38);
  --t-acc:#0064D2;--t-on-acc:#FFFFFF;--t-me:#0057B8;--t-me-bg:rgba(0,100,210,.12);--t-them:#A0470A;--t-them-bg:rgba(160,71,10,.12);--t-live:#C41E14;--t-warn:#A0470A;--t-float:rgba(255,255,255,.94);--t-track:rgba(0,0,0,.5);
  --t-wa:#128C7E;--t-sig:#3B45FD;--t-tg:#1C7DB8;--t-meet:#00897B}
.tel.sombre{--t-bg:#1E1E1E;--t-ink:#F5F5F7;--t-sec:rgba(255,255,255,.62);--t-title:rgba(255,255,255,.62);--t-mass:rgba(255,255,255,.05);--t-chip:rgba(255,255,255,.07);--t-sel:rgba(255,255,255,.12);--t-dis:rgba(255,255,255,.38);
  --t-acc:#409CFF;--t-on-acc:#1E1E1E;--t-me:#409CFF;--t-me-bg:rgba(64,156,255,.12);--t-them:#FF9F0A;--t-them-bg:rgba(255,159,10,.12);--t-live:#FF453A;--t-warn:#FF9F0A;--t-float:rgba(44,44,46,.94);--t-track:rgba(255,255,255,.5);
  --t-wa:#25D366;--t-sig:#7A82FF;--t-tg:#26A5E4;--t-meet:#00897B}
.tel .ic{flex:none;display:block}
.tel .top{height:64px;flex:none;display:flex;align-items:center;padding:0 12px}
.tel .sw2{display:flex;background:var(--t-mass);border-radius:26px;padding:2px;gap:2px}
.tel .sw2 span{width:52px;height:48px;border-radius:24px;display:grid;place-items:center;color:var(--t-sec)}
.tel .sw2 span.on{background:var(--t-sel);color:var(--t-ink)}
.tel .ib{width:48px;height:48px;border-radius:24px;display:grid;place-items:center;color:var(--t-sec);flex:none}
.tel .sp{flex:1}
.tel .liste{flex:1;overflow:hidden;padding:4px 12px}
.tel .jour{font-size:14px;font-weight:500;color:var(--t-title);padding:12px 12px 6px}
.tel .ligne{display:flex;align-items:center;min-height:64px;padding:8px;gap:12px}
.tel .pl{width:44px;height:44px;border-radius:8px;background:var(--t-chip);display:grid;place-items:center;flex:none}
.tel .pl.acc{background:color-mix(in srgb,var(--t-acc) 12%,transparent);color:var(--t-acc)}
.tel .tx{min-width:0;flex:1}
.tel .t16{font-size:16px;line-height:22px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tel .t14{font-size:14px;line-height:20px;color:var(--t-sec);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-top:2px}
.tel .live{color:var(--t-live)}.tel .acc{color:var(--t-acc)}.tel .warn{color:var(--t-warn)}
.tel .pied{flex:none;padding:8px 12px 16px}
.tel .fr{display:flex;align-items:center;gap:8px;min-height:48px;padding:0 12px 0 8px;font-size:16px;color:var(--t-sec)}
.tel .vide{text-align:center;padding:40px 32px 0}
.tel .vide b{display:block;font-size:16px;font-weight:400;line-height:22px}
.tel .vide span{display:block;font-size:14px;line-height:20px;color:var(--t-sec);margin-top:4px}
.tel .bar{min-height:64px;flex:none;display:flex;align-items:center;padding:0 4px;gap:4px}
.tel .bar .ti{font-size:22px;line-height:28px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tel .bar .ti.c{font-size:16px;font-weight:500;line-height:22px}
.tel .bar .de{font-size:14px;line-height:20px;color:var(--t-sec);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tel .kp{width:36px;height:36px;border-radius:6.5px;background:var(--t-chip);display:grid;place-items:center;flex:none;margin:0 6px 0 4px}
.tel .lect{margin:4px 12px 0;background:var(--t-mass);border-radius:12px;padding:10px 12px;display:flex;align-items:center;gap:12px}
.tel .play{width:48px;height:48px;border-radius:24px;background:var(--t-acc);color:var(--t-on-acc);display:grid;place-items:center;flex:none}
.tel .piste{height:48px;display:flex;align-items:center;flex:1;position:relative}
.tel .piste i{display:block;height:4px;border-radius:2px;background:var(--t-track);width:100%}
.tel .piste i::before{content:"";position:absolute;left:0;top:22px;height:4px;width:11%;background:var(--t-acc);border-radius:2px}
.tel .piste i::after{content:"";position:absolute;left:calc(11% - 8px);top:16px;width:16px;height:16px;border-radius:8px;background:var(--t-acc)}
.tel .h12{font-size:12px;line-height:16px;color:var(--t-sec);font-variant-numeric:tabular-nums}
.tel .repl{padding:14px 16px 0;flex:1;overflow:hidden}
.tel .r{display:flex;gap:12px;padding-bottom:16px}
.tel .av{width:36px;height:36px;border-radius:18px;display:grid;place-items:center;font-size:13px;font-weight:500;flex:none}
.tel .av.me{background:var(--t-me-bg);color:var(--t-me)}.tel .av.them{background:var(--t-them-bg);color:var(--t-them)}
.tel .qui{display:flex;align-items:baseline;gap:8px}
.tel .qui b{font-size:14px;font-weight:500}
.tel .qui b.me{color:var(--t-me)}
.tel .dit{font-size:16px;line-height:1.38;margin-top:2px}
.tel .flot{position:absolute;left:50%;transform:translateX(-50%);bottom:24px;background:var(--t-float);border-radius:32px;padding:4px;display:flex;gap:0;box-shadow:0 3px 10px rgba(0,0,0,.18),0 1px 3px rgba(0,0,0,.12)}
.tel .outil{min-width:76px;height:56px;border-radius:28px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;font-size:12px;font-weight:500;color:var(--t-ink)}
.tel .outil.dis{color:var(--t-dis)}
.tel .capsule{display:flex;align-items:center;gap:4px}
.tel .stop{height:48px;border-radius:24px;background:var(--t-live);color:#fff;display:flex;align-items:center;gap:8px;padding:0 18px 0 14px;font-size:14px;font-weight:500;font-variant-numeric:tabular-nums;white-space:nowrap}
.tel .champ{display:flex;align-items:center;margin:8px 12px 0;background:var(--t-mass);border-radius:12px;min-height:48px;padding:0 6px 0 14px;font-size:16px}
.tel .champ .n{color:var(--t-sec);font-size:14px;margin-right:6px}
.tel .reg{padding:4px 16px 24px;flex:1;overflow:hidden}
.tel .gt{font-size:14px;font-weight:500;color:var(--t-title);padding:12px 4px 8px}
.tel .grp{background:var(--t-mass);border-radius:12px;padding:4px 4px 4px 8px}
.tel .rad{display:flex;gap:14px;padding:12px 12px 12px 10px;align-items:flex-start}
.tel .rond{width:20px;height:20px;border-radius:10px;border:2px solid var(--t-sec);flex:none;margin-top:1px}
.tel .rond.on{border-color:var(--t-acc);box-shadow:inset 0 0 0 3px var(--t-bg),inset 0 0 0 10px var(--t-acc)}
.tel .rad .n{font-size:16px;line-height:22px}.tel .rad .d{font-size:14px;line-height:20px;color:var(--t-sec)}
.tel .row{display:flex;align-items:center;min-height:48px;padding:8px 12px;gap:12px}
.tel .tog{width:52px;height:32px;border-radius:16px;background:var(--t-acc);position:relative;flex:none}
.tel .tog::after{content:"";position:absolute;right:4px;top:4px;width:24px;height:24px;border-radius:12px;background:var(--t-on-acc)}
.tel .tog.off{background:transparent;box-shadow:inset 0 0 0 2px var(--t-sec)}.tel .tog.off::after{left:8px;top:8px;width:16px;height:16px;background:var(--t-sec)}
.tel .tog.dim{opacity:.38}
.tel .chev{display:flex;align-items:center;min-height:48px;padding:0 8px 0 12px;font-size:16px}
.tel .chev .v{font-size:14px;color:var(--t-sec);margin-right:6px}
.tel .ombre{flex:1;background:#202124;padding:16px 10px}
.tel .notif{background:#2D2F31;color:#E3E3E3;border-radius:20px;padding:12px 14px;margin-bottom:8px;font-size:14px}
.tel .notif .h{display:flex;align-items:center;gap:6px;font-size:12px;color:#C4C7C5}
.tel .notif .h i{width:18px;height:18px;border-radius:9px;background:#0064D2;display:grid;place-items:center}
.tel .notif .t{font-size:15px;color:#E3E3E3;margin-top:4px}
.tel .notif .s{font-size:13.5px;color:#C4C7C5}
.tel .notif .pr{height:4px;border-radius:2px;background:rgba(168,199,250,.25);margin-top:8px;position:relative;overflow:hidden}
.tel .notif .pr::after{content:"";position:absolute;left:25%;width:30%;top:0;bottom:0;background:#A8C7FA;border-radius:2px}
.tel .notif .a{color:#A8C7FA;font-weight:500;margin-top:8px;font-size:14px}
.tel .sb{height:28px;flex:none;display:flex;align-items:center;justify-content:space-between;padding:0 18px;font-size:13px;color:#E3E3E3;background:#202124}
.tel .chip{background:#0064D2;color:#fff;border-radius:12px;padding:2px 9px;font-size:12px;font-weight:500;display:flex;gap:5px;align-items:center}
.tel .mois{display:grid;grid-template-columns:repeat(7,1fr);padding:0 8px}
.tel .mois span{height:48px;display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:16px}
.tel .mois span i{width:4px;height:4px;border-radius:2px;margin-top:2px;background:var(--t-title)}
.tel .mois span.sel b{width:40px;height:40px;border-radius:20px;background:var(--t-acc);color:var(--t-on-acc);display:grid;place-items:center;font-weight:500}
.tel .mois span.auj b{width:40px;height:40px;border-radius:20px;box-shadow:inset 0 0 0 1.5px var(--t-acc);color:var(--t-acc);display:grid;place-items:center}
.tel .mois span b{font-weight:400}
.tel .wd{font-size:12px!important;font-weight:500;color:var(--t-title);height:24px!important}
.tel .pastille{display:inline-flex;background:var(--t-float);border-radius:24px;box-shadow:0 3px 10px rgba(0,0,0,.2)}
.tel .pastille span{width:48px;height:48px;display:grid;place-items:center}
.tel.big .t16{font-size:28px;line-height:34px}.tel.big .t14{font-size:24px;line-height:30px}
.tel.big .bar .ti{font-size:30px;line-height:36px}.tel.big .bar .de{font-size:24px;line-height:30px}
.tel.big .dit{font-size:28px}.tel.big .qui b{font-size:24px}.tel.big .h12{font-size:20px;line-height:24px}
</style>
"""

def top(cal=False, recherche=None):
    if recherche is not None:
        return f'<div class="top"><span style="flex:1;font-size:16px;margin-left:8px">{e(recherche) or "<span style=\'color:var(--t-sec)\'>Rechercher</span>"}<span style="border-left:2px solid var(--t-acc);margin-left:1px"></span></span><span class="ib">{ic("ic_fermer", 22)}</span></div>'
    return (f'<div class="top"><div class="sw2"><span class="{"" if cal else "on"}">{ic("ic_liste", 22)}</span><span class="{"on" if cal else ""}">{ic("ic_calendrier", 22)}</span></div>'
            f'<span class="sp"></span><span class="ib">{ic("ic_chercher", 22)}</span></div>')

def ligne(titre, meta, icone="ic_reunion", couleur="var(--t-sec)", plate="", meta_cls=""):
    return f'<div class="ligne"><div class="pl {plate}">{ic(icone, 20, couleur)}</div><div class="tx"><div class="t16">{e(titre)}</div><div class="t14 {meta_cls}">{meta}</div></div></div>'

def pied(enreg=False, cache=False):
    if cache: return ""
    if enreg:
        return f'<div class="pied"><div class="fr live">{ic("ic_arreter", 24)}Arrêter l\'enregistrement</div><div class="fr">{ic("ic_photo", 24)}Prendre une photo</div></div>'
    return f'<div class="pied"><div class="fr">{ic("ic_enregistrer", 24)}Enregistrer une réunion</div><div class="fr">{ic("ic_reglages", 24)}Réglages</div></div>'

LISTE = [("Aujourd'hui · dimanche 8 novembre", [("Point produit", "13:23 · 47 min · Sophie Marchand, Karim Benali", "ic_reunion", "var(--t-sec)"), ("Café avec Thomas", "11:23 · 12 min · Thomas Girard", "ic_whatsapp", "var(--t-wa)")]),
         ("Hier · samedi 7 novembre", [("Paul Mercier · expert-comptable", "12:23 · 9 min · Paul Mercier", "ic_telephone", "var(--t-sec)")]),
         ("Vendredi 6 novembre", [("Conseil d'école", "12:23 · 2 h 41 · 2 voix", "ic_reunion", "var(--t-sec)")]),
         ("Jeudi 5 novembre", [("Claire Duval", "12:23 · 12 min · Claire Duval", "ic_signal", "var(--t-sig)")])]

def accueil(avant_liste="", vide=None, enreg=False, attente=False):
    h = [top(), '<div class="liste">', avant_liste]
    if vide:
        h.append(f'<div class="vide"><b>{e(vide[0])}</b>' + (f"<span>{e(vide[1])}</span>" if vide[1] else "") + "</div>")
    else:
        for j, (jour, ls) in enumerate(LISTE):
            h.append(f'<div class="jour" role="heading">{e(jour)}</div>')
            if j == 0 and enreg:
                h.append(ligne("Réunion", '14:23 · ● En cours · 12 min', "ic_micro", "var(--t-live)", meta_cls="live"))
            if j == 0 and attente:
                h.append(ligne("Réunion", "13:53 · 5 min · pas encore sur le Mac", "ic_reunion"))
            for t, m, i, col in ls: h.append(ligne(t, m, i, col))
    h.append("</div>")
    h.append(pied(enreg))
    return "".join(h)

def bar(titre, detail=None, icone=None, couleur="var(--t-sec)", plus=True, conv=True):
    lead = f'<div class="kp">{ic(icone, 18, couleur)}</div>' if icone else ""
    return (f'<div class="bar"><span class="ib" style="color:var(--t-ink)">{ic("ic_retour", 22)}</span>{lead}<div class="tx"><div class="ti{" c" if conv else ""}">{e(titre)}</div>' +
            (f'<div class="de">{detail}</div>' if detail else "") + f'</div>{"<span class=ib>" + ic("ic_plus", 22) + "</span>" if plus else ""}</div>')

REPL = [("SM", "Sophie Marchand", "00:04", "On commence par la feuille de route. Où en est la page des réglages ?", False),
        ("GF", "Moi", "00:11", "Elle est prête, il reste les textes à relire.", True),
        ("KB", "Karim Benali", "00:18", "Je peux m'en occuper d'ici lundi.", False)]

def repliques(lignes=REPL, sans_qui=False):
    h = ['<div class="repl">']
    for av, qui, t, dit, me in lignes:
        if sans_qui:
            h.append(f'<div class="r" style="display:block"><div class="h12">{t}</div><div class="dit">{e(dit)}</div></div>')
        else:
            h.append(f'<div class="r"><div class="av {"me" if me else "them"}">{av}</div><div><div class="qui"><b class="{"me" if me else ""}">{e(qui)}</b><span class="h12">{t}</span></div><div class="dit">{e(dit)}</div></div></div>')
    h.append("</div>")
    return "".join(h)

def outils(desactives=(), icones_seules=False):
    o = [("ic_chercher", "Rechercher"), ("ic_copier", "Copier"), ("ic_telecharger", "Télécharger"), ("ic_details", "Détails")]
    return '<div class="flot">' + "".join(f'<div class="outil{" dis" if n in desactives else ""}" style="{"min-width:56px" if icones_seules else ""}">{ic(i, 22)}{"" if icones_seules else e(n)}</div>' for i, n in o) + "</div>"

def conversation(big=False):
    return (bar("Point produit", "Dim. 1 nov. · 14:00 · 47 min · Sophie Marchand, Karim Benali", "ic_reunion") +
            f'<div class="lect"><span class="play">{ic("ic_lire", 22)}</span><span class="h12">05:12</span><span class="piste"><i></i></span><span class="h12">47:00</span></div>' +
            repliques() + outils(icones_seules=big))

def en_direct():
    return (bar("Réunion", '<span class="live">● En cours</span> · depuis 14:23', "ic_micro", "var(--t-live)", plus=False) +
            repliques([("", "", "14:23", "on commence par le budget", False), ("", "", "14:24", "et la suite pour vendredi", False)], sans_qui=True) +
            f'<div class="flot capsule"><span class="ib" style="color:var(--t-sec)">{ic("ic_photo", 22)}</span><span class="stop">{ic("ic_arreter", 20)}Arrêter · 12:34</span></div>')

def filtre():
    return (bar("Point produit", "Dim. 1 nov. · 14:00 · 47 min · Sophie Marchand, Karim Benali", "ic_reunion") +
            '<div class="champ"><span style="flex:1">budget</span><span class="n" aria-live="polite">0</span><span class="ib">' + ic("ic_fermer", 20) + '</span></div>' +
            '<div class="vide"><b>Aucune réplique</b></div>' + outils(desactives=("Copier", "Télécharger")))

def recherche(mot, resultats):
    h = [top(recherche=mot), '<div class="liste">']
    if not resultats:
        h.append(f'<div class="vide"><b>Aucun résultat pour « {e(mot)} »</b></div>')
    for t, d, i, col in resultats:
        h.append(f'<div class="ligne"><div class="pl">{ic(i, 20, col)}</div><div class="tx"><div class="t16">{e(t)}</div><div class="t14">{d}</div></div></div>')
    h.append("</div>")
    return "".join(h)

RES = [("Point produit", "Aujourd'hui · Je peux m'en occuper d'ici <b style='color:var(--t-ink);font-weight:500'>lundi</b>.", "ic_reunion", "var(--t-sec)"),
       ("Café avec Thomas", "Aujourd'hui · … d'ici <b style='color:var(--t-ink);font-weight:500'>lundi</b>.", "ic_whatsapp", "var(--t-wa)"),
       ("Paul Mercier · expert-comptable", "Hier · … d'ici <b style='color:var(--t-ink);font-weight:500'>lundi</b>.", "ic_telephone", "var(--t-sec)"),
       ("Claire Duval", "5 nov. · … d'ici <b style='color:var(--t-ink);font-weight:500'>lundi</b>.", "ic_signal", "var(--t-sig)")]

def calendrier():
    jours = "".join(f'<span class="wd">{d}</span>' for d in "LMMJVSD")
    cases = ['<span></span>'] * 6
    for n in range(1, 31):
        cls = "sel" if n == 5 else "auj" if n == 8 else ""
        pt = '<i></i>' if n in (4, 5, 6, 7, 8) else '<i style="background:transparent"></i>'
        cases.append(f'<span class="{cls}"><b>{n}</b>{pt}</span>')
    return (top(cal=True) + f'<div style="display:flex;align-items:center;padding:0 8px"><span class="ib">{ic("chevron", 18, style="transform:scaleX(-1)")}</span><span style="flex:1;text-align:center;font-size:16px;font-weight:500">Novembre 2026</span><span class="ib">{ic("chevron", 18)}</span></div>' +
            f'<div class="mois">{jours}{"".join(cases)}</div><div class="liste"><div class="jour">Jeudi 5 novembre</div>' + ligne("Claire Duval", "12:23 · 12 min · Claire Duval", "ic_signal", "var(--t-sig)") + "</div>" + pied())

def reglages(mode="agenda", manque=True, appels=False, mac="MacBook Air", mac_cls=""):
    def rad(code, nom, d, extra=""):
        return f'<div class="rad"><span class="rond{" on" if mode == code else ""}"></span><div><div class="n">{nom}</div><div class="d">{d}</div>{extra}</div></div>'
    miss = '<div class="d warn" style="margin-top:8px;color:var(--t-warn)">Aucun calendrier relié : rien ne se déclenchera.</div><div class="acc" style="font-size:14px;font-weight:500;min-height:48px;display:flex;align-items:center">Relier un calendrier</div>' if manque and mode == "agenda" else ""
    return (bar("Réglages", plus=False, conv=False) + '<div class="reg"><div class="gt" role="heading">Enregistrement</div><div class="grp">' +
            rad("manual", "Manuel", "Quand vous touchez Enregistrer une réunion, ici ou sur le Mac.") +
            rad("agenda", "Événements du calendrier", "Pendant vos rendez-vous, une heure au plus.", miss) +
            rad("active", "Tout le temps", "Toute la journée, rangée dans le Journal. Les personnes autour sont enregistrées aussi.") + "</div>" +
            f'<div class="grp" style="margin-top:8px;padding:0"><div class="row"><div class="tx"><div style="font-size:16px">Enregistrer les appels</div><div class="t14" style="white-space:normal">Votre voix, pendant les appels du téléphone et des apps.{" Éteint en Manuel." if mode == "manual" else ""}</div></div><span class="tog{"" if appels else " off"}{" dim" if mode == "manual" else ""}"></span></div></div>' +
            '<div class="gt" role="heading" style="padding-top:24px">Intégrations</div><div class="grp" style="padding:4px">' +
            f'<div class="chev"><span style="flex:1">Calendrier</span><span class="v">{"Non relié" if manque else "MacBook Air"}</span>{ic("chevron", 16, "var(--t-sec)")}</div>' +
            f'<div class="chev"><span style="flex:1">Mac</span><span class="v {mac_cls}">{e(mac)}</span>{ic("chevron", 16, "var(--t-sec)")}</div></div></div>')

def notification(verrou=False):
    corps = ('<div class="notif"><div class="h"><i>' + ic("micro_notif", 12, "#fff") + '</i>Callrecorder · <span style="font-variant-numeric:tabular-nums">12:34</span></div>'
             '<div class="t">Point produit</div><div class="s">Enregistrement</div><div class="pr"></div><div class="a">Arrêter</div></div>')
    if verrou:
        return ('<div class="sb"><span>14:36</span><span class="chip">● 12:34</span></div><div class="ombre" style="background:#101418;display:flex;flex-direction:column;justify-content:flex-end;padding-bottom:120px">'
                '<div style="text-align:center;color:#E3E3E3;font-size:64px;font-weight:300;margin-bottom:auto;margin-top:60px">14:36</div>'
                '<div class="notif"><div class="h"><i>' + ic("micro_notif", 12, "#fff") + '</i>Callrecorder · 12:34</div><div class="t">Enregistrement</div><div class="pr"></div></div></div>')
    return '<div class="sb"><span>14:36</span><span class="chip">● 12:34</span></div><div class="ombre">' + corps + "</div>"

def notif_avant():
    return ('<div class="sb"><span>14:36</span><span></span></div><div class="ombre"><div class="notif"><div class="h"><i>' + ic("micro_notif", 12, "#fff") + '</i>CallRecorder · 14:02</div>'
            '<div class="t">Enregistre</div><div class="s">Depuis 14:02</div><div class="pr"></div><div class="a">Arrêter</div></div></div>')

def pastille(etat="enreg"):
    if etat == "arrete":
        p = '<div class="pastille" style="padding:0 6px 0 16px;align-items:center;gap:6px;font-size:14px"><span style="width:auto;color:var(--t-sec)">Arrêté</span><span style="width:auto;padding:0 12px;color:var(--t-acc);font-weight:500">Reprendre</span></div>'
    else:
        p = f'<div class="pastille"><span style="color:var(--t-sec)">{ic("ic_photo", 22)}</span><span style="color:var(--t-live)">{ic("ic_arreter", 22)}</span></div>'
    return f'<div style="flex:1;background:repeating-linear-gradient(135deg,var(--t-mass) 0 12px,transparent 12px 24px);position:relative"><div style="position:absolute;right:8px;top:260px">{p}</div></div>'

def tel(contenu, theme, big=False):
    return f'<div class="z"><div class="tel {theme}{" big" if big else ""}">{contenu}</div></div>'

def scene(id_, titre, pbs, avants, apres, note="", avants_html=()):
    h = [f'<section class="scene" id="{id_}"><h2>{e(titre)}</h2><p style="color:var(--sec)">Problèmes : ' + ", ".join(f'<a href="problemes.html#{p}">{p}</a>' for p in pbs) + "</p>"]
    if note: h.append(f'<p class="note">{note}</p>')
    h.append('<div class="rang">')
    for nom, lg in avants:
        h.append(f'<div class="cad"><b>Avant · {e(lg)}</b><img src="{avant(nom)}" alt="Avant : {e(lg)}" loading="lazy"></div>')
    for contenu, lg, theme in avants_html:
        h.append(f'<div class="cad"><b>Avant · {e(lg)}</b>{tel(contenu, theme)}</div>')
    for contenu, lg, theme, big in apres:
        h.append(f'<div class="cad apres"><b>Après · {e(lg)}</b>{tel(contenu, theme, big)}</div>')
    h.append("</div></section>")
    return "".join(h)

def construire():
    A = lambda ec, et, conf="clair-100": f"{ec}--{et}--{conf}"
    c = [sprite(), CSS_TEL, '<link rel="preconnect" href="https://fonts.gstatic.com"><link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">',
         "<h1>Prototypes : les écrans retouchés, aux vraies valeurs, avant et après, en clair et en sombre</h1>",
         """<p class="lead">Chaque « après » est du HTML/CSS à 1 dp = 1 px (affiché à 52 %), avec la police Roboto, les couleurs de <code>Look.kt</code> corrigées par le <a href="systeme.html">système proposé</a>, les icônes tirées des vecteurs de l'app (<code>res/drawable</code>) et les textes proposés. Chaque « avant » est le rendu du banc d'inventaire, sur tout l'écran (412 × 915 dp). Les notifications et l'écran verrouillé sont dessinés par Android : leur prototype imite un Pixel, il n'est fidèle qu'au contenu.</p>"""]
    c.append(scene("accueil-vide", "Accueil : la liste, vide, et la recherche sans résultat", ["P01", "P13"],
        [(A("accueil", "vide"), "accueil vide"), (A("accueil", "recherche-sans-resultat"), "recherche sans résultat")],
        [(accueil(vide=("Aucune conversation", "Le prochain rendez-vous s'enregistrera seul.")), "vide, clair", "clair", False),
         (accueil(vide=("Aucune conversation", "Le prochain rendez-vous s'enregistrera seul.")), "vide, sombre", "sombre", False),
         (recherche("facture", []), "sans résultat, clair (pied caché)", "clair", False), (recherche("facture", []), "sans résultat, sombre", "sombre", False)]))
    c.append(scene("recherche", "Recherche : la date et le mot trouvé", ["P13"], [(A("accueil", "recherche-resultats"), "résultats")],
        [(recherche("lundi", RES), "clair", "clair", False), (recherche("lundi", RES), "sombre", "sombre", False)]))
    c.append(scene("liste", "Accueil : « Hier », la conversation en attente, l'enregistrement en cours", ["P07", "P13", "P02"],
        [(A("accueil", "en-attente-du-mac"), "en attente du Mac"), (A("accueil", "enregistrement"), "enregistrement")],
        [(accueil(attente=True), "en attente, clair", "clair", False), (accueil(enreg=True), "enregistrement (ligne touchable), sombre", "sombre", False)]))
    c.append(scene("en-direct", "Conversation en cours : Arrêter là où l'on regarde", ["P02"],
        [(A("conversation", "en-direct"), "en direct, clair"), (A("conversation", "en-direct", "sombre-100"), "en direct, sombre")],
        [(en_direct(), "clair", "clair", False), (en_direct(), "sombre", "sombre", False)]))
    c.append(scene("conversation", "Conversation : jour dans l'en-tête, Lire en 48 dp, piste visible, heures lisibles, « GF »", ["P08", "P10", "P13", "P18"],
        [(A("conversation", "transcrite-avec-son"), "clair"), (A("conversation", "transcrite-avec-son", "sombre-100"), "sombre")],
        [(conversation(), "clair", "clair", False), (conversation(), "sombre", "sombre", False)]))
    c.append(scene("filtre", "Conversation : le filtre compte, et dit « aucune »", ["P01", "P09"], [(A("conversation", "filtre-sans-resultat"), "filtre sans résultat")],
        [(filtre(), "clair", "clair", False), (filtre(), "sombre", "sombre", False)], note="Copier et Télécharger désactivés (et annoncés comme tels) quand rien n'est affiché."))
    c.append(scene("police", "Police à 200 % : l'en-tête grandit, la barre passe en icônes", ["P04"], [(A("conversation", "transcrite-avec-son", "clair-200"), "200 %")],
        [(conversation(big=True), "200 %, clair", "clair", True), (conversation(big=True), "200 %, sombre", "sombre", True)],
        note="Tailles du prototype : celles qu'Android 14 donne à 200 % (16 sp → 28 dp environ, courbe non linéaire). Les mots de la barre restent dans la description et l'info-bulle."))
    c.append(scene("sombre", "Sombre : l'accent #409CFF, le jour choisi plein", ["P03", "P08", "P21"],
        [(A("accueil", "calendrier", "sombre-100"), "calendrier, sombre"), (A("accueil", "ecoute", "sombre-100"), "écoute, sombre")],
        [(calendrier(), "calendrier, sombre", "sombre", False), (accueil(avant_liste=ligne("Journal", "● Écoute depuis 08:12", "ic_onde", "var(--t-acc)", plate="acc", meta_cls="acc")), "écoute, sombre", "sombre", False),
         (calendrier(), "calendrier, clair", "clair", False)]))
    c.append(scene("reglages", "Réglages : ronds par état, une seule alerte, le Mac qui dit son état, le texte des appels", ["P05", "P07", "P16"],
        [(A("reglages", "calendrier-sans-calendrier"), "sans calendrier"), (A("reglages", "manuel", "sombre-100"), "manuel, sombre")],
        [(reglages(), "sans calendrier, clair", "clair", False), (reglages(mode="manual", manque=False, appels=True, mac="2 en attente", mac_cls="warn"), "manuel, Mac injoignable, sombre", "sombre", False),
         (reglages(mode="active", manque=False, appels=True), "tout le temps, appels allumés, clair", "clair", False)]))
    c.append(scene("notification", "Notification d'enregistrement : la conversation, le temps, l'écran verrouillé", ["P06"], [],
        [(notification(), "volet", "sombre", False), (notification(verrou=True), "écran verrouillé", "sombre", False)],
        note="Dessin indicatif d'un Pixel : Android dessine la notification ; la pastille « ● 12:34 » de la barre d'état est la mise en avant d'Android 16 (Live Update), en bleu (couleur de la notification), sans rouge de l'app.", avants_html=[(notif_avant(), "volet (textes lus dans le code)", "sombre")]))
    c.append(scene("pastille", "Pastille : quatre secondes pour reprendre", ["P15"], [],
        [(pastille(), "pendant l'enregistrement (inchangée)", "clair", False), (pastille("arrete"), "4 s après Arrêter, clair", "clair", False), (pastille("arrete"), "4 s après Arrêter, sombre", "sombre", False)]))
    page("prototypes.html", "Prototypes UX Android", "\n".join(c), "Écrans retouchés en HTML/CSS aux vraies valeurs, avant/après, clair et sombre.")

if __name__ == "__main__":
    construire()

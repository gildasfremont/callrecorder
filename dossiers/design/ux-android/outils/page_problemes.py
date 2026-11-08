"""Page « Problèmes et recos »."""
from commun import *
from problemes import P, R, GRAV, FREQ

def ref(k):
    t, u = R[k]
    return f'<a href="{e(u)}">{e(t)}</a>'

def bloc_spec(spec):
    out = []
    for ou, avant, apres in spec:
        out.append(f"<h4><code>{e(ou)}</code></h4><pre>" +
                   ("".join(f'<span class="del">− {e(l)}</span>' for l in avant.split("\n")) if avant and avant != "—" else "") +
                   ("".join(f'<span class="add">+ {e(l)}</span>' for l in apres.split("\n")) if apres else "") + "</pre>")
    return "\n".join(out)

def construire():
    tri = sorted(P, key=lambda x: (-x["score"], x["id"]))
    c = [f"<h1>Problèmes et recos : {len(P)} problèmes, chacun prouvé, chiffré et spécifié</h1>",
         """<p class="lead">Pour chaque problème : le symptôme, sa preuve (capture annotée ou mesure), sa cause dans le code, son impact, deux ou trois options avec leurs pour et contre, le choix et sa raison, la règle qui le fonde, ce qui touche à un choix déjà tranché, la spécification (fichier:ligne, avant → après) et des critères d'acceptation vérifiables. Les numéros de ligne sont ceux de la branche <code>recos-design</code> (7 novembre 2026).</p>""",
         "<p>Score = gravité (3 bloque ou trompe, 2 gêne, 1 détail) × fréquence (3 à chaque usage, 2 souvent, 1 rarement). Le tableau est trié par score.</p>"]
    c.append(tableau(["N°", "Problème", "Gravité", "Fréquence", "Score", "Effort", "Lot"],
                     [[f'<a href="#{x["id"]}">{x["id"]}</a>', e(x["titre"]), GRAV[x["gravite"]], FREQ[x["frequence"]], f"<b>{x['score']}</b>", x["effort"], f'<a href="plan.html#{x["lot"]}">{x["lot"]}</a>'] for x in tri], brut=True))
    for x in sorted(P, key=lambda x: x["id"]):
        h = [f'<section class="pb" id="{x["id"]}"><h2>{x["id"]}. {e(x["titre"])}</h2>']
        h.append('<div>' + f'<span class="tag {"g" if x["gravite"] >= 2 else "d"}">{GRAV[x["gravite"]]}</span>' + f'<span class="tag">{FREQ[x["frequence"]]}</span>' +
                 f'<span class="tag">score {x["score"]}</span><span class="tag">{e(x["effort"])}</span><span class="tag">lot {x["lot"]}</span>' +
                 "".join(f'<span class="tag">{e(a)}</span>' for a in x["axes"]) + (f'<span class="tag c">touche un choix tranché</span>' if x["tranche"] else "") + "</div>")
        h.append("<dl>")
        h.append(f"<dt>Symptôme</dt><dd>{x['symptome']}</dd>")
        h.append(f"<dt>Preuve</dt><dd>{x['mesures']}</dd>")
        h.append(f"<dt>Cause</dt><dd>{x['cause']}</dd>")
        h.append(f"<dt>Impact</dt><dd>{x['impact']}</dd>")
        h.append("</dl>")
        if x["preuves"]:
            h.append('<div class="preuves">' + "".join(f'<figure><img src="{im}" alt="{e(lg)}" loading="lazy"><figcaption>{e(lg)}</figcaption></figure>' for im, lg in x["preuves"]) + "</div>")
        h.append("<h3>Options</h3><div class=\"opts\">")
        for titre, pour, contre, choisi in x["options"]:
            h.append(f'<div class="opt{" choisi" if choisi else ""}"><h5>{e(titre)}{" · retenue" if choisi else ""}</h5><ul>' +
                     "".join(f"<li>+ {e(a)}</li>" for a in pour) + "".join(f"<li>− {e(a)}</li>" for a in contre) + "</ul></div>")
        h.append("</div>")
        h.append(f"<p><b>Choix.</b> {x['choix']}</p>")
        h.append("<p><b>Règle.</b> " + " · ".join(ref(k) for k in x["refs"]) + "</p>")
        if x["tranche"]:
            h.append(f'<p class="note choix"><b>Choix déjà tranché.</b> {e(x["tranche"])}</p>')
        if x["proto"]:
            h.append(f'<p><a href="prototypes.html#{x["proto"]}">Voir le prototype →</a></p>')
        h.append("<details><summary>Spécification (avant → après)</summary>" + bloc_spec(x["spec"]) + "</details>")
        h.append('<h4>Critères d\'acceptation</h4><ul class="crit">' + "".join(f"<li>{k}</li>" for k in x["criteres"]) + "</ul>")
        h.append("</section>")
        c.append("\n".join(h))
    page("problemes.html", "Problèmes et recos UX Android", "\n".join(c), "24 problèmes de l'app Android : preuve, cause, options, choix, spécification, critères.")

if __name__ == "__main__":
    construire()

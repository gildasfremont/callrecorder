#!/usr/bin/env python3
"""Arrête une livraison qui remet un texte qu'un commit récent avait retiré exprès.

Le 6 novembre 2026, une relecture des textes a remis sur l'accueil du site le titre long, que Gildas avait raccourci le
3 novembre : elle suivait un exemple périmé, et rien ne le lui a dit. Ce contrôle le dit. Pour chaque ligne de texte que
la livraison ajoute, il cherche dans l'histoire récente de la base un commit qui l'avait retirée. S'il en trouve un, il
s'arrête et le nomme.

Revenir en arrière reste possible quand c'est voulu (Gildas l'a demandé, ou le retrait était une erreur) : l'un des commits
livrés le dit dans son message, par « Revient sur <hash> » suivi de la raison.

    python3 scripts/retours.py                       la branche courante contre origin/main, dans ce dépôt
    python3 scripts/retours.py --base A --tete B     deux références quelconques
    python3 scripts/retours.py --depot <dossier>     un autre dépôt (le site public, par exemple)

Code 0 : rien qui revient. Code 1 : des textes reviennent, la liste dit lesquels et d'où.
Seules comptent les lignes de texte : pages du site, Markdown, et chaînes d'au moins quatre mots dans le code.
"""
import argparse, re, subprocess, sys

JOURS = 60
MOTS = re.compile(r"[A-Za-zÀ-ÿ'’]{2,}")
CHAINE = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')


def git(depot, *args):
    return subprocess.run(["git", "-C", depot, *args], capture_output=True, text=True, errors="replace").stdout


def norme(t):
    return re.sub(r"\s+", " ", t.replace("’", "'").replace("&nbsp;", " ").replace(" ", " ").replace(" ", " ")).strip()


def texte(fichier, ligne):
    """Le texte qu'un lecteur verra dans cette ligne, ou None."""
    if fichier.endswith((".html", ".md", ".txt")):
        t = re.sub(r"<[^>]*>", " ", ligne)
    elif fichier.endswith((".swift", ".kt", ".py", ".js", ".xml", ".json")):
        if ligne.lstrip().startswith(("//", "#", "*", "///")):
            return None
        t = " ".join(CHAINE.findall(ligne))
    else:
        return None
    return t if len(MOTS.findall(t)) >= 4 else None


def ajoutees(depot, base, tete):
    out, fichier = [], ""
    for l in git(depot, "diff", "-U0", f"{base}...{tete}").splitlines():
        if l.startswith("+++ "):
            fichier = l[6:] if l.startswith("+++ b/") else ""
        elif l.startswith("+") and fichier and not l.startswith("+++"):
            if texte(fichier, l[1:]):
                out.append((fichier, l[1:].strip()))
    return out


def morceau(ligne):
    """Le plus long passage de la ligne sans apostrophe ni espace insécable : il se cherche tel quel dans l'histoire."""
    return max(re.split(r"['’\u00a0\u202f]|&nbsp;", ligne.strip()), key=len)


def retires(depot, base, fichier, ligne):
    """Les commits récents de la base qui ont retiré cette ligne."""
    cherche = norme(ligne)
    out = []
    for h in git(depot, "log", f"--since={JOURS}.days", "--format=%h", "-S", morceau(ligne), base, "--", fichier).split():
        for l in git(depot, "show", "--format=", "-U0", h, "--", fichier).splitlines():
            if l.startswith("-") and not l.startswith("---") and norme(l[1:]) == cherche:
                out.append(h)
                break
    return out


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--depot", default=".")
    a.add_argument("--base", default="origin/main")
    a.add_argument("--tete", default="HEAD")
    o = a.parse_args()
    voulus = set(re.findall(r"[Rr]evient sur ([0-9a-f]{7,40})", git(o.depot, "log", "--format=%B", f"{o.base}..{o.tete}")))
    trouves = []
    for fichier, ligne in ajoutees(o.depot, o.base, o.tete):
        for h in retires(o.depot, o.base, fichier, ligne):
            if not any(h.startswith(v[:7]) or v.startswith(h) for v in voulus):
                trouves.append((h, fichier, ligne))
    if not trouves:
        return 0
    print("✗ Des textes retirés récemment reviennent. Un commit les avait changés exprès, peut-être à la demande de Gildas :", file=sys.stderr)
    for h in sorted({t[0] for t in trouves}):
        sujet = git(o.depot, "log", "-1", "--format=%ad %s", "--date=format:%d/%m", h).strip()
        print(f"\n  {h} {sujet}", file=sys.stderr)
        for _, fichier, ligne in [t for t in trouves if t[0] == h][:5]:
            print(f"    revient dans {fichier} : {ligne[:140]}", file=sys.stderr)
    print("\nGarder le texte d'aujourd'hui, sauf si le retour est voulu : l'écrire alors dans le message d'un commit,"
          " « Revient sur <hash> : <raison> ».", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

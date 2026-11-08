"""Les icônes de l'app (res/drawable/*.xml, vecteurs Android) converties en symboles SVG, pour des prototypes fidèles."""
import glob, os, re

def sprite():
    out = ['<svg width="0" height="0" style="position:absolute" aria-hidden="true">']
    for f in sorted(glob.glob("phone/android/app/src/main/res/drawable/*.xml")):
        x = open(f, encoding="utf-8").read()
        vw = re.search(r'viewportWidth="([\d.]+)"', x).group(1); vh = re.search(r'viewportHeight="([\d.]+)"', x).group(1)
        paths = []
        for p in re.findall(r"<path\b(.*?)/>", x, re.S):
            d = re.search(r'pathData="([^"]+)"', p).group(1)
            fill = re.search(r'fillColor="#(\w+)"', p); stroke = re.search(r'strokeColor="#(\w+)"', p)
            sw = re.search(r'strokeWidth="([\d.]+)"', p)
            cap = re.search(r'strokeLineCap="(\w+)"', p); join = re.search(r'strokeLineJoin="(\w+)"', p)
            a = [f'd="{d}"']
            a.append('fill="currentColor"' if fill and not fill.group(1).startswith("00") else 'fill="none"')
            if stroke and not stroke.group(1).startswith("00"):
                a.append(f'stroke="currentColor" stroke-width="{sw.group(1) if sw else 1}"')
                if cap: a.append(f'stroke-linecap="{cap.group(1)}"')
                if join: a.append(f'stroke-linejoin="{join.group(1)}"')
            paths.append("<path " + " ".join(a) + "/>")
        out.append(f'<symbol id="{os.path.basename(f)[:-4]}" viewBox="0 0 {vw} {vh}">' + "".join(paths) + "</symbol>")
    out.append("</svg>")
    return "\n".join(out)

def ic(nom, taille=24, couleur="currentColor", style=""):
    return f'<svg class="ic" width="{taille}" height="{taille}" style="color:{couleur};{style}" aria-hidden="true"><use href="#{nom}"/></svg>'

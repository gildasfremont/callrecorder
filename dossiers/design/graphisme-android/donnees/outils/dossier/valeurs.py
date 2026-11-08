"""Les valeurs actuelles de l'app (Look.kt et usages), et les contrastes des éléments non textuels."""
import csv
from commun import *

def ink(a, dark): return '#%02X%s' % (round(a * 255), 'FFFFFF' if dark else '000000')

def palette(dark):
    return {
        'page': '#FF1E1E1E' if dark else '#FFF5F5F5',
        'text': '#FFF5F5F7' if dark else '#FF1D1D1F',
        'secondary': ink(0.62 if dark else 0.6, dark),
        'title': ink(0.62 if dark else 0.56, dark),
        'card': ink(0.05, dark), 'button': ink(0.07, dark), 'touch': ink(0.12, dark),
        'floating': '#F02C2C2E' if dark else '#F0FFFFFF',
        'ACCENT': '#FF0064D2',
        'INFO': '#FF409CFF' if dark else '#FF0064D2',
        'WARNING': '#FFFF9F0A' if dark else '#FFA0470A',
        'LIVE': '#FFFF453A' if dark else '#FFC41E14',
        'OK': '#FF32D74B' if dark else '#FF147333',
    }

def alpha_of(hexc_, a):
    """Une couleur #AARRGGBB dont on multiplie l'opacité par a."""
    h = hexc_.lstrip('#')
    return '#%02X%s' % (round(int(h[:2], 16) * a), h[2:])

def plate(color, a=0x1F / 255):
    return alpha_of(color, a)

# (rôle, où, premier plan, fond (sur la page), règle)
def non_text(dark):
    p = palette(dark)
    card = p['card']
    def onplate(c): return c
    L = [
        ('Icône au texte (Retour, Liste, barre du bas)', 'Screen.kt:110, ConversationScreen.kt:177', p['text'], None, '1.4.11'),
        ('Icône secondaire (Rechercher, pied, Calendrier)', 'HomeScreen.kt:61,76,232-235', p['secondary'], None, '1.4.11'),
        ('Mois précédent (ic_retour, teinte secondaire)', 'HomeScreen.kt:283', p['secondary'], None, '1.4.11'),
        ('Mois suivant (chevron : 40 % gravé × teinte secondaire)', 'HomeScreen.kt:285, chevron.xml:10', alpha_of(p['secondary'], 0.4), None, '1.4.11'),
        ('Chevron des Réglages (40 % gravé × ink 0,4)', 'Screen.kt:148, chevron.xml:10', alpha_of(ink(0.4, dark), 0.4), card, '1.4.11'),
        ('Point d\'un jour qui a une conversation (ink 0,45)', 'HomeScreen.kt:318', ink(0.45, dark), None, '1.4.11'),
        ('Vignette : icône neutre (ink 0,55) sur masse 0,07', 'Screen.kt:89, HomeScreen.kt:268', ink(0.55, dark), p['button'], '1.4.11'),
        ('Vignette : WhatsApp #25D366 sur masse 0,07', 'Screen.kt:85', '#FF25D366', p['button'], '1.4.11'),
        ('Vignette : Signal #3B45FD sur masse 0,07', 'Screen.kt:86', '#FF3B45FD', p['button'], '1.4.11'),
        ('Vignette : Telegram #26A5E4 sur masse 0,07', 'Screen.kt:87', '#FF26A5E4', p['button'], '1.4.11'),
        ('Vignette : Meet #00897B sur masse 0,07', 'Screen.kt:88', '#FF00897B', p['button'], '1.4.11'),
        ('Vignette en cours : micro LIVE sur masse 0,07', 'HomeScreen.kt:243', p['LIVE'], p['button'], '1.4.11'),
        ('Journal : onde ACCENT sur masse ACCENT 12 %', 'HomeScreen.kt:241-253', p['ACCENT'], plate(p['ACCENT']), '1.4.11'),
        ('Rond des modes (RadioButton, ACCENT) sur carte', 'SettingsScreen.kt:38', p['ACCENT'], card, '1.4.11'),
        ('Curseur du lecteur (ACCENT) sur carte', 'ConversationScreen.kt:87-88', p['ACCENT'], card, '1.4.11'),
        ('Piste du lecteur (ink 0,12) sur carte', 'ConversationScreen.kt:89', ink(0.12, dark), card, 'décor'),
        ('Lire : icône blanche sur ACCENT', 'ConversationScreen.kt:274', '#FFFFFFFF', p['ACCENT'], '1.4.11'),
        ('Pastille : Prendre une photo (secondaire) sur verre', 'Pastille.kt:44', p['secondary'], p['floating'], '1.4.11'),
        ('Pastille : Arrêter (LIVE) sur verre', 'Pastille.kt:45', p['LIVE'], p['floating'], '1.4.11'),
        ('Bouton de liste choisi : masse 0,12 contre la capsule 0,05', 'HomeScreen.kt:66,113', p['touch'], p['card'], '1.4.11 (état)'),
        ('Jour choisi : masse 0,12 sur la page', 'HomeScreen.kt:312', p['touch'], None, '1.4.11 (état)'),
        ('Carte (0,05) contre la page', 'Look.kt:28', p['card'], None, 'repère'),
    ]
    out = []
    for role, ou, fg, bg, regle in L:
        # fond : bg composé sur la page ; premier plan composé sur ce fond
        b = over(parse(bg), parse(p['page'])) if bg else parse(p['page'])
        if role.startswith(('Bouton de liste choisi', 'Jour choisi', 'Carte')):
            # un fond contre un autre fond
            f = over(parse(fg), parse(p['page']))
            b = over(parse(bg), parse(p['page'])) if bg else parse(p['page'])
        else:
            f = over(parse(fg), b)
        r = wcag(f, b)
        out.append({'mode': 'sombre' if dark else 'clair', 'role': role, 'ou': ou, 'premier_plan': hexc(f), 'fond': hexc(b),
                    'wcag': round(r, 2), 'requis': 3.0 if regle.startswith('1.4.11') else '', 'ok': (r >= 3.0) if regle.startswith('1.4.11') else '',
                    'apca_lc': round(abs(apca(f, b)), 1), 'regle': regle})
    return out

def write_non_text():
    data = non_text(False) + non_text(True)
    with open(f'{D}/mesures-contrastes-non-texte.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, list(data[0].keys())); w.writeheader(); w.writerows(data)
    return data

if __name__ == '__main__':
    for r in write_non_text(): print(r['mode'], r['role'][:50], r['premier_plan'], r['fond'], r['wcag'], r['ok'], r['apca_lc'])

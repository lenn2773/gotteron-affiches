
import re
import urllib.request
from html.parser import HTMLParser

URL = "https://www.sihf.ch"

class LiensParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.liens = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs = dict(attrs)
            href = attrs.get("href", "")
            texte = attrs.get("title", "")
            if href:
                self.liens.append((href, texte))

print("Recherche des liens du site SIHF...")

try:
    req = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(req, timeout=20) as reponse:
        html = reponse.read().decode("utf-8", errors="replace")

    parser = LiensParser()
    parser.feed(html)

    mots = ("game", "match", "calendar", "kalender", "result", "spiel", "equipe")

    trouves = set()
    for href, titre in parser.liens:
        if any(mot in (href + " " + titre).lower() for mot in mots):
            trouves.add(href + " — " + titre)

    if trouves:
        print("Liens potentiellement utiles :")
        for lien in sorted(trouves):
            print(lien)
    else:
        print("Aucun lien de calendrier détecté dans la page d'accueil.")

except Exception as erreur:
    print("Erreur :", erreur)

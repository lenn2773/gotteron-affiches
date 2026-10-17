import urllib.request
from html.parser import HTMLParser
import re

URL = (
    "https://www.sihf.ch/fr/game-center/"
    "equipe/calendrier-des-matchs/1-1-103138"
)


class TexteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.textes = []

    def handle_data(self, data):
        texte = data.strip()
        if texte:
            self.textes.append(texte)


print("Lecture du calendrier officiel de Gottéron...")

try:
    req = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(req, timeout=30) as response:
        html = response.read().decode(
            "utf-8",
            errors="replace"
        )

    parser = TexteParser()
    parser.feed(html)

    texte = re.sub(
        r"\s+",
        " ",
        " ".join(parser.textes)
    )

    print("Page récupérée :", len(html), "caractères")

    position = texte.find("Fribourg-Gottéron")

    if position >= 0:
        print("Extrait du calendrier :")
        print(texte[position:position + 2500])
    else:
        print(
            "Les matchs ne sont pas visibles "
            "dans le HTML reçu."
        )
        print("Début de la page :", texte[:500])

except Exception as erreur:
    print("Erreur :", erreur)

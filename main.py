
import urllib.request
from html.parser import HTMLParser
from html import unescape
import re

URL = "https://www.sihf.ch/fr/game-center/equipe/calendrier-des-matchs/1-1-103138"

class MatchParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.matches = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "c-game-preview" in a.get("class", ""):
            home = a.get("data-home-club-id", "")
            away = a.get("data-away-club-id", "")
            game = a.get("data-game-id", "")
            if "103138" in (home, away) and game:
                self.matches.append(game)

try:
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode("utf-8", errors="replace")

    p = MatchParser()
    p.feed(html)
    ids = list(dict.fromkeys(p.matches))

    print("Matchs de Gottéron trouvés :", len(ids))

    if ids:
        match_url = "https://www.sihf.ch/umbraco/GameCenter/GameShort/Get?gameId=" + ids[0] + "&displayStyle=simple&leagueColor="
        req = urllib.request.Request(match_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            resultat = r.read().decode("utf-8", errors="replace")
        texte = re.sub(r"<[^>]+>", " ", resultat)
        texte = re.sub(r"\s+", " ", unescape(texte)).strip()
        print("Réponse du match :", texte[:700])
    else:
        print("Aucun identifiant de match trouvé.")

except Exception as e:
    print("Erreur :", e)

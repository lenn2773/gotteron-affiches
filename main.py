
import urllib.request
from html.parser import HTMLParser
from html import unescape
import re

PAGE_URL = (
    "https://www.sihf.ch/fr/game-center/equipe/"
    "calendrier-des-matchs/1-1-103138"
)


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        data = data.strip()
        if data:
            self.parts.append(data)


def fetch(url, referer=None):
    headers = {"User-Agent": "Mozilla/5.0", "HX-Request": "true"}
    if referer:
        headers["Referer"] = referer

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


try:
    page = fetch(PAGE_URL)

    ids = list(dict.fromkeys(
        re.findall(r'data-game-id="([^"]+)"', page)
    ))

    print("Matchs trouvés :", len(ids))

    if not ids:
        print("Aucun match trouvé.")
    else:
        game_id = ids[0]
        print("Match testé :", game_id)

        url = (
            "https://www.sihf.ch/umbraco/GameCenter/GameShort/Get"
            f"?gameId={game_id}&displayStyle=simple&leagueColor="
        )

        html = fetch(url, PAGE_URL)

        parser = TextParser()
        parser.feed(html)

        texte = re.sub(
            r"\s+",
            " ",
            unescape(" ".join(parser.parts))
        ).strip()

        print("Informations du match :")
        print(texte[:1200])

except Exception as error:
    print("Erreur :", error)

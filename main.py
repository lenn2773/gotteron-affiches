
import urllib.request
from html.parser import HTMLParser
from html import unescape
import re

URL = "https://www.sihf.ch/fr/game-center/equipe/calendrier-des-matchs/1-1-103138"


class MatchParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.matches = []
        self.current = None
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "div":
            classes = attrs.get("class", "")

            if self.current is None and "c-game-preview" in classes:
                home = attrs.get("data-home-club-id", "")
                away = attrs.get("data-away-club-id", "")
                game = attrs.get("data-game-id", "")

                if "103138" in (home, away) and game:
                    self.current = {
                        "id": game,
                        "text": [],
                    }
                    self.depth = 1
                    return

            elif self.current is not None:
                self.depth += 1

    def handle_endtag(self, tag):
        if tag == "div" and self.current is not None:
            self.depth -= 1

            if self.depth == 0:
                self.matches.append(self.current)
                self.current = None

    def handle_data(self, data):
        if self.current is not None:
            text = data.strip()
            if text:
                self.current["text"].append(text)


def main():
    print("Recherche des matchs de Fribourg-Gottéron...")

    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", errors="replace")

    parser = MatchParser()
    parser.feed(html)

    matches = parser.matches

    print("Matchs de Gottéron trouvés :", len(matches))

    if not matches:
        print("Aucun match détecté. Il faudra vérifier la page SIHF.")
        return

    for match in matches[:5]:
        text = re.sub(
            r"\s+",
            " ",
            unescape(" ".join(match["text"]))
        ).strip()

        print("\nMatch ID :", match["id"])
        print("Informations :", text[:500])

    print("\nVérification terminée.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Erreur :", error)

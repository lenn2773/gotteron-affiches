
import urllib.request
import re
from html import unescape

URL = "https://www.sihf.ch/fr/game-center/equipe/calendrier-des-matchs/1-1-103138"

try:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", errors="replace")

    # Recherche les balises qui contiennent directement les identifiants.
    pattern = re.compile(
        r'<[^>]+data-game-id="([^"]+)"[^>]*data-home-club-id="([^"]+)"[^>]*data-away-club-id="([^"]+)"[^>]*>',
        re.DOTALL
    )

    matches = {}

    for match in pattern.finditer(html):
        game_id, home, away = match.groups()

        if "103138" in (home, away):
            matches[game_id] = (home, away, match.group(0))

    print("Matchs uniques de Gottéron :", len(matches))

    for game_id, (home, away, tag) in list(matches.items())[:10]:
        print("\nID :", game_id)
        print("Domicile :", home)
        print("Extérieur :", away)
        print("Balise :", unescape(tag)[:300])

except Exception as error:
    print

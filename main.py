
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

    # Repère les cartes de match et leurs informations.
    positions = [
        m.start()
        for m in re.finditer(r'class="[^"]*c-game-preview', html)
    ]

    print("Cartes de match trouvées :", len(positions))

    for i, position in enumerate(positions[:3], start=1):
        extrait = html[position:position + 5000]

        game_id = re.search(r'data-game-id="([^"]+)"', extrait)
        home_id = re.search(r'data-home-club-id="([^"]+)"', extrait)
        away_id = re.search(r'data-away-club-id="([^"]+)"', extrait)

        texte = re.sub(r"<[^>]+>", " ", extrait)
        texte = re.sub(r"\s+", " ", unescape(texte)).strip()

        print(f"\nCarte {i}")
        print("ID match :", game_id.group(1) if game_id else "inconnu")
        print("ID domicile :", home_id.group(1) if home_id else "inconnu")
        print("ID extérieur :", away_id.group(1) if away_id else "inconnu")
        print("Texte :", texte[:500])

except Exception as error:
    print("Erreur :", error)

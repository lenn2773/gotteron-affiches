
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

    # Cherche les identifiants des matchs dans le HTML.
    ids = re.findall(r'data-game-id="([^"]+)"', html)

    print("Nombre d'identifiants trouvés :", len(ids))
    print("Premiers identifiants :", ids[:5])

    # Affiche un extrait autour du premier identifiant.
    if ids:
        position = html.find(ids[0])
        extrait = html[max(0, position - 500):position + 1000]
        extrait = re.sub(r"<[^>]+>", " ", extrait)
        extrait = re.sub(r"\s+", " ", unescape(extrait)).strip()
        print("\nExtrait du premier match :")
        print(extrait[:800])

except Exception as error:
    print("Erreur :", error)

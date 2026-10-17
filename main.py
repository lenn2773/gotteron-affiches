
import urllib.request
import re
from datetime import datetime

URL = "https://www.flashscore.de/team/hc-fribourg-gotteron/r94HIWFD/ergebnisse/"

request = urllib.request.Request(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

try:
    with urllib.request.urlopen(request, timeout=30) as response:
        page = response.read().decode("utf-8", errors="replace")

    debut = page.find('cjs.initialFeeds["results"]')

    if debut == -1:
        print("Flux des résultats introuvable.")
    else:
        extrait = page[debut:debut + 250000]

        matchs = re.findall(
            r'AA÷([^¬]+).*?AD÷([^¬]+).*?'
            r'AE÷([^¬]+).*?AF÷([^¬]+).*?'
            r'AG÷([^¬]+).*?AH÷([^¬]+)',
            extrait
        )

        print("Matchs trouvés :", len(matchs))
        print("\nPremiers résultats :")

        for identifiant, date, equipe1, equipe2, score1, score2 in matchs[:15]:
            print(
                f"ID={identifiant} | Date={date} | "
                f"{equipe1} - {equipe2} | {score1}-{score2}"
            )

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))

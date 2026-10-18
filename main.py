
import urllib.request
import re

URL = "https://www.flashscore.de/team/hc-fribourg-gotteron/r94HIWFD/ergebnisse/"

try:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        page = response.read().decode("utf-8", errors="replace")

    identifiant = "pIS547h5"
    position = page.find(identifiant)

    if position == -1:
        print("Match introuvable dans la page")
    else:
        debut = max(0, position - 3000)
        fin = min(len(page), position + 3000)
        extrait = page[debut:fin]

        liens = re.findall(
            r"""href=["']([^"']+)["']""",
            extrait
        )

        for lien in liens:
            if "match" in lien or "spiel" in lien:
                print(lien)

        print("\n--- FIN DU TEST ---")

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))

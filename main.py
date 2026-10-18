
import urllib.request
import re
from datetime import datetime, timezone

URL = "https://www.flashscore.de/team/hc-fribourg-gotteron/r94HIWFD/ergebnisse/"

try:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        page = response.read().decode("utf-8", errors="replace")

    marqueur = 'cjs.initialFeeds["results"]'
    debut = page.find(marqueur)
    debut = page.find("data: `", debut)
    debut += len("data: `")
    fin = page.find("`;", debut)
    donnees = page[debut:fin]

    print("Matchs de Gottéron :\n")

    for bloc in donnees.split("¬~"):
        champs = dict(
            re.findall(r"(?:^|¬)([A-Z]+)÷([^¬]*)", bloc)
        )

        domicile = champs.get("AE", "")
        exterieur = champs.get("AF", "")
        score_dom = champs.get("AG", "")
        score_ext = champs.get("AH", "")
        identifiant = champs.get("AA", "")
        date = champs.get("AD", "")

        if "Fribourg-Gottéron" in (domicile + exterieur):
            if score_dom and score_ext:
                print(
                    f"ID: {identifiant} | "
                    f"{domicile} {score_dom} - "
                    f"{score_ext} {exterieur} | "
                    f"Date: {date}"
                )

    print("\nTEST TERMINÉ")

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))

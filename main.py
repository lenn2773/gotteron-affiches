
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

    for identifiant in ["pIS547h5", "r9Y59gz2"]:
        position = page.find(identifiant)
        print(f"\n--- {identifiant} ---")

        if position == -1:
            print("Identifiant introuvable")
        else:
            print(page[max(0, position - 500):position + 1000])

    print("\nTEST TERMINÉ")

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))

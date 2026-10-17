
import urllib.request
import re

url = "https://www.sihf.ch/scripts/game-center.js"

try:
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        js = r.read().decode("utf-8", errors="replace")

    print("Fichier récupéré :", len(js), "caractères")
    lignes = [
        x.strip() for x in js.splitlines()
        if re.search(r"api|ajax|fetch|calendar|match|game", x, re.I)
    ]

    for ligne in lignes[:10]:
        print(ligne[:220])

    if not lignes:
        print("Aucune ligne utile trouvée.")

except Exception as e:
    print("Erreur :", e)

import urllib.request
import re

BASE = "https://static.flashscore.com/res/_fs/build/"

FICHIERS = [
    "EventIncidentTypeList.CFYVND3.js",
    "schemas.BARhQst.js",
    "setServerTimeFromResponse.Cpqbm3X.js",
]

for fichier in FICHIERS:
    print("\n" + "=" * 55)
    print("MODULE :", fichier)

    try:
        req = urllib.request.Request(
            BASE + fichier,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urllib.request.urlopen(req, timeout=20) as r:
            code = r.read().decode("utf-8", errors="replace")

        print("Taille :", len(code))
        print(code[:7000])

    except Exception as erreur:
        print("ERREUR :", erreur)

print("\nTEST TERMINÉ")

import urllib.request
import re

BASE = "https://static.flashscore.com/res/_fs/build/"
FICHIER = "FeedFetcherWithStatus.DYI27xv.js"

try:
    req = urllib.request.Request(
        BASE + FICHIER,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(req, timeout=20) as r:
        contenu = r.read().decode("utf-8", errors="replace")

    print("Taille du module :", len(contenu))

    mots = [
        "fetch(",
        "getUrl",
        "feed",
        "incidents",
        "event",
        "endpoint",
        "pathPrefix",
        "resolveFetchedData",
        "x-fsign"
    ]

    for mot in mots:
        positions = [
            m.start()
            for m in re.finditer(re.escape(mot), contenu, re.IGNORECASE)
        ]

        print(f"\n--- {mot} : {len(positions)} occurrence(s) ---")

        for pos in positions[:3]:
            debut = max(0, pos - 350)
            fin = min(len(contenu), pos + 650)
            print(contenu[debut:fin])
            print()

    print("TEST TERMINÉ")

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))

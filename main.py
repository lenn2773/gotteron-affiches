import urllib.request
import re

BASE = "https://static.flashscore.com/res/_fs/build/"

FICHIERS = [
    "hockey-detail.QRcARaG.js",
    "FeedFetcherAbstract.l5uJmGG.js",
    "DataProvider.DSxxxWP.js",
    "api.C3suFwK.js",
]

MOTS = [
    "incidents",
    "goal",
    "scorer",
    "participant",
    "graphql",
    "pq_graphql",
    "fetch(",
]

for fichier in FICHIERS:
    print("\n" + "=" * 60)
    print("MODULE :", fichier)

    try:
        req = urllib.request.Request(
            BASE + fichier,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=20) as r:
            contenu = r.read().decode("utf-8", errors="replace")

        deja_vus = set()
        nombre = 0

        for mot in MOTS:
            debut = 0
            while True:
                pos = contenu.lower().find(mot.lower(), debut)
                if pos == -1:
                    break

                debut = pos + len(mot)
                gauche = max(0, pos - 250)
                droite = min(len(contenu), pos + 450)

                extrait = contenu[gauche:droite]
                cle = extrait[:150]

                if cle not in deja_vus:
                    deja_vus.add(cle)
                    print(f"\n--- Mot trouvé : {mot} ---")
                    print(extrait)
                    nombre += 1

                if nombre >= 8:
                    break

            if nombre >= 8:
                break

        print("\nExtraits affichés :", nombre)

    except Exception as erreur:
        print("ERREUR :", erreur)

print("\nTEST TERMINÉ")

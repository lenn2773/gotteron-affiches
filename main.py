
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

    print("Page récupérée :", len(page), "caractères")

    marqueur = 'cjs.initialFeeds["results"]'
    debut = page.find(marqueur)

    if debut == -1:
        print("Flux des résultats introuvable.")
    else:
        debut = page.find("data: `", debut)

        if debut == -1:
            print("Données des résultats introuvables.")
        else:
            debut += len("data: `")
            fin = page.find("`;", debut)

            if fin == -1:
                print("Fin des données introuvable.")
            else:
                donnees = page[debut:fin]
                print("Données extraites :", len(donnees), "caractères")

                blocs = donnees.split("¬~")
                print("Blocs trouvés :", len(blocs))
                print("\nExemples de blocs :")

                for bloc in blocs[:5]:
                    print(bloc[:500])
                    print("---")

    print("TEST TERMINÉ")

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))

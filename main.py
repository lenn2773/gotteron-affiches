
import urllib.request
import re

URL = "https://www.sihf.ch/fr/game-center/equipe/calendrier-des-matchs/1-1-103138"

print("Recherche des résultats de Fribourg-Gottéron...")

try:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        page = response.read().decode("utf-8", errors="replace")

    texte = re.sub(r"<[^>]+>", " ", page)
    texte = re.sub(r"\s+", " ", texte)

    if "Fribourg-Gottéron" in texte:
        print("Le site de la SIHF est accessible.")
        print("Des informations sur Gottéron ont été trouvées.")
        print("Extrait :", texte[:1500])
    else:
        print("Le site répond, mais les résultats n'ont pas été détectés.")

except Exception as erreur:
    print("Impossible de récupérer les données :", erreur)


import urllib.request
import re

URL = "https://www.flashscore.de/team/hc-fribourg-gotteron/r94HIWFD/begegnungen/"

try:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        page = response.read().decode("utf-8", errors="replace")

    print("Statut HTTP :", response.status)
    print("Taille :", len(page))

    feeds = re.findall(
        r'cjs\.initialFeeds\["([^"]+)"\]\s*=\s*\{\s*data:\s*`(.*?)`',
        page,
        re.DOTALL
    )

    for name, data in feeds:
        print("\nFlux trouvé :", name)
        print("Nombre de matchs :", len(re.findall(r"(?:^|¬~)AA÷", data)))
        print("Extrait :", data[:1000])

    if not feeds:
        print("Aucun flux de calendrier détecté.")

except Exception as error:
    print("Erreur :", type(error).__name__, str(error))

print("\nTEST TERMINÉ")

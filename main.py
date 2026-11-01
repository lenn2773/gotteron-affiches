
import urllib.request
import re

URL = "https://www.flashscore.de/team/hc-fribourg-gotteron/r94HIWFD/ergebnisse/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    request = urllib.request.Request(URL, headers=headers)

    with urllib.request.urlopen(request, timeout=20) as response:
        page = response.read().decode("utf-8", errors="replace")

    print("Statut HTTP :", response.status)
    print("Taille de la page :", len(page))

    match = re.search(
        r'cjs\.initialFeeds\["results"\]\s*=\s*"([^"]*)"',
        page
    )

    if not match:
        print("Flux des résultats introuvable.")
    else:
        feed = match.group(1)
        feed = feed.replace("\\u00ac", "¬")

        print("Flux trouvé !")
        print("Identifiants de matchs détectés :",
              len(re.findall(r"AA÷", feed)))

        print("\nExtrait du flux :")
        print(feed[:2500])

except Exception as error:
    print("Erreur :", type(error).__name__, str(error))

print("\nTEST TERMINÉ")

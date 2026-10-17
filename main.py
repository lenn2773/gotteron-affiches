
import urllib.request
from html.parser import HTMLParser

URL = "https://www.flashscore.de/team/hc-fribourg-gotteron/r94HIWFD/ergebnisse/"

request = urllib.request.Request(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "de-DE,de;q=0.9,fr;q=0.8",
    },
)

try:
    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", errors="replace")

    print("TEST FLASHSCORE")
    print("Page récupérée :", len(html), "caractères")

    for mot in ["Schmid", "Sörensen", "goal", "scorer", "event"]:
        print(f"{mot} :", mot.lower() in html.lower())

    with open("flashscore_test.html", "w", encoding="utf-8") as fichier:
        fichier.write(html)

    print("Page enregistrée dans flashscore_test.html")
    print("TEST TERMINÉ")

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))

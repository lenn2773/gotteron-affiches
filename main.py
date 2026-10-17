
import urllib.request
import re
import html

URL = "https://www.flashscore.de/team/hc-fribourg-gotteron/r94HIWFD/ergebnisse/"

request = urllib.request.Request(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

try:
    with urllib.request.urlopen(request, timeout=30) as response:
        page = response.read().decode("utf-8", errors="replace")

    # Repérer les identifiants de matchs Flashscore
    ids = list(dict.fromkeys(re.findall(
        r'data-event-id=["\']([^"\']+)["\']',
        page
    )))

    print("Nombre de matchs repérés :", len(ids))
    print("\nPremiers identifiants :")

    for identifiant in ids[:15]:
        print(identifiant)

    # Repérer les liens vers les détails des matchs
    liens = list(dict.fromkeys(re.findall(
        r'href=["\']([^"\']*(?:match|spiel|game)[^"\']*)["\']',
        page,
        re.IGNORECASE
    )))

    print("\nLiens possibles vers les matchs :")

    for lien in liens[:15]:
        print(html.unescape(lien))

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))

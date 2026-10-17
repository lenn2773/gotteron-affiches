
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

    print("Page récupérée :", len(page), "caractères")

    # Chercher les classes HTML liées aux matchs
    classes = re.findall(
        r'class=["\']([^"\']*(?:event|match|participant|score)[^"\']*)["\']',
        page,
        re.IGNORECASE
    )

    print("\nClasses liées aux matchs :")
    for classe in list(dict.fromkeys(classes))[:35]:
        print(classe)

    # Chercher les occurrences du nom de Gottéron
    for terme in ["Fribourg-Gottéron", "Fribourg", "result"]:
        print(f"\nOccurrences de {terme} :",
              len(re.findall(re.escape(terme), page, re.IGNORECASE)))

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))


import urllib.request
import re

URL = "https://www.flashscore.de/match/pIS547h5/"

try:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        page = response.read().decode("utf-8", errors="replace")

    print("Page récupérée :", len(page), "caractères")

    for terme in ["Sörensen", "Schmid", "goal", "scorer", "incident"]:
        print(
            f"{terme} :",
            len(re.findall(re.escape(terme), page, re.IGNORECASE))
        )

    for marqueur in ["initialFeeds", "detail", "event"]:
        print(
            f"{marqueur} présent :",
            marqueur.lower() in page.lower()
        )

    print("TEST TERMINÉ")

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))


import urllib.request
import re

URL = "https://static.flashscore.com/res/_fs/build/detail.B0EdFI7.js"

try:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        script = response.read().decode("utf-8", errors="replace")

    fichiers = sorted(set(re.findall(
        r'["\']([^"\']+\.js)["\']',
        script
    )))

    mots = [
        "feed", "fetch", "api", "data",
        "event", "incident", "match", "detail"
    ]

    print("Modules potentiellement intéressants :")

    for fichier in fichiers:
        if any(mot in fichier.lower() for mot in mots):
            print(fichier)

    print("\nNombre total de modules :", len(fichiers))
    print("TEST TERMINÉ")

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))

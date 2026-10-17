
import urllib.request
import re
import html

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
        page = response.read().decode("utf-8", errors="replace")

    print("Page récupérée :", len(page), "caractères")

    for terme in ["Schmid", "goalServe", "incident", "participant", "event"]:
        positions = [m.start() for m in re.finditer(
            re.escape(terme), page, re.IGNORECASE
        )]

        print(f"\n--- {terme} : {len(positions)} occurrences ---")

        for position in positions[:2]:
            extrait = page[max(0, position - 250):position + 500]
            extrait = html.unescape(extrait)
            print(extrait.replace("\n", " ")[:750])

    print("\nTEST TERMINÉ")

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))

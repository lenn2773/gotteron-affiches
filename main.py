
import urllib.request
import re

URL = "https://www.flashscore.de/team/hc-fribourg-gotteron/r94HIWFD/ergebnisse/"

request = urllib.request.Request(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

try:
    with urllib.request.urlopen(request, timeout=30) as response:
        page = response.read().decode("utf-8", errors="replace")

    for terme in [
        "matches-block-results",
        "team-page-results",
        "data-testid",
        "eventRow",
    ]:
        print(f"\n========== {terme} ==========")

        positions = [
            match.start()
            for match in re.finditer(re.escape(terme), page, re.IGNORECASE)
        ]

        print("Occurrences :", len(positions))

        for position in positions[:2]:
            print(page[max(0, position - 300):position + 900])
            print("\n---")

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))

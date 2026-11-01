
import urllib.request
import re

URL = "https://www.flashscore.com/match/hockey/fribourg-r94HIWFD/zurich-vmRgFvP6/?mid=pIS547h5"

try:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        page = response.read().decode("utf-8", errors="replace")

    for mot in ["pq_graphql", "initialFeeds", "detail", "event", "incident"]:
        positions = [
            m.start() for m in re.finditer(
                re.escape(mot), page, re.IGNORECASE
            )
        ]

        print(f"\n--- {mot} : {len(positions)} occurrence(s) ---")

        for pos in positions[:3]:
            print(page[max(0, pos - 250):pos + 500])
            print()

    print("TEST TERMINÉ")

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))


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

    print("Taille du script :", len(script))

    for mot in ["pq_graphql", "incidents", "event", "goal", "detail"]:
        positions = [
            m.start() for m in re.finditer(
                re.escape(mot), script, re.IGNORECASE
            )
        ]

        print(f"\n--- {mot} : {len(positions)} occurrence(s) ---")

        for pos in positions[:2]:
            print(script[max(0, pos - 200):pos + 400])
            print()

    print("TEST TERMINÉ")

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))

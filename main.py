
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

    print("Page téléchargée :", len(page), "caractères")

    mots = [
        "pIS547h5",
        "incident",
        "event",
        "goal",
        "scorer",
        "Sörensen",
        "Schmid"
    ]

    for mot in mots:
        positions = [
            m.start() for m in re.finditer(
                re.escape(mot), page, re.IGNORECASE
            )
        ]

        print(f"\n{mot} : {len(positions)} occurrence(s)")

        for pos in positions[:2]:
            print(page[max(0, pos - 150):pos + 300])

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))


import urllib.request
import re
from html import unescape

URL = "https://www.gotteron.ch/fr/game/2026-10-10/20271105000077"

try:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", errors="replace")

    print("Page du match accessible :", len(html), "caractères")

    mots = [
        "buteur", "scorer", "goal", "goals",
        "scorers", "assists", "tor", "torschütze"
    ]

    for mot in mots:
        positions = [
            m.start() for m in re.finditer(
                re.escape(mot), html, re.IGNORECASE
            )
        ]

        print(f"\n{mot} : {len(positions)} occurrence(s)")

        for position in positions[:2]:
            extrait = html[max(0, position - 120):position + 250]
            extrait = re.sub(r"\s+", " ", unescape(extrait))
            print(extrait)

except Exception as error:
    print("Erreur :", error)

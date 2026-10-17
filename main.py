
import urllib.request
import re

url = "https://www.sihf.ch/scripts/game-center.js"

req = urllib.request.Request(
    url, headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=30) as r:
    js = r.read().decode("utf-8", errors="replace")

print("Fichier chargé :", len(js), "caractères")

for mot in ["api/", "/api", "gamecenter", "game-center", "calendar", "fixtures"]:
    positions = [m.start() for m in re.finditer(re.escape(mot), js, re.I)]
    print(f"\n{mot} : {len(positions)} occurrence(s)")
    for pos in positions[:2]:
        print(js[max(0, pos-100):pos+220])

print("\nFin du diagnostic.")

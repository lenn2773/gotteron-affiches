
import urllib.request
import re

url = "https://www.sihf.ch/scripts/game-center.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

with urllib.request.urlopen(req, timeout=30) as r:
    js = r.read().decode("utf-8", errors="replace")

for mot in ["GamesCalendarComponent", "fetch(", "XMLHttpRequest", "teamId", "leagueId"]:
    print("\n---", mot, "---")
    for m in list(re.finditer(re.escape(mot), js, re.I))[:2]:
        print(js[max(0, m.start()-250):m.start()+500])

print("\nFin.")

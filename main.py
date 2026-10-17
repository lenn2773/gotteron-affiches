
import urllib.request
import re

url = "https://www.sihf.ch/scripts/game-center.js"

req = urllib.request.Request(
    url, headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=30) as r:
    js = r.read().decode("utf-8", errors="replace")

for mot in ["firebaseConfig", "getDatabase", "getDocs", "collection(", "GamesCalendarComponent"]:
    m = re.search(re.escape(mot), js)
    print(f"{mot} :", js[max(0, m.start()-100):m.start()+250] if m else "absent")


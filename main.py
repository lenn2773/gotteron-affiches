
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

    scripts = re.findall(
        r'<script[^>]+src=["\']([^"\']+)["\']',
        page
    )

    print("Nombre de scripts :", len(scripts))

    for script in scripts:
        if "detail" in script.lower() or "match" in script.lower():
            print(script)

    print("\nTEST TERMINÉ")

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))

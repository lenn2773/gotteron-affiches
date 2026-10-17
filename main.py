
import urllib.request
import re

url = "https://www.sihf.ch/fr/game-center/equipe/calendrier-des-matchs/1-1-103138"

req = urllib.request.Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0",
        "HX-Request": "true",
        "HX-Current-URL": url,
    },
)

try:
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode("utf-8", errors="replace")

    print("Réponse :", len(html), "caractères")

    for mot in ["Fribourg-Gottéron", "c-game-preview", "data-home-team", "score"]:
        print(mot, ":", len(re.findall(mot, html, re.I)))

    pos = html.find("c-game-preview")
    if pos >= 0:
        print("\nExtrait :")
        print(re.sub(r"\s+", " ", html[pos:pos+700]))
    else:
        print("Aucun bloc de match détecté.")

except Exception as e:
    print("Erreur :", e)

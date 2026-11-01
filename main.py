import urllib.request
import re
import os

TEAM_URL = "https://www.flashscore.de/team/hc-fribourg-gotteron/r94HIWFD/ergebnisse/"

request = urllib.request.Request(
    TEAM_URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(request, timeout=20) as response:
    page = response.read().decode("utf-8", errors="replace")

feed_match = re.search(
    r'cjs\.initialFeeds\["results"\]\s*=\s*\{\s*data:\s*`(.*?)`',
    page,
    re.DOTALL
)

if not feed_match:
    raise SystemExit("Flux des résultats introuvable.")

feed = feed_match.group(1)

def get_value(text, key):
    match = re.search(rf"(?:^|¬){key}÷([^¬~]*)", text)
    return match.group(1).strip() if match else ""

match = re.search(
    r"(?:^|¬~)AA÷2omdEcvK(.*?)(?=¬~AA÷|$)",
    feed,
    re.DOTALL
)

if not match:
    raise SystemExit("Match de test introuvable.")

record = match.group(1)

logos = {
    "fribourg": get_value(record, "OA"),
    "geneve": get_value(record, "OB")
}

os.makedirs("logos", exist_ok=True)

for team, filename in logos.items():
    if not filename:
        print("Logo manquant :", team)
        continue

    url = "https://static.flashscore.com/res/image/data/" + filename

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            content = response.read()

            if not response.headers.get("Content-Type", "").startswith("image/"):
                print("Ce fichier n'est pas une image :", team)
                continue

        path = os.path.join("logos", team + ".png")

        with open(path, "wb") as file:
            file.write(content)

        print("Logo téléchargé :", team)
        print("Fichier :", path)
        print("Taille :", len(content), "octets")

    except Exception as error:
        print("Erreur pour", team, ":", error)

print("\nTEST TERMINÉ")

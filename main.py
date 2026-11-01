import urllib.request
import re

URL = "https://www.flashscore.de/team/hc-fribourg-gotteron/r94HIWFD/ergebnisse/"

request = urllib.request.Request(
    URL,
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
    print("ERREUR : résultats introuvables.")
    raise SystemExit

feed = feed_match.group(1)

def get_value(text, key):
    match = re.search(rf"(?:^|¬){key}÷([^¬~]*)", text)
    return match.group(1).strip() if match else ""

matches = re.finditer(
    r"(?:^|¬~)AA÷([^¬~]+)(.*?)(?=¬~AA÷|$)",
    feed,
    re.DOTALL
)

for match in matches:
    record = match.group(2)

    if "r94HIWFD" not in record:
        continue

    home = get_value(record, "AE")
    away = get_value(record, "AF")

    home_logo = get_value(record, "OA")
    away_logo = get_value(record, "OB")

    print("\nMATCH :", home, "-", away)
    print("Logo domicile :", home_logo)
    print("Logo extérieur :", away_logo)

    if home_logo and away_logo:
        print("Résultat : les deux logos sont disponibles !")
    else:
        print("Résultat : il manque au moins un logo.")

    break

print("\nTEST TERMINÉ")

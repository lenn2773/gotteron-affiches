import urllib.request
import re
from datetime import datetime
from zoneinfo import ZoneInfo

URL = "https://www.flashscore.de/team/hc-fribourg-gotteron/r94HIWFD/begegnungen/"

request = urllib.request.Request(
    URL,
    headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(request, timeout=20) as response:
    page = response.read().decode("utf-8", errors="replace")

match = re.search(
    r'cjs\.initialFeeds\["fixtures"\]\s*=\s*\{\s*data:\s*`(.*?)`',
    page,
    re.DOTALL
)

if not match:
    print("ERREUR : flux des matchs à venir introuvable.")
    raise SystemExit

feed = match.group(1)

def get_value(record, key):
    result = re.search(rf"(?:^|¬){key}÷([^¬~]*)", record)
    return result.group(1) if result else ""

print("CALENDRIER DE FRIBOURG-GOTTÉRON")
print("=" * 45)

count = 0
league = ""

for record in feed.split("¬~"):
    if get_value(record, "ZA"):
        league = get_value(record, "ZA")

    match_id = get_value(record, "AA")
    if not match_id:
        continue

    home_id = get_value(record, "PX")
    away_id = get_value(record, "PY")

    if home_id != "r94HIWFD" and away_id != "r94HIWFD":
        continue

    timestamp = get_value(record, "AD")
    home = get_value(record, "AE")
    away = get_value(record, "AF")

    if not timestamp:
        continue

    date = datetime.fromtimestamp(
        int(timestamp),
        ZoneInfo("Europe/Zurich")
    )

    print(f"{date:%d.%m.%Y à %H:%M}")
    print(f"{home} - {away}")
    print(f"Compétition : {league}")
    print(f"Identifiant : {match_id}")
    print("-" * 45)

    count += 1

print(f"\nTotal : {count} matchs trouvés.")
print("TEST TERMINÉ")

import urllib.request
import re
from datetime import datetime
from zoneinfo import ZoneInfo

TEAM_ID = "r94HIWFD"

# 1. Récupérer les résultats de Gottéron
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
    result = re.search(rf"(?:^|¬){key}÷([^¬~]*)", text)
    return result.group(1).strip() if result else ""


# 2. Identifier les matchs terminés de Gottéron
matches = re.finditer(
    r"(?:^|¬~)AA÷([^¬~]+)(.*?)(?=¬~AA÷|$)",
    feed,
    re.DOTALL
)

finished = []

for match in matches:
    match_id = match.group(1)
    record = match.group(2)

    home_id = get_value(record, "PX")
    away_id = get_value(record, "PY")

    if TEAM_ID not in (home_id, away_id):
        continue

    timestamp = get_value(record, "AD")
    home_score = get_value(record, "AG")
    away_score = get_value(record, "AH")

    if not timestamp or not home_score or not away_score:
        continue

    finished.append({
        "id": match_id,
        "timestamp": int(timestamp),
        "home": get_value(record, "AE"),
        "away": get_value(record, "AF"),
        "home_score": home_score,
        "away_score": away_score
    })

if not finished:
    print("Aucun match terminé trouvé.")
    raise SystemExit

# 3. Prendre le plus récent
latest = max(finished, key=lambda match: match["timestamp"])

date = datetime.fromtimestamp(
    latest["timestamp"],
    ZoneInfo("Europe/Zurich")
)

print("DERNIER MATCH TERMINÉ DE GOTTÉRON")
print("=" * 45)
print("Date :", date.strftime("%d.%m.%Y à %H:%M"))
print("Match :", latest["home"], "-", latest["away"])
print("Score :", latest["home_score"], "-", latest["away_score"])
print("Identifiant :", latest["id"])


# 4. Récupérer les événements de ce match
event_url = (
    "https://local-global.flashscore.ninja/2/x/feed/df_sui_2_"
    + latest["id"]
)

headers = {
    "User-Agent": "Mozilla/5.0",
    "x-fsign": "SW9D1eZo",
    "Referer": "https://www.flashscore.com/",
    "Origin": "https://www.flashscore.com/",
    "Accept": "*/*"
}

request = urllib.request.Request(event_url, headers=headers)

with urllib.request.urlopen(request, timeout=20) as response:
    data = response.read().decode("utf-8", errors="replace")

print("\nBUTEURS ET ASSISTS")
print("=" * 45)

period = ""

for part in data.split("~"):

    if part.startswith("AC÷"):
        period = get_value(part, "AC")
        continue

    if get_value(part, "IK") != "Goal":
        continue

    team = get_value(part, "IA")
    minute = get_value(part, "IB")
    scorer = get_value(part, "IF")

    players = re.findall(
        r"IF÷([^¬~]*)¬IU÷[^¬~]*¬ICT÷¬IK÷([^¬~]*)",
        part
    )

    assists = [
        name for name, role in players
        if role.startswith("Assistance")
    ]

    team_name = (
        latest["home"] if team == "1"
        else latest["away"]
    )

    print(f"\n{minute} - {period}")
    print("Équipe :", team_name)
    print("Buteur :", scorer)
    print("Assists :", ", ".join(assists) if assists else "Aucune")

print("\nTEST TERMINÉ")

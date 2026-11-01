import urllib.request
import re

MATCH_ID = "pIS547h5"

URL = f"https://local-global.flashscore.ninja/2/x/feed/df_sui_2_{MATCH_ID}"

headers = {
    "User-Agent": "Mozilla/5.0",
    "x-fsign": "SW9D1eZo",
    "Referer": "https://www.flashscore.com/",
    "Origin": "https://www.flashscore.com",
    "Accept": "*/*"
}

request = urllib.request.Request(URL, headers=headers)

with urllib.request.urlopen(request, timeout=20) as response:
    data = response.read().decode("utf-8", errors="replace")

def get_value(text, key):
    match = re.search(rf"(?:^|¬){key}÷([^¬~]*)", text)
    return match.group(1).strip() if match else ""

print("ÉVÉNEMENTS : ZURICH 5–4 FRIBOURG")
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

    team_name = "Zürich" if team == "1" else "Fribourg"

    print(f"\nPériode : {period}")
    print(f"Minute : {minute}")
    print(f"Équipe : {team_name}")
    print(f"Buteur : {scorer}")
    print("Assists :", ", ".join(assists) if assists else "Aucune")

print("\nTEST TERMINÉ")

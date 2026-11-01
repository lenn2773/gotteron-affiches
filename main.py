
import urllib.request
import re

MATCH_ID = "pIS547h5"

url = (
    "https://local-global.flashscore.ninja/"
    f"2/x/feed/df_sui_2_{MATCH_ID}"
)

headers = {
    "User-Agent": "Mozilla/5.0",
    "x-fsign": "SW9D1eZo",
    "Referer": "https://www.flashscore.com/",
    "Origin": "https://www.flashscore.com",
    "Accept": "*/*",
}

def get_value(text, key):
    match = re.search(
        rf"(?:^|¬){key}÷([^¬~]*)",
        text
    )
    return match.group(1) if match else ""

try:
    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request, timeout=20) as response:
        data = response.read().decode("utf-8")

    period = "Période inconnue"

    for part in data.split("~"):
        if part.startswith("AC÷"):
            period = part.replace("AC÷", "").strip()

        elif "IK÷Goal" in part:
            team = get_value(part, "IA")
            minute = get_value(part, "IB")
            scorer = get_value(part, "IF")

            # Les noms des assistants suivent le buteur.
            players = re.findall(
                r"IF÷([^¬~]*)¬IU÷[^¬~]*¬ICT÷¬IK÷([^¬~]*)",
                part
            )

            assists = [
                name for name, role in players
                if role.startswith("Assistance")
            ]

            print("--------------------------------")
            print("Période :", period)
            print("Équipe :", "Domicile" if team == "1" else "Extérieur")
            print("Minute :", minute)
            print("Buteur :", scorer)
            print("Passeurs :", ", ".join(assists) if assists else "Aucun")

    print("\nTEST TERMINÉ")

except Exception as error:
    print("Erreur :", type(error).__name__, str(error))

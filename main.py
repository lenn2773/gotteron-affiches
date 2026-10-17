
import urllib.request
import re

URL = "https://www.sihf.ch/fr/game-center/equipe/calendrier-des-matchs/1-1-103138"

try:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", errors="replace")

    match = re.search(r'data-game-id="([^"]+)"', html)

    if not match:
        print("Aucun match trouvé.")
    else:
        game_id = match.group(1)
        print("Match testé :", game_id)

        match_url = (
            "https://www.sihf.ch/umbraco/GameCenter/GameShort/Get"
            f"?gameId={game_id}&displayStyle=simple&leagueColor="
        )

        request = urllib.request.Request(
            match_url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Referer": URL,
                "HX-Request": "true",
            }
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            resultat = response.read().decode("utf-8", errors="replace")
            print("Code HTTP :", response.status)
            print("Réponse du serveur :")
            print(re.sub(r"\s+", " ", resultat)[:1500])

except Exception as error:
    print("Erreur :", error)

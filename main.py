
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
        print("Code HTTP :", response.status)

    print("Taille de la page :", len(html))
    print("Identifiant 103138 présent :", "103138" in html)
    print("Occurrences de c-game-preview :", html.count("c-game-preview"))
    print("Occurrences de data-game-id :", html.count("data-game-id"))

    match = re.search(r".{0,200}103138.{0,500}", html)

    if match:
        print("\nExtrait de la page :")
        print(match.group(0))
    else:
        print("\nAucun extrait contenant 103138.")
        print("Début de la page :")
        print(html[:500])

except Exception as error:
    print("Erreur :", error)

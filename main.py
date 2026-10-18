
import urllib.request

URL = "https://www.flashscore.de/match/pIS547h5/"

try:
    request = urllib.request.Request(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://www.flashscore.de/"
        }
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        page = response.read().decode("utf-8", errors="replace")
        print("Code HTTP :", response.status)
        print("Taille de la page :", len(page))
        print("Contient le nom de Fribourg :", "Fribourg" in page)
        print("Contient le mot goal :", "goal" in page.lower())
        print("Contient le mot scorer :", "scorer" in page.lower())

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))

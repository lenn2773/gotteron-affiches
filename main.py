
import urllib.request

URL = "https://www.flashscore.de/team/hc-fribourg-gotteron/r94HIWFD/ergebnisse/"

try:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        page = response.read().decode("utf-8", errors="replace")

    print("Statut HTTP :", response.status)
    print("Taille :", len(page))

    for term in ["initialFeeds", "results", "AA÷", "pIS547h5"]:
        position = page.find(term)
        print("\nRecherche :", term)
        print("Position :", position)

        if position != -1:
            print("Extrait :", page[max(0, position-200):position+800])

except Exception as error:
    print("Erreur :", type(error).__name__, str(error))

print("\nTEST TERMINÉ")

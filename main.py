
import urllib.request

URL = "https://www.flashscore.com/match/hockey/fribourg-r94HIWFD/zurich-vmRgFvP6/?mid=pIS547h5"

try:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        page = response.read().decode("utf-8", errors="replace")
        print("Code HTTP :", response.status)
        print("Taille de la page :", len(page))
        print("Fribourg présent :", "Fribourg" in page)
        print("ZSC présent :", "ZSC Lions" in page)
        print("Identifiant présent :", "pIS547h5" in page)

        for mot in ["Sörensen", "Schmid", "goal", "scorer"]:
            print(mot, ":", mot.lower() in page.lower())

except Exception as erreur:
    print("ERREUR :", type(erreur).__name__, str(erreur))

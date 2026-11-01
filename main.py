import urllib.request

url = "https://local-global.flashscore.ninja/2/x/feed/df_sui_2_pIS547h5"

headers = {
    "User-Agent": "Mozilla/5.0",
    "x-fsign": "SW9D1eZo",
    "Referer": "https://www.flashscore.com/",
    "Origin": "https://www.flashscore.com",
    "Accept": "*/*",
}

try:
    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req, timeout=20) as response:
        data = response.read().decode("utf-8", errors="replace")

        print("Statut HTTP :", response.status)
        print("Longueur :", len(data))
        print("Réponse :")
        print(data[:4000])

except Exception as e:
    print("Erreur :", type(e).__name__, str(e))

print("\nTEST TERMINÉ")

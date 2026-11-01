import urllib.request

URL = "https://www.flashscore.com/x/feed/df_team_1_"

headers = {
    "User-Agent": "Mozilla/5.0",
    "x-fsign": "000000"
}

try:
    req = urllib.request.Request(URL, headers=headers)

    with urllib.request.urlopen(req, timeout=20) as r:
        print("Statut HTTP :", r.status)
        print("Réponse :")
        print(r.read(2000).decode("utf-8", errors="replace"))

except Exception as e:
    print("Erreur :", type(e).__name__, str(e))

print("\nTEST TERMINÉ")

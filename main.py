
import json
import urllib.request

URL = "https://www.sihf.ch"

print("Recherche des données de Gottéron...")

try:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        print("Code de réponse du site :", response.status)
        page = response.read(5000).decode("utf-8", errors="replace")

    print("Connexion au site réussie.")
    print("Début de la réponse :")
    print(page[:1000])

except Exception as erreur:
    print("Erreur de connexion :", erreur)

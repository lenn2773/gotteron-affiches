
import urllib.request
import re

URL = "https://www.sihf.ch/fr/game-center/equipe/calendrier-des-matchs/1-1-103138"

req = urllib.request.Request(
    URL, headers={"User-Agent": "Mozilla/5.0"}
)

with urllib.request.urlopen(req, timeout=30) as r:
    html = r.read().decode("utf-8", errors="replace")

motifs = [
    r"<script[^>]+src=[\"']([^\"']+)",
    r"https?[^\"']*(?:api|game|match|calendar)[^\"']*",
]

for motif in motifs:
    resultats = re.findall(motif, html, re.I)
    print("\n---", motif, "---")
    for resultat in resultats[:8]:
        print(resultat)

print("\nDiagnostic terminé.")


import urllib.request
from html.parser import HTMLParser
from html import unescape

URL = "https://www.gotteron.ch/fr/Principale/Calendrier-et-resultats"


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs = dict(attrs)
            self.current = {
                "url": attrs.get("href", ""),
                "text": []
            }

    def handle_data(self, data):
        if self.current is not None:
            self.current["text"].append(data.strip())

    def handle_endtag(self, tag):
        if tag == "a" and self.current is not None:
            text = " ".join(
                part for part in self.current["text"] if part
            )
            self.links.append({
                "url": self.current["url"],
                "text": text
            })
            self.current = None


try:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8", errors="replace")
        print("Code HTTP :", response.status)

    parser = LinkParser()
    parser.feed(html)

    reports = [
        link for link in parser.links
        if "compte-rendu" in unescape(link["text"]).lower()
    ]

    print("Liens de comptes rendus trouvés :", len(reports))

    for report in reports[:10]:
        print("\nTitre :", report["text"])
        print("Lien :", report["url"])

except Exception as error:
    print("Erreur :", error)


import urllib.request
from html.parser import HTMLParser

URL = "https://www.flashscore.de/team/hc-fribourg-gotteron/r94HIWFD/ergebnisse/"

class LinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != "a":
            return

        attrs = dict(attrs)
        href = attrs.get("href", "")
        title = attrs.get("title", "")

        if "r94HIWFD" in href or "spiele" in href.lower():
            print("Lien :", href)
            if title:
                print("Titre :", title)

try:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        page = response.read().decode("utf-8", errors="replace")

    parser = LinkParser()
    parser.feed(page)

except Exception as error:
    print("Erreur :", type(error).__name__, str(error))

print("\nTEST TERMINÉ")


import urllib.request
import re

URL = "https://www.flashscore.de/team/hc-fribourg-gotteron/r94HIWFD/ergebnisse/"

try:
    request = urllib.request.Request(
        URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        page = response.read().decode("utf-8", errors="replace")

    match = re.search(
        r'cjs\.initialFeeds\["summary-results"\]\s*=\s*\{\s*data:\s*`(.*?)`',
        page,
        re.DOTALL
    )

    if not match:
        print("Flux introuvable.")
    else:
        feed = match.group(1)

        matches = re.finditer(
            r'(?:^|¬~)AA÷([^¬~]+)(.*?)(?=¬~AA÷|$)',
            feed,
            re.DOTALL
        )

        count = 0

        for item in matches:
            data = item.group(2)

            def field(name):
                result = re.search(
                    rf'(?:^|¬){name}÷([^¬~]*)',
                    data
                )
                return result.group(1) if result else "?"

            count += 1
            print("--------------------------------")
            print("ID :", item.group(1))
            print("Date :", field("AD"))
            print("Domicile :", field("AE"))
            print("Extérieur :", field("AF"))
            print("Score domicile :", field("AG"))
            print("Score extérieur :", field("AH"))

        print("\nNombre de matchs :", count)

except Exception as error:
    print("Erreur :", type(error).__name__, str(error))

print("\nTEST TERMINÉ")

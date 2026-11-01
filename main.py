import urllib.request
import re

BASE = "https://static.flashscore.com/res/_fs/build/"

FICHIERS = [
    "hockey-detail.QRcARaG.js",
    "api.C3suFwK.js",
    "FeedFetcherAbstract.l5uJmGG.js",
]

for fichier in FICHIERS:
    print("\n" + "=" * 55)
    print("MODULE :", fichier)

    req = urllib.request.Request(
        BASE + fichier,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            code = r.read().decode("utf-8", errors="replace")

        modules = sorted(set(re.findall(
            r'["\']([^"\']+\.js)["\']', code
        )))

        print("Modules importés :")
        for module in modules:
            print(" ", module)

        print("\nMots-clés de configuration :")
        for mot in [
            "feed_resolver",
            "url_prefix",
            "feed_sign",
            "project",
            "Api.config",
            "incident"
        ]:
            positions = [
                m.start()
                for m in re.finditer(re.escape(mot), code, re.I)
            ]
            if positions:
                print(f"\n{mot} : {len(positions)} occurrence(s)")
                for pos in positions[:2]:
                    print(code[max(0, pos-250):pos+500])

    except Exception as e:
        print("ERREUR :", e)

print("\nTEST TERMINÉ")

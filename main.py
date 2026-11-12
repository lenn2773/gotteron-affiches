
import os
import re
import urllib.request
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# CONFIGURATION
# ==========================================

TEAM_URL = (
    "https://www.flashscore.de/team/"
    "hc-fribourg-gotteron/r94HIWFD/ergebnisse/"
)

WIDTH = 1080
HEIGHT = 1350

OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "affiche.png")


# ==========================================
# POLICES
# ==========================================

def load_font(size, bold=False):
    if bold:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    else:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


# ==========================================
# RECUPERATION DES RESULTATS
# ==========================================

def get_value(record, key):
    match = re.search(
        rf"(?:^|¬){key}÷([^¬~]*)",
        record
    )
    return match.group(1).strip() if match else ""


def get_latest_match():

    request = urllib.request.Request(
        TEAM_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        page = response.read().decode(
            "utf-8",
            errors="replace"
        )

    feed_match = re.search(
        r'cjs\.initialFeeds\["results"\]\s*=\s*\{\s*data:\s*`(.*?)`',
        page,
        re.DOTALL
    )

    if not feed_match:
        raise RuntimeError(
            "Impossible de trouver les résultats Flashscore."
        )

    feed = feed_match.group(1)

    matches = []

    for record in feed.split("¬~"):

        match_id = get_value(record, "AA")
        timestamp = get_value(record, "AD")

        home = get_value(record, "AE")
        away = get_value(record, "AF")

        score_home = get_value(record, "AG")
        score_away = get_value(record, "AH")

        if not all([
            match_id,
            timestamp,
            home,
            away
        ]):
            continue

        if not (
            score_home.isdigit()
            and score_away.isdigit()
        ):
            continue

        try:
            timestamp = int(timestamp)
        except ValueError:
            continue

        matches.append({
            "id": match_id,
            "timestamp": timestamp,
            "home": home,
            "away": away,
            "score_home": int(score_home),
            "score_away": int(score_away)
        })

    if not matches:
        raise RuntimeError(
            "Aucun match terminé trouvé."
        )

    return max(
        matches,
        key=lambda match: match["timestamp"]
    )


# ==========================================
# OUTILS GRAPHIQUES
# ==========================================

def centered_text(draw, text, y, font, fill):

    box = draw.textbbox(
        (0, 0),
        text,
        font=font
    )

    text_width = box[2] - box[0]

    draw.text(
        ((WIDTH - text_width) / 2, y),
        text,
        font=font,
        fill=fill
    )


def fitted_font(text, max_width, initial_size):

    size = initial_size

    while size > 24:
        font = load_font(size, bold=True)

        box = font.getbbox(text)

        if box[2] - box[0] <= max_width:
            return font

        size -= 2

    return load_font(24, bold=True)


# ==========================================
# EFFET GLACE FISSUREE
# ==========================================

def draw_cracks(draw):

    cracks = [
        [(850, 100), (790, 240), (900, 330),
         (800, 460), (920, 590)],

        [(790, 240), (650, 300), (590, 430),
         (450, 500)],

        [(900, 330), (1010, 400), (950, 540),
         (1080, 650)],

        [(590, 430), (700, 550), (620, 690),
         (760, 820)],

        [(450, 500), (350, 640), (440, 760),
         (320, 900)]
    ]

    for crack in cracks:
        draw.line(
            crack,
            fill=(190, 225, 245),
            width=5
        )

        draw.line(
            [(x + 4, y + 4) for x, y in crack],
            fill=(75, 120, 155),
            width=2
        )


# ==========================================
# CREATION DE L'AFFICHE
# ==========================================

def create_poster(match):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        (9, 19, 37)
    )

    draw = ImageDraw.Draw(image)

    home_score = match["score_home"]
    away_score = match["score_away"]

    home = match["home"]
    away = match["away"]

    # Identifier le résultat de Fribourg

    fribourg_home = (
        "fribourg" in home.lower()
        or "gotteron" in home.lower()
        or "gottéron" in home.lower()
    )

    if fribourg_home:
        fribourg_score = home_score
        opponent_score = away_score
    else:
        fribourg_score = away_score
        opponent_score = home_score

    if fribourg_score > opponent_score:
        result = "VICTOIRE"
        accent = (60, 190, 145)
    elif fribourg_score < opponent_score:
        result = "DÉFAITE"
        accent = (220, 75, 85)
    else:
        result = "MATCH NUL"
        accent = (100, 175, 230)

    # Fond dégradé

    for y in range(HEIGHT):
        ratio = y / HEIGHT

        color = (
            int(9 + ratio * 9),
            int(19 + ratio * 18),
            int(37 + ratio * 25)
        )

        draw.line(
            [(0, y), (WIDTH, y)],
            fill=color
        )

    # Cadre

    draw.rounded_rectangle(
        (35, 35, WIDTH - 35, HEIGHT - 35),
        radius=35,
        outline=(85, 115, 145),
        width=3
    )

    # En-tête

    centered_text(
        draw,
        "FRIBOURG-GOTTÉRON",
        115,
        load_font(58, bold=True),
        (235, 242, 250)
    )

    centered_text(
        draw,
        result,
        310,
        load_font(100, bold=True),
        accent
    )

    centered_text(
        draw,
        "SCORE FINAL",
        500,
        load_font(30, bold=True),
        (160, 185, 210)
    )

    # Noms des équipes

    home_font = fitted_font(home, 850, 53)
    away_font = fitted_font(away, 850, 53)

    centered_text(
        draw,
        home,
        650,
        home_font,
        (245, 248, 255)
    )

    centered_text(
        draw,
        away,
        1010,
        away_font,
        (245, 248, 255)
    )

    # Score

    score_text = f"{home_score}  -  {away_score}"

    centered_text(
        draw,
        score_text,
        790,
        load_font(145, bold=True),
        (255, 255, 255)
    )

    # Effet de fissures en cas de défaite

    if result == "DÉFAITE":
        draw_cracks(draw)

    # Petite signature

    centered_text(
        draw,
        "HC FRIBOURG-GOTTÉRON",
        1190,
        load_font(24, bold=True),
        (130, 155, 180)
    )

    image.save(
        OUTPUT_FILE,
        quality=95
    )

    print("Affiche créée :", OUTPUT_FILE)
    print("Résultat :", home, home_score, "-", away_score, away)


# ==========================================
# PROGRAMME PRINCIPAL
# ==========================================

if __name__ == "__main__":

    print("Récupération des résultats...")

    latest_match = get_latest_match()

    print("Dernier match trouvé :")
    print(latest_match)

    create_poster(latest_match)

    print("TERMINÉ !")

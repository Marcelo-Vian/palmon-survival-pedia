import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"D:\Linkedin\palmon_survival_pedia")
THUMB_DIR = ROOT / "assets" / "shop_offer_thumbs"
OUT = ROOT / "shop_analyzer_screenshot_wide.png"
DATA = ROOT / "shop_active_offers_20260617.json"


def font(name: str, size: int):
    try:
        return ImageFont.truetype(name, size)
    except Exception:
        return ImageFont.load_default()


TITLE = font("arialbd.ttf", 44)
H2 = font("arialbd.ttf", 28)
BOLD = font("arialbd.ttf", 18)
TEXT = font("arial.ttf", 17)
SMALL = font("arial.ttf", 14)
TINY_BOLD = font("arialbd.ttf", 12)


def box(draw, x1, y1, x2, y2, fill="#ffffff", outline="#d2deed", radius=14):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=1)


def text(draw, xy, value, fill="#10233b", font_obj=TEXT):
    draw.text(xy, value, fill=fill, font=font_obj)


def paste_thumb(canvas, draw, name, x, y, size=(270, 106)):
    path = THUMB_DIR / f"{name}.jpg"
    if not path.exists():
        box(draw, x, y, x + size[0], y + size[1], "#eef6ff", "#c8d8ec", 10)
        text(draw, (x + 82, y + 42), "sem foto", "#667a93", SMALL)
        return
    thumb = Image.open(path).convert("RGB").resize(size)
    canvas.paste(thumb, (x, y))
    draw.rounded_rectangle([x, y, x + size[0], y + size[1]], radius=10, outline="#9fb7d3", width=1)


def card(canvas, draw, thumb, x, y, title, meta, score, price):
    box(draw, x, y, x + 292, y + 278, "#ffffff", "#cedcec", 12)
    paste_thumb(canvas, draw, thumb, x + 10, y + 10)
    text(draw, (x + 16, y + 132), title, "#10233b", BOLD)
    text(draw, (x + 16, y + 158), meta, "#52687f", SMALL)
    box(draw, x + 16, y + 186, x + 138, y + 226, "#eafaf2", "#b9e8d1", 8)
    text(draw, (x + 28, y + 198), score, "#08794f", BOLD)
    box(draw, x + 150, y + 186, x + 274, y + 226, "#f7fbff", "#d7e4f2", 8)
    text(draw, (x + 174, y + 198), price, "#10233b", BOLD)
    text(draw, (x + 16, y + 242), "ver detalhes / comparar", "#1769e0", SMALL)


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    offers = data.get("offers", [])
    priced = sum(1 for offer in offers if offer.get("price_brl") is not None)
    categories = {
        item.get("category")
        for offer in offers
        for item in offer.get("items", [])
        if item.get("category")
    }
    prices = [offer.get("price_brl") for offer in offers if offer.get("price_brl") is not None]
    lowest = min(prices) if prices else 0
    thumbs = sum(1 for offer in offers if (THUMB_DIR / f"{offer.get('id')}.jpg").exists())

    width, height = 1366, 900
    img = Image.new("RGB", (width, height), "#eef5fb")
    draw = ImageDraw.Draw(img)

    box(draw, 18, 20, width - 18, 92, "#ffffff", "#d2deed", 12)
    text(draw, (38, 38), "Palmon Survival - Shop Desk 2026", "#10233b", H2)
    for i, label in enumerate(["Hub", "Pedia", "Simulador"]):
        x = width - 316 + i * 94
        box(draw, x, 36, x + 82, 76, "#f8fbff", "#c8d8ec", 8)
        text(draw, (x + 20, 48), label, "#123154", SMALL)

    box(draw, 18, 112, width - 18, 286, "#ffffff", "#d2deed", 16)
    box(draw, 38, 132, 220, 165, "#e9f3ff", "#bcd4f5", 16)
    text(draw, (54, 141), "Loja reconstruida do zero", "#135fc8", TINY_BOLD)
    text(draw, (38, 184), "Comprar melhor, esperar melhor, gastar menos", "#0b2442", TITLE)
    text(
        draw,
        (40, 242),
        "Foto do pacote + filtro por recurso + custo-beneficio em uma tela nova para decidir o que vale comprar.",
        "#35516d",
        TEXT,
    )

    stats = [
        ("Ofertas", str(len(offers))),
        ("Fotos", str(thumbs)),
        ("Com preco", str(priced)),
        ("Categorias", str(len(categories))),
        ("Menor ticket", f"R$ {lowest:.2f}".replace(".", ",")),
    ]
    for i, (label, value) in enumerate(stats):
        x = 38 + i * 260
        box(draw, x, 308, x + 230, 392, "#ffffff", "#d2deed", 12)
        text(draw, (x + 14, 324), label.upper(), "#64748b", TINY_BOLD)
        text(draw, (x + 14, 350), value, "#10233b", H2)

    box(draw, 18, 416, width - 18, 520, "#ffffff", "#d2deed", 14)
    text(draw, (38, 436), "Objetivo atual", "#10233b", H2)
    goals = ["Pallite", "Acelerador", "Skillfruit", "Palmon", "Captura", "Passe"]
    for i, goal in enumerate(goals):
        x = 240 + i * 178
        fill = "#eaf3ff" if i == 0 else "#ffffff"
        box(draw, x, 438, x + 158, 490, fill, "#c8d8ec", 10)
        text(draw, (x + 18, 455), goal, "#10233b", BOLD)

    box(draw, 18, 544, width - 18, height - 24, "#ffffff", "#d2deed", 14)
    text(draw, (38, 566), "Biblioteca visual de ofertas", "#10233b", H2)
    text(draw, (38, 602), "Cards grandes para reconhecer o bundle no jogo e comparar score por objetivo.", "#52687f", TEXT)

    rows = [
        ("supply_7d_pallite", 38, 638, "7d Pallite Supply", "Weekly Camp Supply", "224,85/R$", "R$ 16,90"),
        ("growth_fund_ii", 354, 638, "Growth Fund II", "Growth Fund", "107,22/R$", "R$ 139,90"),
        ("pallite_24000_54990", 670, 638, "Pallite 12000+12000", "Pallite Store", "43,64/R$", "R$ 549,90"),
        ("bundle_skillfruits", 986, 638, "Skillfruits", "Bundle Store", "35,84/R$", "R$ 27,90"),
    ]
    for row in rows:
        card(img, draw, *row)

    img.save(OUT)
    print(f"Generated {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

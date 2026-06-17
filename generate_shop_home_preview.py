from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"D:\Linkedin\palmon_survival_pedia")
THUMB_DIR = ROOT / "assets" / "shop_offer_thumbs"
OUT = ROOT / "shop_analyzer_screenshot_wide.png"


def font(name: str, size: int):
    try:
        return ImageFont.truetype(name, size)
    except Exception:
        return ImageFont.load_default()


FONT_BOLD = font("arialbd.ttf", 28)
FONT_TITLE = font("arialbd.ttf", 34)
FONT = font("arial.ttf", 18)
SMALL = font("arial.ttf", 14)
TINY_BOLD = font("arialbd.ttf", 13)


def box(draw, x1, y1, x2, y2, fill="#ffffff", outline="#c9d8ea", radius=14):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=1)


def paste_thumb(canvas, draw, name, x, y, size=(150, 59)):
    path = THUMB_DIR / f"{name}.jpg"
    if not path.exists():
        return
    thumb = Image.open(path).convert("RGB").resize(size)
    canvas.paste(thumb, (x, y))
    draw.rounded_rectangle([x, y, x + size[0], y + size[1]], radius=8, outline="#9fb8d8", width=1)


def main():
    width, height = 1366, 900
    img = Image.new("RGB", (width, height), "#eef6ff")
    draw = ImageDraw.Draw(img)

    box(draw, 18, 18, width - 18, 96, "#ffffff", "#d4e1f0", 10)
    draw.text((36, 34), "Palmon Survival - Shop Table Analyzer", fill="#08213f", font=FONT_BOLD)
    draw.text(
        (36, 66),
        "Tabela extraida dos prints: pacotes, itens, precos, miniaturas e custo-beneficio.",
        fill="#49617e",
        font=SMALL,
    )
    for i, text in enumerate(["Pedia", "Montador", "Simulador"]):
        x = width - 280 + i * 88
        box(draw, x, 34, x + 78, 75, "#f8fbff", "#cddbf0", 8)
        draw.text((x + 15, 50), text, fill="#08213f", font=SMALL)

    box(draw, 20, 116, width - 20, 242, "#f8fbff", "#cbdcf3", 16)
    draw.text((42, 138), "Tabela com foto do pacote, itens e preco", fill="#09274a", font=FONT_TITLE)
    draw.text(
        (42, 184),
        "Os prints viraram dados pesquisaveis; cada oferta tem recorte pequeno para localizar o bundle no jogo.",
        fill="#26435f",
        font=FONT,
    )

    stats = [("Ofertas", "42"), ("Miniaturas", "42"), ("Com preco", "39"), ("Categorias", "15"), ("Menor ticket", "R$ 4,90")]
    for i, (label, value) in enumerate(stats):
        x = 42 + i * 250
        box(draw, x, 260, x + 220, 345, "#ffffff", "#d5e0ef", 12)
        draw.text((x + 16, 276), label.upper(), fill="#64748b", font=TINY_BOLD)
        draw.text((x + 16, 302), value, fill="#0b2442", font=FONT_BOLD)

    box(draw, 20, 370, width - 20, 470, "#ffffff", "#d5e0ef", 14)
    draw.text((42, 392), "Filtros", fill="#0b2442", font=FONT_BOLD)
    labels = ["Buscar pacote, item ou cap", "Todas categorias", "Todos status", "Ordenar por recurso", "Toda confianca"]
    for i, label in enumerate(labels):
        x = 42 + i * 255
        box(draw, x, 425, x + 235, 455, "#ffffff", "#b9c9df", 8)
        draw.text((x + 12, 433), label, fill="#63758d", font=SMALL)

    box(draw, 20, 492, width - 20, 610, "#ffffff", "#d5e0ef", 14)
    draw.text((42, 512), "Melhores decisoes rapidas", fill="#0b2442", font=FONT_BOLD)
    cards = [
        ("Melhor Pallite/R$", "Pallite Store - 12000+12000", "43,6 un/R$"),
        ("Melhor acelerador/R$", "Weekly Pass", "26,2 min/R$"),
        ("Skillfruit/R$", "Skillfruits", "35,8 un/R$"),
        ("Baixo gasto util", "7d Pallite Supply", "R$ 16,90"),
    ]
    for i, (title, offer, score) in enumerate(cards):
        x = 42 + i * 320
        box(draw, x, 548, x + 294, 595, "#f8fbff", "#d8e4f2", 10)
        draw.text((x + 12, 557), title, fill="#334155", font=TINY_BOLD)
        draw.text((x + 12, 575), offer + " - " + score, fill="#0f2d4d", font=SMALL)

    box(draw, 20, 632, width - 20, 872, "#ffffff", "#d5e0ef", 14)
    draw.text((42, 650), "Ofertas extraidas", fill="#0b2442", font=FONT_BOLD)
    headers = ["Visual", "Pacote", "Preco", "Itens", "Score", "Decisao", "Fonte"]
    xs = [42, 215, 430, 520, 790, 930, 1190]
    for x, header in zip(xs, headers):
        draw.text((x, 690), header.upper(), fill="#475569", font=TINY_BOLD)

    rows = [
        ("weekly_pass_animated_emoji", "Weekly Pass", "R$ 22,90", "Acelerador 1h x10", "26,2 min/R$", "bom se coletar diario", "loja1 cap19-22"),
        ("bundle_rapid_development", "Rapid Development", "R$ 27,90", "Acelerador 5 min x60", "10,8 min/R$", "acelerador barato", "loja1 cap27-33"),
        ("supply_7d_pallite", "7d Pallite Supply", "R$ 16,90", "Pallite 300 + 3500/7d", "224,9 un/R$", "melhor baixo custo", "loja1 cap23"),
        ("bundle_skillfruits", "Skillfruits", "R$ 27,90", "Skillfruit dourada x1000", "35,8 un/R$", "upar skill agora", "loja1 cap36-37"),
    ]
    for idx, row in enumerate(rows):
        y = 722 + idx * 36
        draw.line((42, y - 10, width - 42, y - 10), fill="#e4edf7")
        paste_thumb(img, draw, row[0], 42, y - 4)
        for x, text in zip(xs[1:], row[1:]):
            draw.text((x, y), text, fill="#0f2742", font=SMALL)

    img.save(OUT)
    print(f"Generated {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()

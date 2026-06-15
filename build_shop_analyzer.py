import html
import json
import pathlib
import re
import sys
import unicodedata
from collections import defaultdict


ROOT = pathlib.Path(r"D:\Linkedin")
PEDIA_DIR = ROOT / "palmon_survival_pedia"
APK_ANALYSIS = ROOT / "palmon_survival_apk" / "analysis"
CONFIG_ROOT = APK_ANALYSIS / "lua_decrypted_config_root"
CONFIG_SELECTED = APK_ANALYSIS / "lua_decrypted_selected"
TOOLS_DIR = APK_ANALYSIS / "tools"
LANG_PT_BR = APK_ANALYSIS / "localization_textassets" / "language_pt_BR.lua"
LANG_DIR = APK_ANALYSIS / "localization_textassets"
OUT_HTML = PEDIA_DIR / "palmon_shop_analyzer.html"
ICON_MANIFEST = PEDIA_DIR / "assets" / "item_icons" / "item_icon_manifest.json"

sys.path.insert(0, str(TOOLS_DIR))
from parse_lua_configs import read_inline_or_split  # noqa: E402


SHOP_TYPE = {
    1: "Loja base",
    2: "Loja da Guilda",
    4: "Loja VIP",
    6: "Loja de Prestigio",
    7: "Loja de Prova",
    10: "Compra de recursos",
    11: "Loja de Prestigio",
    12: "Loja de temporada",
}

FRESH_TYPE = {
    -1: "Sem renovacao",
    0: "Nao informado",
    1: "Diario",
    2: "Semanal",
    3: "Mensal",
}

DROP_TYPE = {
    1: "Pallitas",
    3: "Item",
    4: "Palmon",
    5: "Tropa",
    6: "Ouro",
    7: "Tabuas",
    8: "Aco",
    10: "Moeda",
    11: "Energia",
    13: "Skin",
    14: "Titulo",
    15: "Moldura",
    16: "Arma",
    19: "Bau de alianca",
    20: "Stamina de carta",
    21: "Serum",
    22: "Alma",
    26: "Equipamento",
    27: "Chip",
}

SOURCE_NOTES = {
    "shop": "Confirmado em shop.lua: venda, preco, limite e renovacao aparecem na tabela do cliente.",
    "shop_discount": "Confirmado em shop_discount.lua: loja de desconto/VIP; condicao costuma ser nivel VIP.",
    "shop_medals": "Confirmado em shop_medals.lua: loja por medalhas/moeda de evento.",
    "shop_post_season": "Confirmado em shop_post_season.lua: loja pos-temporada; pode depender da temporada do servidor.",
    "shop_skin": "Confirmado em shop_skin.lua: loja de skins.",
    "activity_blackjack_shop": "Confirmado em activity_blackjack_shop.lua; loja temporaria de evento.",
    "activity_eagle_shop": "Confirmado em activity_eagle_shop.lua; loja temporaria de evento.",
    "activity_goldrobber_shop": "Confirmado em activity_goldrobber_shop.lua; loja temporaria de evento.",
    "activity_thanksgiving_shop": "Confirmado em activity_thanksgiving_shop.lua; loja temporaria de evento.",
    "activity_totalwar_shop": "Confirmado em activity_totalwar_shop.lua; loja temporaria de evento.",
    "week_theme_activity_shop": "Confirmado em week_theme_activity_shop.lua; loja de atividade semanal/tematica.",
    "gift_package": "Confirmado em gift_package.lua: conteudo de pacote/bau pequeno; nao prova que esta a venda hoje.",
}


def parse_l10n(path: pathlib.Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    out: dict[str, str] = {}
    pattern = re.compile(r'^\s*([A-Za-z0-9_]+)\s*=\s*"((?:\\.|[^"\\])*)"\s*,?\s*$', re.M)
    escapes = {
        r"\\": "\\",
        r"\"": '"',
        r"\n": "\n",
        r"\r": "\r",
        r"\t": "\t",
    }
    for key, raw in pattern.findall(text):
        value = raw
        for old, new in escapes.items():
            value = value.replace(old, new)
        if value and value != "#N/A":
            out[key] = value
    return out


LANG_PRIORITY = [
    "pt_BR",
    "en",
    "esla",
    "es",
    "zh_CN",
    "zh_TW",
    "fr",
    "de",
    "it",
    "ja",
    "ko",
    "ru",
    "vi",
    "th",
    "tr",
    "id",
    "pl",
    "po",
]


def load_l10n_by_lang() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for lang in LANG_PRIORITY:
        path = LANG_DIR / f"language_{lang}.lua"
        if path.exists():
            out[lang] = parse_l10n(path)
    for path in sorted(LANG_DIR.glob("language_*.lua")):
        lang = path.stem.removeprefix("language_")
        if lang not in out:
            out[lang] = parse_l10n(path)
    return out


L10N_BY_LANG = load_l10n_by_lang()
L10N = L10N_BY_LANG.get("pt_BR", {})


def loc(key, fallback=""):
    if key is None:
        return fallback
    if isinstance(key, list):
        return " / ".join(loc(item) for item in key if loc(item))
    key_text = str(key)
    return L10N.get(key_text, fallback or key_text)


def loc_info(key, fallback=""):
    if key is None:
        return {"value": fallback, "lang": "", "status": "fallback"}
    key_text = str(key)
    for lang, table in L10N_BY_LANG.items():
        value = table.get(key_text)
        if value and value != "#N/A":
            status = "oficial_pt_BR" if lang == "pt_BR" else f"fallback_{lang}"
            return {"value": value, "lang": lang, "status": status}
    return {"value": fallback, "lang": "", "status": "fallback"}


def ascii_fold(text):
    replacements = {
        "á": "a",
        "à": "a",
        "ã": "a",
        "â": "a",
        "ä": "a",
        "Á": "a",
        "À": "a",
        "Ã": "a",
        "Â": "a",
        "é": "e",
        "è": "e",
        "ê": "e",
        "ë": "e",
        "É": "e",
        "Ê": "e",
        "í": "i",
        "ì": "i",
        "î": "i",
        "ï": "i",
        "Í": "i",
        "ó": "o",
        "ò": "o",
        "õ": "o",
        "ô": "o",
        "ö": "o",
        "Ó": "o",
        "Õ": "o",
        "Ô": "o",
        "ú": "u",
        "ù": "u",
        "û": "u",
        "ü": "u",
        "Ú": "u",
        "ç": "c",
        "Ç": "c",
        " ": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", text) if not unicodedata.combining(ch)
    )


def norm(text):
    return re.sub(r"[^a-z0-9]+", " ", ascii_fold(str(text)).lower()).strip()


def esc(value):
    return html.escape(str(value), quote=True)


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def number(value):
    try:
        if value in ("", None):
            return None
        return float(value)
    except Exception:
        return None


def format_num(value):
    if value in ("", None):
        return ""
    if isinstance(value, bool):
        return "sim" if value else "nao"
    if isinstance(value, (int, float)):
        if abs(float(value) - int(float(value))) < 0.001:
            return f"{int(value):,}".replace(",", ".")
        if 0 < abs(float(value)) < 1:
            return f"{float(value):,.4f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return str(value)


INFERRED_ITEM_NAMES = {
    "921": {
        "name": "Moeda do Bazar da Fogueira",
        "note": "Nome inferido pela descricao pt_BR e por constant_func.lua: shop_post_season_currency = 921.",
    },
    "1029": {
        "name": "Moeda/Item Total War",
        "note": "Nome tecnico inferido por constant_func.lua: totalwar_item = 1029. A localizacao pt_BR/en nao traz nome oficial.",
    },
}

INFERRED_ITEM_DEFS = {
    "314": {
        "name": "Material de Hero Fate / Afinidade",
        "note": "Nome oficial nao apareceu nas localizacoes 2026. O uso foi inferido por hero_fate.lua e constant_func.lua, onde o ID 314 entra como consumo importante do sistema hero_fate.",
        "source": "hero_fate.lua + constant_func.hero_fate_reset_item",
    },
    "818": {
        "name": "Moeda do evento Goldrobber (S0/S2)",
        "note": "Inferido de activity_goldrobber_shop.lua e activity_goldrobber_monsterreward.lua: o ID 818 e usado como moeda do evento nas temporadas 0 e 2.",
        "source": "activity_goldrobber_shop.lua + activity_goldrobber_monsterreward.lua",
    },
    "819": {
        "name": "Material comum de resgate da montaria Swiftger",
        "note": "Inferido de home_mount.lua: a montaria Swiftger usa 90.000 do ID 819 e 150 do ID 820 no resgate 'Alianca Rugidora'. Tambem cai em eventos/monstros e aparece em lojas sazonais.",
        "source": "home_mount.lua redemption_cost + constant_func.home_mount",
        "icon_texture": "item_mount_update",
    },
    "820": {
        "name": "Material raro de resgate da montaria Swiftger",
        "note": "Inferido de home_mount.lua: a montaria Swiftger usa 150 do ID 820 junto com o ID 819 no resgate 'Alianca Rugidora'.",
        "source": "home_mount.lua redemption_cost + constant_func.home_mount",
        "icon_texture": "item_mount_update",
    },
    "831": {
        "name": "Item de refresh do Comercio Aereo",
        "note": "Inferido de constant_func.lua: airship_trade_refresh_item = 831.",
        "source": "constant_func.airship_trade_refresh_item",
    },
    "833": {
        "name": "Essencia de Evolucao",
        "note": "Inferido de constant_func.lua: hero_evolve_item_reset liga 833 -> 928, e o ID 928 tem nome oficial 'Essencia de Evolucao (reembolso)'.",
        "source": "constant_func.hero_evolve_item_reset + item_itemname_928",
        "icon_texture": "item_icon_evolve01",
    },
    "853": {
        "name": "Material sazonal raro de progressao",
        "note": "Nome oficial nao apareceu nas localizacoes 2026. O item aparece em recompensas de activity_precious_reward, week_theme_activity_shop e shop_post_season.",
        "source": "activity_precious_reward.lua + week_theme_activity_shop.lua + shop_post_season.lua",
    },
    "900004": {
        "name": "Item de reset de captura de Boss",
        "note": "Inferido de constant_func.lua: boss_reset_return e boss_reset_regeneration usam o ID 900004 para reset/regeneracao do sistema de captura de boss.",
        "source": "constant_func.boss_reset_return + boss_reset_regeneration",
        "icon_texture": "item_icon_boss01",
    },
    "900005": {
        "name": "Item de reset de nivel de Boss",
        "note": "Inferido de constant_func.lua: boss_lvup_reset_Prop = 900005.",
        "source": "constant_func.boss_lvup_reset_Prop",
        "icon_texture": "item_icon_boss02",
    },
    "911": {
        "name": "Moeda do evento Goldrobber (S1)",
        "note": "Inferido de activity_goldrobber_shop.lua e activity_goldrobber_monsterreward.lua: o ID 911 substitui o 818 como moeda da temporada 1 do evento.",
        "source": "activity_goldrobber_shop.lua + activity_goldrobber_monsterreward.lua",
    },
    "2128": {
        "name": "Material de EXP de Equipamento (medio)",
        "note": "Inferido de constant_func.lua: o ID 2128 faz parte do trio equip_up_item_id = {2127,2128,2129}, e a descricao oficial 2026 indica EXP moderada de equipamento.",
        "source": "constant_func.equip_up_item_id + item_remarks_2128",
        "icon_texture": "item_icon_dust3",
    },
    "2129": {
        "name": "Material de EXP de Equipamento (pequeno)",
        "note": "Inferido de constant_func.lua: o ID 2129 completa o trio equip_up_item_id = {2127,2128,2129}. O cliente nao trouxe o nome oficial nas localizacoes 2026 extraidas.",
        "source": "constant_func.equip_up_item_id",
        "icon_texture": "item_icon_dust",
    },
}


def numeric_item_id(value):
    return bool(re.fullmatch(r"\d+", str(value or "").strip()))


def load_icon_items():
    if not ICON_MANIFEST.exists():
        return []
    try:
        data = json.loads(ICON_MANIFEST.read_text(encoding="utf-8"))
    except Exception:
        return []
    return data.get("items", [])


def icon_rank(icon):
    asset_path = str(icon.get("asset_path", "")).lower()
    texture = str(icon.get("texture_name", "")).lower()
    return (0 if "/uiitem/" in asset_path else 1, texture)


def put_icon(mapping, key, icon):
    if not key:
        return
    key = str(key).strip().lower()
    if not key:
        return
    current = mapping.get(key)
    if current is None or icon_rank(icon) < icon_rank(current):
        mapping[key] = icon


ICON_ITEMS = load_icon_items()
ICON_BY_TEXTURE = {}
ICON_BY_RESOURCE_ID = {}
ICON_BY_ITEM_ID = {}
ICON_BY_PALMON_CHIP = {}

for icon in ICON_ITEMS:
    for key in (
        icon.get("texture_name"),
        pathlib.PurePosixPath(str(icon.get("asset_path", ""))).name,
        pathlib.PurePosixPath(str(icon.get("container", ""))).name,
    ):
        put_icon(ICON_BY_TEXTURE, key, icon)

    if icon.get("resource_id") not in ("", None):
        put_icon(ICON_BY_RESOURCE_ID, icon.get("resource_id"), icon)

    for key in (
        str(icon.get("texture_name", "")).lower(),
        pathlib.PurePosixPath(str(icon.get("asset_path", ""))).name.lower(),
    ):
        for pattern in (r"^item_(\d+)_icon$", r"^item_icon_(\d+)$"):
            match = re.match(pattern, key)
            if match:
                put_icon(ICON_BY_ITEM_ID, match.group(1).lstrip("0") or "0", icon)
        match = re.match(r"^palmon_chip_(\d+)$", key)
        if match:
            put_icon(ICON_BY_PALMON_CHIP, match.group(1), icon)


def icon_by_texture(*keys):
    for key in keys:
        icon = ICON_BY_TEXTURE.get(str(key).lower())
        if icon:
            return icon
    return None


def icon_result(icon, status, source):
    if not icon:
        return {
            "icon": "",
            "icon_status": "sem_icone",
            "icon_source": "Icone nao confirmado no pacote extraido.",
            "icon_texture": "",
        }
    return {
        "icon": icon.get("png_rel", ""),
        "icon_status": status,
        "icon_source": source,
        "icon_texture": icon.get("texture_name", ""),
    }


def palmon_chip_id_from_item_id(item_id):
    text = str(item_id or "").strip()
    # Fichas aparecem como 103201/104003/105023 e reembolsos como 9103201/9104003.
    if len(text) == 6 and text.startswith(("103", "104", "105")):
        return text[2:]
    if len(text) == 7 and text.startswith("910"):
        return text[3:]
    return ""


def norm_has_phrase(blob, phrase):
    return re.search(rf"(^| ){re.escape(phrase)}($| )", blob) is not None


def infer_name_from_desc(raw_id, desc):
    blob = norm(desc)
    if not blob:
        return None
    if "aprimorar equipamentos" in blob and "grande quantidade de exp" in blob:
        return {
            "name": "Material de EXP de Equipamento (grande)",
            "note": "Nome funcional inferido pela descricao oficial 2026: material usado para dar muita EXP de equipamento.",
            "source": f"item_remarks_{raw_id}",
            "icon_texture": "item_icon_dust2",
            "status": "inferido_desc",
        }
    if "aprimorar equipamentos" in blob and ("moderada quantidade de exp" in blob or "quantidade moderada de exp" in blob):
        return {
            "name": "Material de EXP de Equipamento (medio)",
            "note": "Nome funcional inferido pela descricao oficial 2026: material usado para dar EXP moderada de equipamento.",
            "source": f"item_remarks_{raw_id}",
            "icon_texture": "item_icon_dust3",
            "status": "inferido_desc",
        }
    if "aprimorar equipamentos" in blob and ("pequena quantidade de exp" in blob or "pouca quantidade de exp" in blob):
        return {
            "name": "Material de EXP de Equipamento (pequeno)",
            "note": "Nome funcional inferido pela descricao oficial 2026: material usado para dar pouca EXP de equipamento.",
            "source": f"item_remarks_{raw_id}",
            "icon_texture": "item_icon_dust",
            "status": "inferido_desc",
        }
    if "ascender o nivel estelar de um equipamento" in blob:
        return {
            "name": "Material de Ascensao Estelar de Equipamento",
            "note": "Nome funcional inferido pela descricao oficial 2026: material essencial para subir estrela de equipamento.",
            "source": f"item_remarks_{raw_id}",
            "icon_texture": "item_icon_evolve06",
            "status": "inferido_desc",
        }
    if "melhorar a base ao ranque mestre" in blob:
        return {
            "name": "Item de promocao da Base para Ranque Mestre",
            "note": "Nome funcional inferido pela descricao oficial 2026.",
            "source": f"item_remarks_{raw_id}",
            "status": "inferido_desc",
        }
    if "variedade de itens uteis" in blob:
        return {
            "name": "Bau de Itens Uteis",
            "note": "Nome funcional inferido pela descricao oficial 2026.",
            "source": f"item_remarks_{raw_id}",
            "status": "inferido_desc",
        }
    if "motociclistas" in blob and "recluta" in blob:
        return {
            "name": "Convocacao de Motociclistas",
            "note": "Nome funcional inferido pela descricao localizada de 2026.",
            "source": f"item_remarks_{raw_id}",
            "status": "inferido_desc",
        }
    return None


def inferred_item_def(raw_id, desc=""):
    manual = INFERRED_ITEM_DEFS.get(str(raw_id))
    if manual:
        return {
            "name": manual["name"],
            "note": manual.get("note", ""),
            "source": manual.get("source", f"inferencia_manual_{raw_id}"),
            "icon_texture": manual.get("icon_texture", ""),
            "status": "inferido_config",
        }
    return infer_name_from_desc(raw_id, desc)


def icon_for_reward(kind, param, name="", desc="", type_name=""):
    raw_id = "" if param is None else str(param).strip()
    item_id = raw_id.lstrip("0") or raw_id

    if kind == 3:
        direct = ICON_BY_ITEM_ID.get(item_id)
        if direct:
            return icon_result(direct, "icone_id_direto", f"asset item_icon/item_id {item_id}")

        inferred = inferred_item_def(item_id, desc)
        if inferred and inferred.get("icon_texture"):
            icon = icon_by_texture(inferred["icon_texture"])
            if icon:
                return icon_result(
                    icon,
                    "icone_inferido_config",
                    f"{inferred['name']}: icone inferido por {inferred['source']}",
                )

        chip_id = palmon_chip_id_from_item_id(item_id)
        if chip_id:
            chip = ICON_BY_PALMON_CHIP.get(chip_id)
            if chip:
                return icon_result(chip, "icone_chip_inferido", f"Palmon_chip_{chip_id} inferido de item {item_id}")

        blob = norm(f"{name} {desc} {type_name} {item_id}")
        heuristics = [
            ("ovo de palmon", "recruit_icon_recruitegg2", "Ovo de Palmon"),
            ("escudo de base", "item_icon_shield", "Escudo de Base"),
            ("movedor de base direcionado", "item_icon_move3", "Movedor de Base direcionado"),
            ("movedor de base guilda", "item_icon_move2", "Movedor de Base guilda"),
            ("movedor de base aleatorio", "item_icon_move1", "Movedor de Base aleatorio"),
            ("bau de eletricidade", "item_icon_elec2", "Bau de Eletricidade"),
            ("eletricidade", "item_icon_elec2", "Eletricidade"),
            ("aco", "item_icon_steel2", "Aco"),
        ]
        for needle, texture, label in heuristics:
            if norm_has_phrase(blob, needle):
                icon = icon_by_texture(texture)
                if icon:
                    return icon_result(icon, "icone_heuristico", f"{label}: inferido por nome/descricao")

    fixed_kind_icons = {
        1: ("money_icon_1", "Pallitas"),
        6: ("money_icon_6", "Ouro"),
        7: ("money_icon_7", "Tabuas"),
        8: ("money_icon_8", "Aco"),
        11: ("item_icon_0240", "Energia"),
    }
    if kind in fixed_kind_icons:
        texture, label = fixed_kind_icons[kind]
        icon = icon_by_texture(texture)
        if icon:
            return icon_result(icon, "icone_tipo_cliente", f"{label}: tipo {kind} do cliente")

    if kind == 10:
        direct = ICON_BY_ITEM_ID.get(item_id)
        if direct:
            return icon_result(direct, "icone_id_direto", f"moeda/recurso item_icon_{item_id}")
        icon = icon_by_texture(f"money_icon_{item_id}", f"item_icon_{item_id}")
        if icon:
            return icon_result(icon, "icone_tipo_cliente", f"moeda/recurso droptype {item_id}")

    return icon_result(None, "sem_icone", "Icone nao ligado com seguranca ao ID.")


def clean_desc(text):
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", str(text)).strip()


def fallback_symbol(kind, name, param):
    blob = norm(f"{kind} {name} {param}")
    if "pallitas" in blob:
        return "P"
    if "ouro" in blob:
        return "Au"
    if "aco" in blob or "steel" in blob:
        return "Ac"
    if "tabua" in blob or "wood" in blob:
        return "Tb"
    if "energia" in blob or "stamina" in blob or "ap" in blob:
        return "EN"
    if "bau" in blob or "chest" in blob:
        return "Bx"
    if "ficha" in blob or "palmon" in blob:
        return "Pa"
    if "moeda" in blob or "coin" in blob:
        return "$"
    return str(param or "?")[:3]


def item_meta(item_id, kind=3, type_name="Item"):
    raw_id = "" if item_id is None else str(item_id)
    if kind == 1:
        return {
            "name": loc("droptype_name_1", "Pallitas"),
            "desc": "Moeda premium/base usada em varias lojas.",
            "status": "oficial_pt_BR" if "droptype_name_1" in L10N else "padrao_cliente",
            "source": "droptype_name_1 / DROP_TYPE",
            "visual": "P",
            "visual_kind": "currency",
        }
    if kind == 6:
        return {"name": "Ouro", "desc": "Recurso economico.", "status": "padrao_cliente", "source": "DROP_TYPE", "visual": "Au", "visual_kind": "resource"}
    if kind == 7:
        return {"name": "Tabuas", "desc": "Recurso de construcao/base.", "status": "padrao_cliente", "source": "DROP_TYPE", "visual": "Tb", "visual_kind": "resource"}
    if kind == 8:
        return {"name": "Aco", "desc": "Recurso de construcao/base.", "status": "padrao_cliente", "source": "DROP_TYPE", "visual": "Ac", "visual_kind": "resource"}
    if kind == 11:
        return {"name": "Energia", "desc": "Energia/stamina usada por atividades.", "status": "padrao_cliente", "source": "DROP_TYPE", "visual": "EN", "visual_kind": "resource"}
    if kind == 10:
        info = loc_info(f"droptype_name_{raw_id}", f"Moeda #{raw_id}")
        name = info["value"]
        status = info["status"]
        desc = "Moeda/recurso localizado por droptype."
        if status == "fallback":
            desc = "Nome oficial nao encontrado nas localizacoes extraidas."
        elif status.startswith("fallback_"):
            lang = info.get("lang") or status.replace("fallback_", "")
            name = f"{name} (fallback {lang})"
            desc = f"Nome veio do fallback de idioma {lang}, porque pt_BR nao tinha entrada."
        return {
            "name": name,
            "desc": desc,
            "status": status,
            "source": f"droptype_name_{raw_id}",
            "visual": fallback_symbol(kind, name, raw_id),
            "visual_kind": "currency",
        }
    if kind == 4:
        name = hero_name(item_id)
        return {
            "name": name,
            "desc": "Palmon/criatura como recompensa.",
            "status": "oficial_pt_BR" if not name.startswith("Palmon #") else "nao_confirmado",
            "source": f"hero_name_{raw_id}",
            "visual": "Pa",
            "visual_kind": "palmon",
        }
    if kind != 3:
        name = DROP_TYPE.get(kind, f"Tipo {kind}")
        suffix = f" #{raw_id}" if raw_id not in ("", "0") else ""
        return {
            "name": f"{name}{suffix}",
            "desc": "Tipo de recompensa confirmado no cliente; nome detalhado depende de configuracao especifica.",
            "status": "padrao_cliente",
            "source": "DROP_TYPE",
            "visual": fallback_symbol(kind, name, raw_id),
            "visual_kind": "resource",
        }

    name_info = loc_info(f"item_itemname_{raw_id}", "")
    desc_info = loc_info(f"item_remarks_{raw_id}", "")
    name = name_info["value"]
    status = name_info["status"]
    source = f"item_itemname_{raw_id}"
    note = ""

    desc = clean_desc(desc_info["value"])
    if desc and desc_info["status"].startswith("fallback_"):
        lang = desc_info.get("lang") or desc_info["status"].replace("fallback_", "")
        desc = f"{desc} Descricao veio do fallback de idioma {lang}, porque pt_BR nao tinha entrada."
    inferred = inferred_item_def(raw_id, desc)

    if not name:
        if inferred:
            name = inferred["name"]
            status = inferred.get("status", "inferido_config")
            source = inferred.get("source", f"inferencia_manual_{raw_id}")
            note = inferred.get("note", "")
        else:
            inferred_name = INFERRED_ITEM_NAMES.get(raw_id)
            if inferred_name:
                name = inferred_name["name"]
                status = "inferido_config"
                source = f"constant_func.lua / item_remarks_{raw_id}"
                note = inferred_name["note"]
            else:
                name = f"Material sem nome localizado (ID {raw_id})"
                status = "nao_confirmado"
                source = f"item_itemname_{raw_id} ausente nas localizacoes extraidas"

    if not desc and note:
        desc = note
    elif note:
        desc = f"{desc} {note}".strip()
    if not desc:
        desc = "Descricao nao confirmada nas localizacoes 2026 extraidas."

    if status.startswith("fallback_"):
        lang = name_info.get("lang") or status.replace("fallback_", "")
        desc = f"{desc} Nome veio do fallback de idioma {lang}, porque pt_BR nao tinha entrada."

    return {
        "name": name,
        "desc": desc,
        "status": status,
        "source": source,
        "visual": fallback_symbol(kind, name, raw_id),
        "visual_kind": "unknown" if status == "nao_confirmado" else "item",
    }


def item_name(item_id):
    return item_meta(item_id)["name"]


def hero_name(hero_id):
    raw = str(hero_id)
    candidates = [f"hero_name_{raw}"]
    if raw.startswith("20") and len(raw) >= 5:
        candidates.append(f"hero_name_{raw[2:]}")
    if len(raw) >= 4:
        candidates.append(f"hero_name_{raw[-4:]}")
    for key in candidates:
        if key in L10N:
            return L10N[key]
    return f"Palmon #{hero_id}"


def droptype_name(kind, param):
    if kind == 1:
        return loc("droptype_name_1", "Pallitas")
    if kind == 3:
        return item_meta(param, kind=3)["name"]
    if kind == 4:
        return hero_name(param)
    if kind in (6, 7, 8):
        return DROP_TYPE[kind]
    if kind == 10:
        return item_meta(param, kind=10, type_name="Moeda/Recurso")["name"]
    return DROP_TYPE.get(kind, f"Tipo {kind}") + (f" #{param}" if param not in (None, "", 0) else "")


def reward_key(kind, param):
    if kind in (1, 6, 7, 8):
        return f"{kind}:0"
    return f"{kind}:{param}"


def parse_reward(value):
    if not isinstance(value, list) or len(value) < 3:
        return None
    kind, param, qty = value[0], value[1], value[2]
    type_name = DROP_TYPE.get(kind, f"Tipo {kind}")
    meta = item_meta(param, kind=kind, type_name=type_name)
    icon = icon_for_reward(kind, param, meta["name"], meta["desc"], type_name)
    return {
        "kind": kind,
        "param": param,
        "qty": qty,
        "key": reward_key(kind, param),
        "name": meta["name"],
        "desc": meta["desc"],
        "meta_status": meta["status"],
        "meta_source": meta["source"],
        "visual": meta["visual"],
        "visual_kind": meta["visual_kind"],
        "icon": icon["icon"],
        "icon_status": icon["icon_status"],
        "icon_source": icon["icon_source"],
        "icon_texture": icon["icon_texture"],
        "type_name": type_name,
        "raw": value,
    }


def parse_price(value, table_name=""):
    if isinstance(value, list) and len(value) >= 3:
        kind, param, qty = value[0], value[1], value[2]
        if qty in (None, "", []) or not isinstance(kind, int):
            return {
                "kind": None,
                "param": None,
                "qty": None,
                "key": "",
                "name": "Preco nao informado",
                "text": "Preco nao informado",
                "raw": value,
            }
        return {
            "kind": kind,
            "param": param,
            "qty": qty,
            "key": reward_key(kind, param),
            "name": droptype_name(kind, param),
            "text": f"{format_num(qty)} {droptype_name(kind, param)}",
            "raw": value,
        }
    if value not in (None, "", 0):
        suffix = "moeda do evento"
        if table_name == "activity_blackjack_shop":
            suffix = "moeda do Blackjack"
        elif table_name == "activity_eagle_shop":
            suffix = "moeda do evento Eagle"
        elif table_name == "activity_thanksgiving_shop":
            suffix = "moeda do evento Thanksgiving"
        return {
            "kind": "event",
            "param": table_name,
            "qty": value,
            "key": f"event:{table_name}",
            "name": suffix,
            "text": f"{format_num(value)} {suffix}",
            "raw": value,
        }
    return {
        "kind": None,
        "param": None,
        "qty": None,
        "key": "",
        "name": "Preco nao informado",
        "text": "Preco nao informado",
        "raw": value,
    }


def condition_text(value):
    if value in (None, "", [], 0):
        return ""
    if isinstance(value, list):
        if len(value) == 2 and value[0] == 61:
            return f"VIP >= {value[1]}"
        if len(value) == 2 and value[0] == 1:
            return f"Predio/base >= {value[1]}"
        return "condicao " + json.dumps(value, ensure_ascii=False)
    return str(value)


def add_direct_offer(offers, *, table, row, source, reward_value, price_value=None, limit=None, refresh="", evidence="confirmado", note=""):
    reward = parse_reward(reward_value)
    if not reward:
        return
    price = parse_price(price_value, table)
    qty = number(reward.get("qty"))
    price_qty = number(price.get("qty"))
    unit_cost = None
    if qty and price_qty:
        unit_cost = price_qty / qty
    conditions = []
    for key in ("condition", "open_lv", "server_day", "open_week", "season", "version", "activity"):
        value = row.get(key)
        text = condition_text(value)
        if text:
            label = {
                "condition": "condicao",
                "open_lv": "base",
                "server_day": "dia servidor",
                "open_week": "semana",
                "season": "temporada",
                "version": "versao",
                "activity": "atividade",
            }[key]
            conditions.append(f"{label}: {text}")
    offers.append(
        {
            "id": str(row.get("id") or row.get("ID") or ""),
            "table": table,
            "source": source,
            "source_note": SOURCE_NOTES.get(table, ""),
            "item_key": reward["key"],
            "item_name": reward["name"],
            "item_desc": reward["desc"],
            "item_meta_status": reward["meta_status"],
            "item_meta_source": reward["meta_source"],
            "item_visual": reward["visual"],
            "item_visual_kind": reward["visual_kind"],
            "item_icon": reward["icon"],
            "item_icon_status": reward["icon_status"],
            "item_icon_source": reward["icon_source"],
            "item_icon_texture": reward["icon_texture"],
            "item_norm": norm(f"{reward['name']} {reward['desc']} {reward['param']} {reward['type_name']} {reward['meta_status']}"),
            "item_type": reward["type_name"],
            "reward_kind": reward["kind"],
            "reward_param": reward["param"],
            "qty": reward["qty"],
            "qty_text": format_num(reward["qty"]),
            "price_text": price["text"],
            "price_key": price["key"],
            "price_name": price["name"],
            "price_qty": price["qty"],
            "unit_cost": unit_cost,
            "unit_cost_text": format_num(unit_cost) if unit_cost is not None else "",
            "limit": limit if limit not in (None, "", 0, -1) else "",
            "refresh": refresh,
            "discount": row.get("discount") or "",
            "before_price": row.get("before_price") or "",
            "conditions": "; ".join(conditions),
            "evidence": evidence,
            "note": note,
        }
    )


def load_table(name):
    return read_inline_or_split(CONFIG_ROOT, CONFIG_SELECTED, name)


def build_direct_offers():
    offers = []

    for row in load_table("shop"):
        refresh = FRESH_TYPE.get(row.get("fresh_type"), str(row.get("fresh_type")))
        source = SHOP_TYPE.get(row.get("type"), f"Loja tipo {row.get('type')}")
        add_direct_offer(
            offers,
            table="shop",
            row=row,
            source=source,
            reward_value=row.get("shop_sale"),
            price_value=row.get("price"),
            limit=row.get("buymax"),
            refresh=refresh,
        )

    for row in load_table("shop_discount"):
        add_direct_offer(
            offers,
            table="shop_discount",
            row=row,
            source="Loja de desconto/VIP",
            reward_value=row.get("item_id"),
            price_value=row.get("price"),
            limit=row.get("buy_num"),
            refresh="Condicao/VIP",
        )

    for row in load_table("shop_medals"):
        add_direct_offer(
            offers,
            table="shop_medals",
            row=row,
            source="Loja de medalhas",
            reward_value=row.get("shop_sale"),
            price_value=row.get("price"),
            limit="",
            refresh="Rotacao/medalhas",
        )

    for row in load_table("shop_post_season"):
        add_direct_offer(
            offers,
            table="shop_post_season",
            row=row,
            source="Loja pos-temporada",
            reward_value=row.get("shop_sale"),
            price_value=row.get("price"),
            limit=row.get("buymax"),
            refresh=FRESH_TYPE.get(row.get("fresh_type"), ""),
        )

    for row in load_table("shop_skin"):
        add_direct_offer(
            offers,
            table="shop_skin",
            row=row,
            source="Loja de skins",
            reward_value=row.get("shop_sale"),
            price_value=row.get("price"),
            limit="",
            refresh="Permanente/rotacao",
        )

    event_tables = [
        ("activity_blackjack_shop", "Evento Blackjack"),
        ("activity_eagle_shop", "Evento Eagle"),
        ("activity_goldrobber_shop", "Evento Goldrobber"),
        ("activity_thanksgiving_shop", "Evento Thanksgiving"),
    ]
    for table_name, source in event_tables:
        for row in load_table(table_name):
            add_direct_offer(
                offers,
                table=table_name,
                row=row,
                source=source,
                reward_value=row.get("shop_sale"),
                price_value=row.get("price"),
                limit=row.get("buynum"),
                refresh="Evento ativo",
            )

    for row in load_table("activity_totalwar_shop"):
        add_direct_offer(
            offers,
            table="activity_totalwar_shop",
            row=row,
            source="Evento Total War",
            reward_value=row.get("itemid"),
            price_value=row.get("exchangenum"),
            limit=row.get("exchangemaxnum"),
            refresh="Evento ativo",
        )

    for row in load_table("week_theme_activity_shop"):
        add_direct_offer(
            offers,
            table="week_theme_activity_shop",
            row=row,
            source="Evento semanal/tematico",
            reward_value=row.get("goods"),
            price_value=row.get("price"),
            limit=row.get("buynum"),
            refresh="Evento semanal",
        )

    for row in load_table("gift_package"):
        reward = [row.get("type"), row.get("para"), row.get("count")]
        add_direct_offer(
            offers,
            table="gift_package",
            row=row,
            source=f"Conteudo de pacote/bau #{row.get('giftid')}",
            reward_value=reward,
            price_value=None,
            limit="",
            refresh="Conteudo interno",
            evidence="conteudo",
            note="Mostra conteudo do gift_package.lua; nao confirma loja ativa nem preco.",
        )

    return offers


def package_name(row, *keys):
    for key in keys:
        value = row.get(key)
        if value:
            translated = loc(value, "")
            if translated:
                return translated
    return ""


def duration_text(seconds):
    value = number(seconds)
    if not value:
        return ""
    if value >= 86400 and value % 86400 == 0:
        days = int(value // 86400)
        return f"{days} dia" + ("s" if days != 1 else "")
    if value >= 3600 and value % 3600 == 0:
        hours = int(value // 3600)
        return f"{hours} horas"
    return f"{format_num(value)} s"


def build_packages():
    packages = []

    def add_package(table, row, source, name="", desc="", pack_type="", gift_id=None, duration="", price_hint="", note=""):
        name = name or package_name(row, "name", "type_name")
        desc = desc or package_name(row, "slogan", "desc", "describe", "des")
        gift_id = gift_id if gift_id is not None else row.get("gift")
        # Do not include generic words such as "pacote" in the searchable blob:
        # after accent folding, a query for "Aco" would otherwise match "pacote".
        blob = " ".join(
            str(x)
            for x in [
                name,
                desc,
                gift_id,
                row.get("id"),
                row.get("recharge_id"),
                row.get("group"),
                row.get("para"),
            ]
            if x not in (None, "", [])
        )
        packages.append(
            {
                "id": str(row.get("id") or row.get("recharge_id") or ""),
                "table": table,
                "source": source,
                "name": name or f"Pacote #{row.get('id') or row.get('recharge_id')}",
                "desc": desc,
                "type": pack_type,
                "gift_id": str(gift_id or ""),
                "duration": duration,
                "discount": row.get("discount") or "",
                "price_hint": price_hint,
                "server_limit": json.dumps(row.get("server_day_limit"), ensure_ascii=False) if row.get("server_day_limit") else "",
                "base_level": row.get("base_level") or "",
                "condition": condition_text(row.get("condition")),
                "evidence": "pacote_relacionado",
                "note": note or "Pacote existe no cliente, mas conteudo completo/preco real dependem da tabela gift/recharge e do servidor.",
                "norm_blob": norm(blob),
            }
        )

    for row in load_table("recharge_gift_new"):
        add_package(
            "recharge_gift_new",
            row,
            "Pacote pago dinamico",
            desc=loc(row.get("slogan"), ""),
            pack_type="Pago/evento/rotacao",
            duration=duration_text(row.get("duration")),
        )

    for row in load_table("recharge_gift_activity"):
        add_package(
            "recharge_gift_activity",
            row,
            "Pacote de atividade",
            desc=loc(row.get("slogan"), ""),
            pack_type="Pago/evento",
        )

    for row in load_table("recharge_gift_festival"):
        add_package(
            "recharge_gift_festival",
            row,
            "Pacote festival",
            desc=loc(row.get("desc"), ""),
            pack_type="Pago/festival",
        )

    for row in load_table("recharge_gift_heroequip"):
        ptype = "Cartao semanal/equipamento" if "weekly" in str(row.get("name")) else "Pago/equipamento"
        add_package(
            "recharge_gift_heroequip",
            row,
            "Pacote equipamento Palmon",
            pack_type=ptype,
            duration="Semanal" if "weekly" in str(row.get("name")) else "",
            note="Inclui gift e, em alguns casos, daily_gift; conteudo detalhado precisa da tabela gift.",
        )

    for row in load_table("recharge_gift_precious"):
        add_package(
            "recharge_gift_precious",
            row,
            "Pacote precioso",
            pack_type="Pago/limitado",
            gift_id=row.get("gift"),
            price_hint=f"recharge_id {row.get('recharge_id')}",
        )

    for row in load_table("activity_award_dailypack"):
        ids = []
        for group_key in ("recharge_gift", "recharge_gift_new"):
            for group in as_list(row.get(group_key)):
                if isinstance(group, list):
                    ids.extend(str(item) for item in group if isinstance(item, int))
        add_package(
            "activity_award_dailypack",
            row,
            "Pacote diario",
            name=loc(row.get("name"), f"Pacote diario dia {row.get('day')}"),
            desc=loc(row.get("des"), ""),
            pack_type="Diario/pago",
            gift_id=", ".join(ids[:12]),
            duration="Diario",
            note="Tabela liga o painel diario a varios recharge/gift ids; conteudo final depende do gift id e do servidor.",
        )

    for row in load_table("subscribe_gift"):
        price = parse_price(row.get("expend_currency"), "subscribe_gift")
        add_package(
            "subscribe_gift",
            row,
            "Assinatura/beneficio",
            name=loc(row.get("name"), ""),
            desc=loc(row.get("describe"), ""),
            pack_type="Assinatura",
            price_hint=price.get("text", ""),
            note="Mostra assinatura/beneficio existente; recompensa especifica nao esta totalmente expandida aqui.",
        )

    for row in load_table("web_store"):
        reward = parse_reward(row.get("gold_doller"))
        add_package(
            "web_store",
            row,
            "Web store",
            name=row.get("sku") or row.get("product_type"),
            desc=reward["name"] + " x" + format_num(reward["qty"]) if reward else "",
            pack_type="Web store",
            gift_id=row.get("rechange_mail"),
            price_hint=f"SKU {row.get('sku')}",
            note="Oferta de web store no cliente; disponibilidade e preco dependem do servidor/loja.",
        )

    return packages


def build_item_catalog(offers, packages):
    by_key = {}
    for offer in offers:
        by_key.setdefault(
            offer["item_key"],
            {
                "key": offer["item_key"],
                "name": offer["item_name"],
                "desc": offer.get("item_desc", ""),
                "status": offer.get("item_meta_status", ""),
                "source": offer.get("item_meta_source", ""),
                "visual": offer.get("item_visual", ""),
                "visual_kind": offer.get("item_visual_kind", ""),
                "icon": offer.get("item_icon", ""),
                "icon_status": offer.get("item_icon_status", ""),
                "icon_source": offer.get("item_icon_source", ""),
                "icon_texture": offer.get("item_icon_texture", ""),
                "type": offer["item_type"],
                "norm": offer["item_norm"],
                "offer_count": 0,
            },
        )
        by_key[offer["item_key"]]["offer_count"] += 1

    for key, value in L10N.items():
        if key.startswith("item_itemname_"):
            item_id = key.rsplit("_", 1)[-1]
            if not numeric_item_id(item_id):
                continue
            item_key = f"3:{item_id}"
            meta = item_meta(item_id, kind=3)
            icon = icon_for_reward(3, item_id, meta["name"], meta["desc"], "Item")
            by_key.setdefault(
                item_key,
                {
                    "key": item_key,
                    "name": meta["name"],
                    "desc": meta["desc"],
                    "status": meta["status"],
                    "source": meta["source"],
                    "visual": meta["visual"],
                    "visual_kind": meta["visual_kind"],
                    "icon": icon["icon"],
                    "icon_status": icon["icon_status"],
                    "icon_source": icon["icon_source"],
                    "icon_texture": icon["icon_texture"],
                    "type": "Item",
                    "norm": norm(f"{meta['name']} {meta['desc']} {item_id} item"),
                    "offer_count": 0,
                },
            )
    for key, value in L10N.items():
        if key.startswith("droptype_name_") and key.count("_") == 2:
            drop_id = key.rsplit("_", 1)[-1]
            if not numeric_item_id(drop_id):
                continue
            item_key = f"10:{drop_id}"
            meta = item_meta(drop_id, kind=10, type_name="Moeda/Recurso")
            icon = icon_for_reward(10, drop_id, meta["name"], meta["desc"], "Moeda/Recurso")
            by_key.setdefault(
                item_key,
                {
                    "key": item_key,
                    "name": meta["name"],
                    "desc": meta["desc"],
                    "status": meta["status"],
                    "source": meta["source"],
                    "visual": meta["visual"],
                    "visual_kind": meta["visual_kind"],
                    "icon": icon["icon"],
                    "icon_status": icon["icon_status"],
                    "icon_source": icon["icon_source"],
                    "icon_texture": icon["icon_texture"],
                    "type": "Moeda/Recurso",
                    "norm": norm(f"{meta['name']} {meta['desc']} {drop_id} recurso moeda"),
                    "offer_count": 0,
                },
            )

    for kind, name in [(1, "Pallitas"), (6, "Ouro"), (7, "Tabuas"), (8, "Aco"), (11, "Energia")]:
        key = f"{kind}:0"
        meta = item_meta(0, kind=kind, type_name="Recurso")
        icon = icon_for_reward(kind, 0, meta.get("name") or name, meta.get("desc", ""), "Recurso")
        by_key.setdefault(
            key,
            {
                "key": key,
                "name": meta.get("name") or name,
                "desc": meta.get("desc", ""),
                "status": meta.get("status", ""),
                "source": meta.get("source", ""),
                "visual": meta.get("visual", ""),
                "visual_kind": meta.get("visual_kind", ""),
                "icon": icon["icon"],
                "icon_status": icon["icon_status"],
                "icon_source": icon["icon_source"],
                "icon_texture": icon["icon_texture"],
                "type": "Recurso",
                "norm": norm(f"{name} {meta.get('desc', '')}"),
                "offer_count": 0,
            },
        )

    items = sorted(by_key.values(), key=lambda row: (-row["offer_count"], row["name"]))
    return items


def data_payload():
    offers = build_direct_offers()
    packages = build_packages()
    items = build_item_catalog(offers, packages)

    source_counts = defaultdict(int)
    for offer in offers:
        source_counts[offer["table"]] += 1
    package_counts = defaultdict(int)
    for package in packages:
        package_counts[package["table"]] += 1
    icon_counts = defaultdict(int)
    for offer in offers:
        icon_counts[offer.get("item_icon_status") or "sem_icone"] += 1

    return {
        "generated_from": "APK client configs extraidos localmente",
        "generated_at": "2026-06-08",
        "item_icons_extracted": len(ICON_ITEMS),
        "offers": offers,
        "packages": packages,
        "items": items,
        "source_counts": dict(sorted(source_counts.items())),
        "package_counts": dict(sorted(package_counts.items())),
        "icon_counts": dict(sorted(icon_counts.items())),
        "product_tiers": load_table("recharge_product"),
        "limitations": [
            "O servidor decide quais pacotes aparecem hoje, limites reais, AB test e preco regional em BRL.",
            "A tabela gift.lua/recharge.lua grande usa dataprovider externo; nesta versao o conteudo completo de pacotes pagos e preco BRL ficam marcados como nao confirmado.",
            "Foram extraidos icones reais de assets/uiv3/texture/uiitem e uiresourceicon; quando o ID nao casa diretamente com o asset, a pagina marca o icone como provavel/inferido.",
            "A tabela item.lua aponta para item.bytes via dataprovider; sem decodificar esse binario, alguns IDs de item continuam sem ligacao visual 100% confirmada.",
            "Itens sem item_itemname/item_remarks nas localizacoes aparecem como nao confirmado em vez de receber nome inventado.",
            "Quando voce digitar um preco visto no jogo, a pagina calcula R$/unidade localmente e salva no navegador.",
            "Nao use isto para burlar compra/servidor; e uma ferramenta de planejamento e comparacao.",
        ],
    }


HTML_TEMPLATE = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Palmon Survival - Shop Analyzer</title>
<style>
:root {
  color-scheme: light;
  --ink: #172033;
  --muted: #5d687c;
  --line: #d8e0ef;
  --soft: #f3f7fc;
  --panel: #ffffff;
  --blue: #2563eb;
  --green: #138a63;
  --amber: #b45f06;
  --red: #b42318;
  --purple: #7357c9;
  --shadow: 0 10px 24px rgba(23, 32, 51, 0.08);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, Arial, sans-serif;
  color: var(--ink);
  background: #eef3f8;
  letter-spacing: 0;
}
a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; }
header {
  position: sticky;
  top: 0;
  z-index: 4;
  border-bottom: 1px solid var(--line);
  background: rgba(255,255,255,0.94);
  backdrop-filter: blur(10px);
}
.nav {
  max-width: 1480px;
  margin: 0 auto;
  padding: 14px 20px;
  display: grid;
  grid-template-columns: minmax(260px, 1fr) auto;
  gap: 16px;
  align-items: center;
}
.brand h1 { margin: 0; font-size: 20px; line-height: 1.2; }
.brand p { margin: 4px 0 0; color: var(--muted); font-size: 13px; }
.links { display: flex; gap: 8px; flex-wrap: wrap; justify-content: end; }
.links a, .mini-button {
  border: 1px solid var(--line);
  background: #fff;
  color: var(--ink);
  border-radius: 7px;
  padding: 9px 11px;
  font-weight: 700;
  font-size: 13px;
}
main {
  max-width: 1480px;
  margin: 0 auto;
  padding: 22px 20px 56px;
}
.layout {
  display: grid;
  grid-template-columns: 360px minmax(0, 1fr);
  gap: 18px;
  align-items: start;
  min-width: 0;
}
.layout > * { min-width: 0; }
.filters {
  position: sticky;
  top: 84px;
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  box-shadow: var(--shadow);
  padding: 16px;
  min-width: 0;
}
.filters h2, section h2 { margin: 0 0 12px; font-size: 18px; }
.field { margin-bottom: 13px; }
label {
  display: block;
  font-size: 12px;
  font-weight: 800;
  color: #334155;
  margin-bottom: 6px;
  text-transform: uppercase;
}
input, select {
  width: 100%;
  border: 1px solid #bdc7d8;
  background: #fff;
  color: var(--ink);
  border-radius: 7px;
  padding: 10px 11px;
  font-size: 14px;
}
input:focus, select:focus { outline: 2px solid rgba(37,99,235,0.22); border-color: var(--blue); }
.segmented {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
}
.segmented button {
  border: 1px solid var(--line);
  background: #fff;
  color: var(--ink);
  border-radius: 7px;
  padding: 9px 8px;
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.segmented button.active { background: #e8f0ff; border-color: #7da6ff; color: #1640a3; }
.hint {
  color: var(--muted);
  font-size: 13px;
  line-height: 1.45;
  margin: 8px 0 0;
}
.stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 16px;
}
.stat {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 14px;
  min-height: 92px;
}
.stat span { display: block; color: var(--muted); font-size: 12px; font-weight: 800; text-transform: uppercase; }
.stat strong { display: block; margin-top: 8px; font-size: 24px; }
.stat small { display: block; margin-top: 6px; color: var(--muted); line-height: 1.35; }
section {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 8px;
  box-shadow: var(--shadow);
  margin-bottom: 16px;
  overflow: hidden;
  min-width: 0;
}
.section-head {
  padding: 15px 16px;
  border-bottom: 1px solid var(--line);
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
}
.section-head p { margin: 3px 0 0; color: var(--muted); font-size: 13px; }
.section-body { padding: 16px; }
.best-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
  gap: 10px;
}
.best {
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 12px;
  background: #fbfdff;
}
.best b { display: block; font-size: 14px; }
.best span { display: block; color: var(--muted); margin-top: 5px; font-size: 13px; line-height: 1.4; }
.table-wrap { overflow: auto; min-width: 0; }
table {
  width: 100%;
  border-collapse: collapse;
  min-width: 1120px;
}
th, td {
  padding: 10px 12px;
  border-bottom: 1px solid #e6ebf3;
  text-align: left;
  vertical-align: top;
  font-size: 13px;
}
th {
  position: sticky;
  top: 0;
  background: #f7faff;
  color: #34405a;
  font-size: 12px;
  text-transform: uppercase;
  z-index: 1;
}
tbody tr:hover { background: #fbfdff; }
.pill {
  display: inline-flex;
  align-items: center;
  min-height: 22px;
  border-radius: 6px;
  padding: 3px 7px;
  font-size: 12px;
  font-weight: 800;
  white-space: nowrap;
}
.pill.confirmado { background: #e8f8f0; color: var(--green); }
.pill.conteudo { background: #fff4df; color: var(--amber); }
.pill.pacote { background: #f0ecff; color: var(--purple); }
.pill.warn { background: #ffebe8; color: var(--red); }
.muted { color: var(--muted); }
.mono { font-family: ui-monospace, SFMono-Regular, Consolas, monospace; font-size: 12px; }
.item-cell {
  display: grid;
  grid-template-columns: 48px minmax(0, 1fr);
  gap: 10px;
  align-items: start;
  min-width: 250px;
}
.item-thumb {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  border: 1px solid #b7c5d9;
  background: linear-gradient(145deg, #f7fbff, #dfeaff);
  display: grid;
  place-items: center;
  color: #1f3b69;
  font-weight: 900;
  font-size: 14px;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.9);
}
.item-thumb.currency { background: linear-gradient(145deg, #fff7d6, #ffd36e); color: #6d4300; }
.item-thumb.resource { background: linear-gradient(145deg, #e9fbf4, #9ee6c8); color: #07553f; }
.item-thumb.palmon { background: linear-gradient(145deg, #f0ecff, #b9a7ff); color: #38206b; }
.item-thumb.unknown { background: linear-gradient(145deg, #f8fafc, #d5dde9); color: #5b6678; }
.item-thumb.real {
  background: #fff;
  padding: 2px;
  overflow: hidden;
}
.item-thumb img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}
.item-main b { display: block; font-size: 13px; line-height: 1.25; overflow-wrap: anywhere; }
.item-desc {
  display: block;
  margin-top: 4px;
  color: var(--muted);
  line-height: 1.35;
  max-width: 420px;
}
.item-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 6px;
}
.mini {
  display: inline-flex;
  align-items: center;
  min-height: 20px;
  border-radius: 5px;
  padding: 2px 6px;
  font-size: 11px;
  font-weight: 800;
  background: #eef4fb;
  color: #42506a;
}
.mini.ok { background: #e8f8f0; color: var(--green); }
.mini.infer { background: #fff4df; color: var(--amber); }
.mini.miss { background: #ffebe8; color: var(--red); }
.brl-input { width: 92px; padding: 7px 8px; font-size: 13px; }
.package-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 10px;
}
.package {
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 13px;
  background: #fbfdff;
}
.package h3 { margin: 0; font-size: 15px; line-height: 1.3; }
.package p { margin: 7px 0 0; color: var(--muted); line-height: 1.4; font-size: 13px; }
.package dl {
  display: grid;
  grid-template-columns: 92px minmax(0, 1fr);
  gap: 5px 9px;
  margin: 11px 0 0;
  font-size: 12px;
}
.package dt { color: var(--muted); font-weight: 800; }
.package dd { margin: 0; overflow-wrap: anywhere; }
.sources {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 8px;
}
.source-row {
  border: 1px solid var(--line);
  border-radius: 7px;
  padding: 10px;
  background: #fbfdff;
  font-size: 13px;
}
.empty {
  padding: 24px;
  text-align: center;
  color: var(--muted);
  border: 1px dashed #bfccdd;
  border-radius: 8px;
  background: #fbfdff;
}
@media (max-width: 1000px) {
  .nav { grid-template-columns: 1fr; }
  .links { justify-content: start; }
  .layout { grid-template-columns: 1fr; }
  .filters { position: static; }
  .stats { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
@media (max-width: 620px) {
  main { padding: 14px 10px 40px; }
  .stats { grid-template-columns: 1fr; }
  .section-head { align-items: start; flex-direction: column; }
  .segmented { grid-template-columns: 1fr; }
}
</style>
</head>
<body>
<header>
  <div class="nav">
    <div class="brand">
      <h1>Palmon Survival - Shop Analyzer</h1>
      <p>Escolha o item que voce precisa e compare lojas, eventos e pacotes conhecidos no cliente.</p>
    </div>
    <div class="links">
      <a href="palmon_survival_pedia_completa.html">Pedia</a>
      <a href="palmon_team_builder.html">Montador</a>
      <a href="palmon_battle_simulator.html">Simulador</a>
    </div>
  </div>
</header>
<main>
  <div class="layout">
    <aside class="filters">
      <h2>Busca</h2>
      <div class="field">
        <label for="itemSearch">Item ou recurso</label>
        <input id="itemSearch" list="itemList" placeholder="Ex.: Aco, EXP de Palmon, Pallitas, acelerador" autocomplete="off">
        <datalist id="itemList"></datalist>
        <p class="hint">Pode digitar nome, ID do item ou moeda. A busca aceita texto parcial.</p>
      </div>
      <div class="field">
        <label for="sourceFilter">Fonte</label>
        <select id="sourceFilter">
          <option value="">Todas as fontes</option>
        </select>
      </div>
      <div class="field">
        <label>Tipo de evidencia</label>
        <div class="segmented" id="evidenceButtons">
          <button type="button" class="active" data-evidence="">Tudo</button>
          <button type="button" data-evidence="confirmado">Confirmado</button>
          <button type="button" data-evidence="pacote">Pacotes</button>
        </div>
      </div>
      <div class="field">
        <label for="sortMode">Ordenar ofertas confirmadas</label>
        <select id="sortMode">
          <option value="best">Melhor custo unitario conhecido</option>
          <option value="qty">Maior quantidade</option>
          <option value="source">Fonte</option>
        </select>
      </div>
      <p class="hint">Precos em BRL nao ficam confiaveis no APK: a loja/servidor pode mudar por pais, conta e evento. Use o campo R$ visto para comparar quando aparecer no jogo.</p>
    </aside>

    <div>
      <div class="stats">
        <div class="stat"><span>Ofertas confirmadas</span><strong id="statOffers">0</strong><small>linhas com item/quantidade/preco conhecidos</small></div>
        <div class="stat"><span>Pacotes relacionados</span><strong id="statPackages">0</strong><small>pacotes por nome/tema ou gift id</small></div>
        <div class="stat"><span>Melhor moeda</span><strong id="statBest">-</strong><small id="statBestDetail">Escolha um item</small></div>
        <div class="stat"><span>Catalogo</span><strong id="statCatalog">0</strong><small>itens/recursos localizados em pt_BR</small></div>
      </div>

      <section>
        <div class="section-head">
          <div>
            <h2>Melhores opcoes</h2>
            <p>Resumo por moeda. Compare apenas ofertas que usam a mesma moeda.</p>
          </div>
          <span class="pill confirmado">dados do cliente</span>
        </div>
        <div class="section-body">
          <div id="bestOptions" class="best-grid"></div>
        </div>
      </section>

      <section>
        <div class="section-head">
          <div>
            <h2>Ofertas confirmadas</h2>
            <p>Itens vendidos/trocados diretamente em lojas e eventos extraidos dos Lua configs.</p>
          </div>
          <span id="offerCountLabel" class="pill confirmado">0 resultados</span>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Item</th>
                <th>Qtd.</th>
                <th>Fonte</th>
                <th>Preco</th>
                <th>Custo un.</th>
                <th>R$ visto</th>
                <th>R$/un.</th>
                <th>Renova</th>
                <th>Limite</th>
                <th>Condicoes</th>
                <th>Fonte tecnica</th>
              </tr>
            </thead>
            <tbody id="offersBody"></tbody>
          </table>
        </div>
      </section>

      <section>
        <div class="section-head">
          <div>
            <h2>Pacotes e assinaturas relacionados</h2>
            <p>Pacotes existentes no cliente. Conteudo exato fica marcado quando a tabela interna nao esta expandida.</p>
          </div>
          <span id="packageCountLabel" class="pill pacote">0 resultados</span>
        </div>
        <div class="section-body">
          <div id="packages" class="package-list"></div>
        </div>
      </section>

      <section>
        <div class="section-head">
          <div>
            <h2>Fontes e limites</h2>
            <p>O que a ferramenta sabe e o que ainda precisa de print/tela ativa.</p>
          </div>
          <span class="pill warn">nao mexe no jogo</span>
        </div>
        <div class="section-body">
          <div id="sources" class="sources"></div>
        </div>
      </section>
    </div>
  </div>
</main>

<script id="data" type="application/json">__DATA__</script>
<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
const els = {
  itemSearch: document.getElementById('itemSearch'),
  itemList: document.getElementById('itemList'),
  sourceFilter: document.getElementById('sourceFilter'),
  evidenceButtons: document.getElementById('evidenceButtons'),
  sortMode: document.getElementById('sortMode'),
  statOffers: document.getElementById('statOffers'),
  statPackages: document.getElementById('statPackages'),
  statBest: document.getElementById('statBest'),
  statBestDetail: document.getElementById('statBestDetail'),
  statCatalog: document.getElementById('statCatalog'),
  bestOptions: document.getElementById('bestOptions'),
  offersBody: document.getElementById('offersBody'),
  packages: document.getElementById('packages'),
  offerCountLabel: document.getElementById('offerCountLabel'),
  packageCountLabel: document.getElementById('packageCountLabel'),
  sources: document.getElementById('sources')
};

let evidenceMode = '';
let prices = {};
try { prices = JSON.parse(localStorage.getItem('palmon_shop_prices') || '{}'); } catch (_) { prices = {}; }

function norm(text) {
  return String(text || '')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
}
function fmt(value) {
  if (value === null || value === undefined || value === '') return '';
  const n = Number(value);
  if (!Number.isFinite(n)) return String(value);
  return n.toLocaleString('pt-BR', { maximumFractionDigits: 2 });
}
function fmtCost(value) {
  if (value === null || value === undefined || value === '') return '';
  const n = Number(value);
  if (!Number.isFinite(n)) return String(value);
  const digits = Math.abs(n) > 0 && Math.abs(n) < 1 ? 4 : 2;
  return n.toLocaleString('pt-BR', { maximumFractionDigits: digits });
}
function money(value) {
  const n = Number(value);
  if (!Number.isFinite(n)) return '';
  return n.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}
function rowKey(row) {
  return `${row.table}:${row.id}:${row.item_key}`;
}
function hasUnitCost(row) {
  return row.unit_cost !== null && row.unit_cost !== undefined && row.unit_cost !== '' && Number.isFinite(Number(row.unit_cost));
}
function queryTokens() {
  return norm(els.itemSearch.value).split(' ').filter(Boolean);
}
function matchesText(blob, tokens) {
  if (!tokens.length) return true;
  const target = norm(blob);
  return tokens.every(token => target.includes(token));
}
function sourceOptions() {
  const sources = Array.from(new Set(DATA.offers.map(row => row.source))).sort();
  for (const source of sources) {
    const option = document.createElement('option');
    option.value = source;
    option.textContent = source;
    els.sourceFilter.appendChild(option);
  }
}
function itemOptions() {
  els.statCatalog.textContent = DATA.items.length.toLocaleString('pt-BR');
  for (const item of DATA.items.slice(0, 650)) {
    const option = document.createElement('option');
    option.value = item.name;
    const desc = item.desc ? ` - ${item.desc}` : '';
    option.label = `${item.name} (${item.type}, ${item.key})${desc}`.slice(0, 180);
    els.itemList.appendChild(option);
  }
}
function filterOffers() {
  const tokens = queryTokens();
  const source = els.sourceFilter.value;
  let rows = DATA.offers.filter(row => {
    if (source && row.source !== source) return false;
    if (evidenceMode === 'confirmado' && row.evidence !== 'confirmado') return false;
    if (evidenceMode === 'pacote' && row.evidence !== 'conteudo') return false;
    return matchesText(`${row.item_norm} ${row.item_name} ${row.item_desc} ${row.reward_param} ${row.price_name}`, tokens);
  });
  if (els.sortMode.value === 'best') {
    rows.sort((a, b) => {
      const av = hasUnitCost(a) ? Number(a.unit_cost) : Number.POSITIVE_INFINITY;
      const bv = hasUnitCost(b) ? Number(b.unit_cost) : Number.POSITIVE_INFINITY;
      if (av !== bv) return av - bv;
      return String(a.source).localeCompare(String(b.source));
    });
  } else if (els.sortMode.value === 'qty') {
    rows.sort((a, b) => Number(b.qty || 0) - Number(a.qty || 0));
  } else {
    rows.sort((a, b) => String(a.source).localeCompare(String(b.source)));
  }
  return rows;
}
function filterPackages() {
  const tokens = queryTokens();
  if (evidenceMode === 'confirmado') return [];
  return DATA.packages.filter(pkg => matchesText(`${pkg.norm_blob} ${pkg.name} ${pkg.desc} ${pkg.gift_id}`, tokens));
}
function renderBest(rows) {
  const groups = new Map();
  for (const row of rows) {
    if (!hasUnitCost(row) || !row.price_name) continue;
    const key = row.price_key || row.price_name;
    const current = groups.get(key);
    if (!current || Number(row.unit_cost) < Number(current.unit_cost)) groups.set(key, row);
  }
  const bestRows = Array.from(groups.values()).slice(0, 8);
  els.bestOptions.innerHTML = '';
  if (!bestRows.length) {
    els.bestOptions.innerHTML = '<div class="empty">Sem custo unitario conhecido para este filtro. Use um item vendido diretamente ou preencha preco visto em R$ na tabela.</div>';
    els.statBest.textContent = '-';
    els.statBestDetail.textContent = 'Sem comparacao direta';
    return;
  }
  els.statBest.textContent = bestRows[0].price_name;
  els.statBestDetail.textContent = `${fmtCost(bestRows[0].unit_cost)} ${bestRows[0].price_name} por unidade`;
  for (const row of bestRows) {
    const div = document.createElement('div');
    div.className = 'best';
    div.innerHTML = `<b>${escapeHtml(row.source)}</b><span>${escapeHtml(row.qty_text)} ${escapeHtml(row.item_name)} por ${escapeHtml(row.price_text)}<br>Custo: ${escapeHtml(row.unit_cost_text)} ${escapeHtml(row.price_name)} / un.</span>`;
    els.bestOptions.appendChild(div);
  }
}
function escapeHtml(text) {
  return String(text ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}
function statusInfo(status) {
  if (status === 'oficial_pt_BR' || status === 'padrao_cliente') return {label: status === 'oficial_pt_BR' ? 'nome oficial' : 'tipo cliente', cls: 'ok'};
  if (status === 'inferido_config') return {label: 'inferido', cls: 'infer'};
  if (String(status || '').startsWith('fallback_')) return {label: String(status).replace('fallback_', 'fallback '), cls: 'infer'};
  return {label: 'nao confirmado', cls: 'miss'};
}
function iconStatusInfo(status) {
  if (status === 'icone_id_direto' || status === 'icone_tipo_cliente') return {label: 'icone real', cls: 'ok'};
  if (status === 'icone_chip_inferido') return {label: 'chip inferido', cls: 'infer'};
  if (status === 'icone_heuristico') return {label: 'icone provavel', cls: 'infer'};
  return {label: 'sem icone', cls: 'miss'};
}
function itemCell(row) {
  const status = statusInfo(row.item_meta_status);
  const iconStatus = iconStatusInfo(row.item_icon_status);
  const desc = row.item_desc || 'Descricao nao confirmada nas localizacoes extraidas.';
  const source = row.item_meta_source || row.item_key;
  const visual = row.item_visual || '?';
  const visualKind = row.item_visual_kind || 'unknown';
  const iconTitle = row.item_icon_source || 'Icone nao confirmado';
  const thumb = row.item_icon
    ? `<div class="item-thumb real" title="${escapeHtml(iconTitle)}"><img src="${escapeHtml(row.item_icon)}" alt=""></div>`
    : `<div class="item-thumb ${escapeHtml(visualKind)}" title="Icone real nao ligado com seguranca ao ID; marcador visual por categoria">${escapeHtml(visual)}</div>`;
  return `
    <div class="item-cell">
      ${thumb}
      <div class="item-main">
        <b>${escapeHtml(row.item_name)}</b>
        <span class="item-desc">${escapeHtml(desc)}</span>
        <div class="item-meta">
          <span class="mini ${status.cls}">${escapeHtml(status.label)}</span>
          <span class="mini ${iconStatus.cls}" title="${escapeHtml(iconTitle)}">${escapeHtml(iconStatus.label)}</span>
          <span class="muted mono">${escapeHtml(row.item_key)}</span>
          <span class="muted mono">${escapeHtml(source)}</span>
        </div>
      </div>
    </div>
  `;
}
function renderOffers(rows) {
  els.statOffers.textContent = rows.length.toLocaleString('pt-BR');
  els.offerCountLabel.textContent = `${rows.length.toLocaleString('pt-BR')} resultados`;
  els.offersBody.innerHTML = '';
  if (!rows.length) {
    els.offersBody.innerHTML = '<tr><td colspan="11"><div class="empty">Nenhuma oferta confirmada para este filtro.</div></td></tr>';
    return;
  }
  for (const row of rows.slice(0, 300)) {
    const key = rowKey(row);
    const brl = prices[key] || '';
    const brlUnit = brl && Number(row.qty) ? money(Number(brl) / Number(row.qty)) : '';
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${itemCell(row)}</td>
      <td>${escapeHtml(row.qty_text)}</td>
      <td>${escapeHtml(row.source)}<br><span class="pill ${row.evidence === 'conteudo' ? 'conteudo' : 'confirmado'}">${row.evidence === 'conteudo' ? 'conteudo' : 'confirmado'}</span></td>
      <td>${escapeHtml(row.price_text)}</td>
      <td>${row.unit_cost_text ? `${escapeHtml(row.unit_cost_text)} <span class="muted">${escapeHtml(row.price_name)}</span>` : '<span class="muted">-</span>'}</td>
      <td><input class="brl-input" inputmode="decimal" data-price-key="${escapeHtml(key)}" data-qty="${escapeHtml(row.qty)}" value="${escapeHtml(brl)}" placeholder="R$"></td>
      <td class="brl-unit">${escapeHtml(brlUnit)}</td>
      <td>${escapeHtml(row.refresh || '-')}</td>
      <td>${escapeHtml(row.limit || '-')}</td>
      <td>${escapeHtml(row.conditions || row.note || '-')}</td>
      <td><span class="mono">${escapeHtml(row.table)}:${escapeHtml(row.id)}</span><br><span class="muted">${escapeHtml(row.source_note || '')}</span></td>
    `;
    els.offersBody.appendChild(tr);
  }
  for (const input of els.offersBody.querySelectorAll('.brl-input')) {
    input.addEventListener('input', event => {
      const target = event.currentTarget;
      const key = target.dataset.priceKey;
      const raw = target.value.replace(',', '.');
      if (raw) prices[key] = raw; else delete prices[key];
      localStorage.setItem('palmon_shop_prices', JSON.stringify(prices));
      const qty = Number(target.dataset.qty);
      const value = Number(raw);
      const cell = target.closest('tr').querySelector('.brl-unit');
      cell.textContent = Number.isFinite(value) && qty ? money(value / qty) : '';
    });
  }
}
function renderPackages(rows) {
  els.statPackages.textContent = rows.length.toLocaleString('pt-BR');
  els.packageCountLabel.textContent = `${rows.length.toLocaleString('pt-BR')} resultados`;
  els.packages.innerHTML = '';
  if (!rows.length) {
    els.packages.innerHTML = '<div class="empty">Nenhum pacote relacionado por nome/tema para este filtro.</div>';
    return;
  }
  for (const pkg of rows.slice(0, 160)) {
    const div = document.createElement('div');
    div.className = 'package';
    div.innerHTML = `
      <h3>${escapeHtml(pkg.name)}</h3>
      <p>${escapeHtml(pkg.desc || pkg.note)}</p>
      <dl>
        <dt>Tipo</dt><dd>${escapeHtml(pkg.type || '-')}</dd>
        <dt>Fonte</dt><dd>${escapeHtml(pkg.source)}</dd>
        <dt>ID</dt><dd class="mono">${escapeHtml(pkg.table)}:${escapeHtml(pkg.id)}</dd>
        <dt>Gift</dt><dd class="mono">${escapeHtml(pkg.gift_id || 'nao expandido')}</dd>
        <dt>Duracao</dt><dd>${escapeHtml(pkg.duration || '-')}</dd>
        <dt>Base</dt><dd>${escapeHtml(pkg.base_level || '-')}</dd>
        <dt>Preco</dt><dd>${escapeHtml(pkg.price_hint || 'preco BRL nao confirmado')}</dd>
      </dl>
      <p><span class="pill pacote">pacote no cliente</span></p>
    `;
    els.packages.appendChild(div);
  }
}
function renderSources() {
  const rows = [];
  for (const [key, count] of Object.entries(DATA.source_counts)) rows.push([key, count, 'ofertas']);
  for (const [key, count] of Object.entries(DATA.package_counts)) rows.push([key, count, 'pacotes']);
  rows.push(['icones_extraidos', DATA.item_icons_extracted || 0, 'assets PNG']);
  for (const [key, count] of Object.entries(DATA.icon_counts || {})) rows.push([key, count, 'ofertas']);
  els.sources.innerHTML = rows.map(([key, count, kind]) => `<div class="source-row"><b class="mono">${escapeHtml(key)}</b><br><span class="muted">${fmt(count)} ${kind}</span></div>`).join('');
  for (const limit of DATA.limitations) {
    const div = document.createElement('div');
    div.className = 'source-row';
    div.innerHTML = `<b>Limite</b><br><span class="muted">${escapeHtml(limit)}</span>`;
    els.sources.appendChild(div);
  }
}
function render() {
  const offers = filterOffers();
  const packages = filterPackages();
  renderBest(offers);
  renderOffers(offers);
  renderPackages(packages);
}
els.itemSearch.addEventListener('input', render);
els.sourceFilter.addEventListener('change', render);
els.sortMode.addEventListener('change', render);
els.evidenceButtons.addEventListener('click', event => {
  const button = event.target.closest('button');
  if (!button) return;
  evidenceMode = button.dataset.evidence;
  for (const btn of els.evidenceButtons.querySelectorAll('button')) btn.classList.toggle('active', btn === button);
  render();
});
sourceOptions();
itemOptions();
renderSources();
render();
</script>
</body>
</html>
"""


def main():
    PEDIA_DIR.mkdir(parents=True, exist_ok=True)
    data = data_payload()
    html_text = HTML_TEMPLATE.replace(
        "__DATA__",
        json.dumps(data, ensure_ascii=False).replace("</", "<\\/"),
    )
    OUT_HTML.write_text(html_text, encoding="utf-8")
    print(
        f"Shop Analyzer: {OUT_HTML} | offers={len(data['offers'])} | packages={len(data['packages'])} | items={len(data['items'])}"
    )


if __name__ == "__main__":
    main()

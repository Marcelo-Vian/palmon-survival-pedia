import pathlib
import re
from typing import Dict, Tuple

from PIL import Image, ImageOps


ROOT = pathlib.Path(r"D:\Linkedin")
PRINTS_DIR = ROOT / "palmon_survival_prints" / "loja" / "prints"
OUT_DIR = ROOT / "palmon_survival_pedia" / "assets" / "shop_offer_thumbs"
OUT_SIZE = (420, 165)

Box = Tuple[int, int, int, int]
ThumbMap = Dict[str, Tuple[int, Box]]


def cap_index() -> Dict[int, pathlib.Path]:
    files: Dict[int, pathlib.Path] = {}
    for path in PRINTS_DIR.glob("*.png"):
        match = re.search(r"_cap(\d+)_", path.name)
        if match:
            files[int(match.group(1))] = path
    return files


THUMBS: ThumbMap = {
    "finguenue_small_490": (2, (25, 825, 860, 1024)),
    "finguenue_medium_1090": (2, (25, 1030, 860, 1222)),
    "finguenue_large_2290": (2, (25, 1232, 860, 1424)),
    "daily_value_palcatcher": (3, (20, 668, 880, 885)),
    "daily_mount_upgrade": (3, (25, 1135, 880, 1340)),
    "daily_lumber_bundle": (4, (25, 1238, 880, 1445)),
    "daily_electricity_bundle": (5, (25, 1238, 880, 1445)),
    "weekly_camp_upgrade": (9, (25, 384, 884, 730)),
    "weekly_power_evolution": (9, (25, 1090, 884, 1440)),
    "weekly_one_big_happy_family": (13, (25, 384, 884, 725)),
    "weekly_blessings_palantis": (13, (25, 1090, 884, 1435)),
    "choice_monthly_pass": (19, (35, 238, 870, 870)),
    "weekly_pass_animated_emoji": (19, (35, 898, 870, 1535)),
    "weekly_camp_supply": (23, (25, 220, 875, 552)),
    "supply_7d_pallite": (23, (36, 612, 865, 868)),
    "supply_7d_palmon_egg": (24, (36, 588, 865, 840)),
    "supply_7d_temperite": (23, (36, 1190, 865, 1444)),
    "supply_7d_speedup": (24, (36, 1165, 865, 1428)),
    "bundle_rapid_development": (27, (32, 228, 866, 580)),
    "bundle_triumph_badges": (27, (32, 612, 866, 958)),
    "bundle_equipment": (27, (32, 994, 866, 1346)),
    "bundle_pearl_power": (34, (32, 500, 866, 850)),
    "bundle_energy_prime": (35, (32, 410, 866, 760)),
    "bundle_mount": (35, (32, 1180, 866, 1440)),
    "bundle_skillfruits": (36, (32, 480, 866, 832)),
    "bundle_research_speedup": (36, (32, 875, 866, 1223)),
    "bundle_palcatcher_world": (38, (32, 300, 866, 650)),
    "bundle_elite_trainer": (38, (32, 692, 866, 1030)),
    "bundle_assistant": (38, (32, 1070, 866, 1425)),
    "growth_fund_ii": (40, (26, 232, 872, 450)),
    "pallite_100_490": (45, (36, 474, 440, 678)),
    "pallite_1040_2790": (45, (468, 474, 870, 678)),
    "pallite_2100_5490": (44, (36, 863, 440, 1198)),
    "pallite_4300_10999": (45, (468, 710, 870, 1034)),
    "pallite_11000_27990": (45, (36, 1078, 440, 1412)),
    "pallite_24000_54990": (45, (468, 1078, 870, 1412)),
    "event_carnival_wheel": (48, (0, 235, 900, 600)),
    "palmon_mammolith_arrival": (53, (35, 1325, 350, 1510)),
    "palmon_meet_gnashley": (57, (35, 1325, 350, 1510)),
    "event_froggy_gaiden": (83, (42, 245, 858, 1295)),
    "custom_weekly_pass_pending": (86, (0, 215, 900, 670)),
    "event_mariners_hoard": (93, (0, 235, 900, 600)),
}


def make_thumb(source: pathlib.Path, box: Box, target: pathlib.Path) -> None:
    image = Image.open(source).convert("RGB")
    crop = image.crop(box)
    resized = ImageOps.contain(crop, OUT_SIZE, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", OUT_SIZE, "#eaf4ff")
    x = (OUT_SIZE[0] - resized.width) // 2
    y = (OUT_SIZE[1] - resized.height) // 2
    canvas.paste(resized, (x, y))
    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(target, quality=82, optimize=True)


def main() -> None:
    caps = cap_index()
    missing = []
    for offer_id, (cap_no, box) in THUMBS.items():
        source = caps.get(cap_no)
        if source is None:
            missing.append(f"{offer_id}: cap{cap_no}")
            continue
        make_thumb(source, box, OUT_DIR / f"{offer_id}.jpg")
    print(f"Generated {len(THUMBS) - len(missing)} thumbnails in {OUT_DIR}")
    if missing:
        print("Missing:")
        for item in missing:
            print(f"- {item}")


if __name__ == "__main__":
    main()

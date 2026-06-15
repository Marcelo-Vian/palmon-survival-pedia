import json
import pathlib
import re
import sys

import UnityPy
from UnityPy.helpers.UnityVersion import UnityVersion


ROOT = pathlib.Path(r"D:\Linkedin")
APK_ROOT = ROOT / "palmon_survival_apk"
ASSET_ROOT = APK_ROOT / "asset_apk_extracted" / "assets"
SOURCE_DIRS = [
    ASSET_ROOT / "uiv3" / "texture" / "uiitem",
    ASSET_ROOT / "uiv3" / "texture" / "uiresourceicon",
]
RESOURCES_LUA = APK_ROOT / "analysis" / "lua_decrypted_config_root" / "Resources.lua"
OUT_DIR = ROOT / "palmon_survival_pedia" / "assets" / "item_icons"
MANIFEST = OUT_DIR / "item_icon_manifest.json"


_unity_from_str = UnityVersion.from_str.__func__


def _patched_unity_version(cls, version):
    if isinstance(version, str):
        version = version.strip().split()[0]
    return _unity_from_str(cls, version)


UnityVersion.from_str = classmethod(_patched_unity_version)


def parse_resources():
    text = RESOURCES_LUA.read_text(encoding="utf-8", errors="replace")
    pattern = re.compile(r'\[\s*(-?\d+)\s*\]\s*=\s*\{\s*-?\d+\s*,\s*"([^"]+)"\s*,?\s*\}')
    resources = []
    for resource_id, path in pattern.findall(text):
        norm = path.lower()
        if norm.startswith("uiv3/texture/uiitem/") or norm.startswith("uiv3/texture/uiresourceicon/"):
            resources.append({"resource_id": resource_id, "asset_path": path})
    return resources


def safe_name(path, resource_id):
    base = pathlib.PurePosixPath(path).name
    base = re.sub(r"[^A-Za-z0-9_.-]+", "_", base).strip("_") or f"resource_{resource_id}"
    return f"{base}__{resource_id}.png"


def trim_unityfs(raw):
    idx = raw.find(b"UnityFS")
    if idx > 0:
        return raw[idx:]
    return raw


def clean_bundle_path(path):
    if not path:
        return ""
    path = str(path).replace("\\", "/").strip()
    path = re.sub(r"\.ua$", "", path, flags=re.I)
    path = re.sub(r"\.png$", "", path, flags=re.I)
    path = path.removeprefix("assets/works/resources/")
    return path


def bundle_info(env):
    info = {"bundle_name": "", "container": ""}
    for obj in env.objects:
        if obj.type.name != "AssetBundle":
            continue
        tree = obj.read_typetree()
        info["bundle_name"] = clean_bundle_path(tree.get("m_AssetBundleName") or tree.get("m_Name") or "")
        container = tree.get("m_Container") or []
        if container and isinstance(container[0], list) and container[0]:
            info["container"] = clean_bundle_path(container[0][0])
        break
    return info


def texture_entries(env):
    for obj in env.objects:
        if obj.type.name != "Texture2D":
            continue
        tree = obj.read_typetree()
        data = obj.read()
        image = data.image
        if image is None:
            continue
        yield {
            "texture_name": tree.get("m_Name") or getattr(data, "name", "") or "",
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "image": image,
        }


def extract_bundle(bundle_path):
    raw = trim_unityfs(bundle_path.read_bytes())
    env = UnityPy.load(raw)
    info = bundle_info(env)
    textures = list(texture_entries(env))
    return info, textures


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []
    failed = []
    resources_by_path = {row["asset_path"].lower(): row for row in parse_resources()}

    bundle_files = []
    for source_dir in SOURCE_DIRS:
        bundle_files.extend(sorted(source_dir.glob("*.ua")))

    for bundle_path in bundle_files:
        try:
            info, textures = extract_bundle(bundle_path)
        except Exception as exc:
            failed.append({"source_bundle": str(bundle_path), "error": f"{type(exc).__name__}: {exc}"})
            continue
        if not textures:
            failed.append({"source_bundle": str(bundle_path), "error": "Texture2D nao encontrada"})
            continue
        logical = info.get("bundle_name") or info.get("container") or bundle_path.stem
        config_resource = resources_by_path.get(logical.lower()) or resources_by_path.get(info.get("container", "").lower())
        for idx, texture in enumerate(textures, start=1):
            texture_name = texture["texture_name"] or pathlib.PurePosixPath(logical).name or bundle_path.stem
            png_name = safe_name(texture_name, bundle_path.stem if len(textures) == 1 else f"{bundle_path.stem}_{idx}")
            out_path = OUT_DIR / png_name
            texture["image"].save(out_path)
            manifest.append(
                {
                    "asset_path": logical,
                    "container": info.get("container", ""),
                    "texture_name": texture_name,
                    "resource_id": config_resource.get("resource_id", "") if config_resource else "",
                    "bundle_hash": bundle_path.stem,
                    "source_bundle": str(bundle_path),
                    "png": str(out_path),
                    "png_rel": f"assets/item_icons/{png_name}",
                    "width": texture["width"],
                    "height": texture["height"],
                    "mode": texture["mode"],
                }
            )

    MANIFEST.write_text(
        json.dumps(
            {
                "generated_from": "assetLibrary.apk / assets/uiv3/texture/uiitem + uiresourceicon",
                "bundle_files": len(bundle_files),
                "resources_total": len(resources_by_path),
                "extracted": len(manifest),
                "failed": len(failed),
                "items": manifest,
                "failed_items": failed[:100],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Extracted {len(manifest)} icons -> {OUT_DIR}")
    print(f"Bundles {len(bundle_files)} | failed {len(failed)}")
    if failed:
        print(json.dumps(failed[:5], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.exit(main())

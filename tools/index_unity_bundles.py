#!/usr/bin/env python3
"""Index Unity bundles shipped with Palmon Survival split APKs.

The game prefixes its UnityFS bundles with a small custom header. This utility
finds the UnityFS signature, reads bundle metadata with UnityPy, and writes a
searchable JSONL index without exporting copyrighted bulk assets.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import UnityPy


def bundle_record(path: Path, root: Path) -> dict:
    raw = path.read_bytes()
    offset = raw.find(b"UnityFS")
    if offset < 0:
        raise ValueError("UnityFS signature not found")

    env = UnityPy.load(raw[offset:])
    names: list[dict[str, str]] = []
    counts: Counter[str] = Counter()
    bundle_name = ""

    for obj in env.objects:
        type_name = obj.type.name
        counts[type_name] += 1
        if type_name not in {
            "AssetBundle",
            "TextAsset",
            "Texture2D",
            "Sprite",
            "SpriteAtlas",
            "GameObject",
            "MonoBehaviour",
        }:
            continue
        try:
            data = obj.read()
            name = getattr(data, "m_Name", "") or ""
        except Exception:
            name = ""
        if type_name == "AssetBundle" and name:
            bundle_name = name
        if name:
            names.append({"type": type_name, "name": name})

    return {
        "file": path.relative_to(root).as_posix(),
        "size": path.stat().st_size,
        "prefix_bytes": offset,
        "bundle": bundle_name,
        "containers": sorted(env.container.keys()),
        "types": dict(sorted(counts.items())),
        "objects": names,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path, help="Root directory containing .ua bundles")
    parser.add_argument("output", type=Path, help="Destination JSONL index")
    parser.add_argument("--scope", default="", help="Optional subdirectory, e.g. luabyte or uiv3")
    args = parser.parse_args()

    root = args.root.resolve()
    scan_root = (root / args.scope).resolve() if args.scope else root
    files = sorted(scan_root.rglob("*.ua"))
    args.output.parent.mkdir(parents=True, exist_ok=True)

    indexed = 0
    failed = 0
    with args.output.open("w", encoding="utf-8") as handle:
        for number, path in enumerate(files, 1):
            try:
                record = bundle_record(path, root)
            except Exception as exc:
                record = {
                    "file": path.relative_to(root).as_posix(),
                    "size": path.stat().st_size,
                    "error": f"{type(exc).__name__}: {exc}",
                }
                failed += 1
            else:
                indexed += 1
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            if number % 500 == 0:
                print(f"processed {number}/{len(files)}")

    print(f"indexed={indexed} failed={failed} output={args.output}")
    return 0 if indexed else 1


if __name__ == "__main__":
    raise SystemExit(main())

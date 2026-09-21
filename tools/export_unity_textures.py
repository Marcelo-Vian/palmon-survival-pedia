#!/usr/bin/env python3
"""Export selected Texture2D assets from Palmon's prefixed UnityFS bundles."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import UnityPy


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("index", type=Path)
    parser.add_argument("bundle_root", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--contains", action="append", required=True)
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    selected: list[dict] = []
    for line in args.index.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        haystack = " ".join([record.get("bundle", ""), *record.get("containers", [])]).lower()
        if any(term.lower() in haystack for term in args.contains):
            selected.append(record)

    exported = 0
    for record in selected:
        raw = (args.bundle_root / record["file"]).read_bytes()
        offset = raw.find(b"UnityFS")
        if offset < 0:
            continue
        env = UnityPy.load(raw[offset:])
        for obj in env.objects:
            if obj.type.name != "Texture2D":
                continue
            data = obj.read()
            name = getattr(data, "m_Name", "texture") or "texture"
            safe_name = "".join(char if char.isalnum() or char in "_-" else "_" for char in name)
            destination = args.output / f"{safe_name}.png"
            data.image.save(destination)
            exported += 1
            print(destination)
    print(f"exported={exported}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

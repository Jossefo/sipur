#!/usr/bin/env python3
"""Generate data/templates.json with 270 story templates."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from story_catalog import build_all_templates, required_keys_ok  # noqa: E402


def main() -> None:
    templates = build_all_templates()
    bad = [t["id"] for t in templates if not required_keys_ok(t)]
    if bad:
        raise SystemExit(f"invalid templates: {bad[:5]}")
    out = ROOT / "data" / "templates.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(templates, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(templates)} templates -> {out}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Apply the PortaCraft rebrand to a modrinth/code checkout (build-time only).

Run from the repository root:  python apply_rebrand.py

What it changes:
  1. apps/app/tauri.conf.json
     productName / mainBinaryName: "Modrinth App" -> "PortaCraft"
     identifier: "ModrinthApp" -> "com.portacraft.app"
     window title: "Modrinth App" -> "PortaCraft"
     (mainBinaryName changes the built exe to PortaCraft.exe)
  2. apps/app-frontend/index.html
     <title>Modrinth App</title> -> <title>PortaCraft</title>
  3. apps/app/icons/
     Overwrites 128x128.png, 128x128@2x.png, icon.ico, icon.icns with the
     PortaCraft artwork from rebrand-icons/ (committed at the repo root).

The script fails loudly (non-zero exit) if an anchor is not found exactly
once, so a CI build never silently ships an unbranded binary.
"""

import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent

TAURI_CONF = ROOT / "apps/app/tauri.conf.json"
INDEX_HTML = ROOT / "apps/app-frontend/index.html"
ICON_SRC_DIR = ROOT / "rebrand-icons"
ICON_DST_DIR = ROOT / "apps/app/icons"

ICON_FILES = ("128x128.png", "128x128@2x.png", "icon.ico", "icon.icns")

# (file, old, new) — each `old` must occur exactly once.
REPLACEMENTS = (
    (TAURI_CONF, '"productName": "Modrinth App"', '"productName": "PortaCraft"'),
    (TAURI_CONF, '"mainBinaryName": "Modrinth App"', '"mainBinaryName": "PortaCraft"'),
    (TAURI_CONF, '"identifier": "ModrinthApp"', '"identifier": "com.portacraft.app"'),
    (TAURI_CONF, '"title": "Modrinth App"', '"title": "PortaCraft"'),
    (INDEX_HTML, "<title>Modrinth App</title>", "<title>PortaCraft</title>"),
)


def replace_once(path: pathlib.Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        print(f"already applied, skipping: {path} [{new.strip()}]")
        return
    count = text.count(old)
    if count != 1:
        sys.exit(f"ERROR: anchor found {count} times (expected 1) in {path}: {old}")
    path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"patched: {path} [{old.strip()} -> {new.strip()}]")


def main() -> None:
    for p in (TAURI_CONF, INDEX_HTML, ICON_DST_DIR):
        if not p.exists():
            sys.exit(f"ERROR: not found: {p} (run this script from the repo root)")

    for path, old, new in REPLACEMENTS:
        replace_once(path, old, new)

    for name in ICON_FILES:
        src = ICON_SRC_DIR / name
        if not src.is_file():
            sys.exit(f"ERROR: missing rebrand icon: {src} (commit rebrand-icons/ to the repo root)")
    for name in ICON_FILES:
        shutil.copy2(ICON_SRC_DIR / name, ICON_DST_DIR / name)
        print(f"icon replaced: apps/app/icons/{name}")

    # Sanity check.
    conf = TAURI_CONF.read_text(encoding="utf-8")
    assert '"productName": "PortaCraft"' in conf, "productName rebrand did not stick"
    assert '"mainBinaryName": "PortaCraft"' in conf, "mainBinaryName rebrand did not stick"
    assert '"identifier": "com.portacraft.app"' in conf, "identifier rebrand did not stick"
    assert '"title": "PortaCraft"' in conf, "window title rebrand did not stick"
    print("PortaCraft rebrand applied successfully.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Genere photos.json : une entree par soiree datee trouvee dans photos/."""

import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
PHOTOS = ROOT / "photos"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif", ".svg"}
SCREENS = "ecrans.html"
DATED = re.compile(r"^(\d{4})-(\d{2})-(\d{2})[\s_-]*(.*)$")


def web_path(path):
    return quote(path.relative_to(ROOT).as_posix(), safe="/")


def images_in(directory):
    files = (p for p in directory.iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONS)
    return [web_path(p) for p in sorted(files, key=lambda p: p.name.lower())]


def parse(directory):
    match = DATED.match(directory.name)
    if not match:
        return None
    year, month, day, label = match.groups()
    try:
        day_date = date(int(year), int(month), int(day))
    except ValueError:
        return None

    images = images_in(directory)
    screens = directory / SCREENS

    title = label.replace("_", " ").replace("-", " ").strip()
    evening = {
        "date": day_date.isoformat(),
        "title": title.capitalize() if title else "",
        "poster": images[0] if images else "",
        "detail": images[1:],
    }
    if screens.is_file():
        evening["screens"] = web_path(screens)
    return evening


def build():
    PHOTOS.mkdir(exist_ok=True)
    evenings, ignored = [], []
    for directory in sorted(p for p in PHOTOS.iterdir() if p.is_dir()):
        evening = parse(directory)
        if evening:
            evenings.append(evening)
        else:
            ignored.append(directory.name)

    evenings.sort(key=lambda e: e["date"])
    (ROOT / "photos.json").write_text(
        json.dumps({"evenings": evenings}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return evenings, ignored


if __name__ == "__main__":
    evenings, ignored = build()
    for evening in evenings:
        if "screens" in evening:
            kind = "ecrans html"
        elif evening["poster"]:
            kind = f"affiche + {len(evening['detail'])} au detail"
        else:
            kind = "a definir"
        print(f"  {evening['date']}  {evening['title'] or '(sans titre)':<24} {kind}")
    print(f"photos.json : {len(evenings)} soiree(s)")

    stray = [p.name for p in PHOTOS.iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONS]
    for name in ignored + stray:
        print(f"  ignore : {name} (attendu : un dossier AAAA-MM-JJ_titre)", file=sys.stderr)

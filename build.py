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
DATED = re.compile(r"^(\d{4})-(\d{2})-(\d{2})[\s_-]*(.*)$")


def images_in(directory):
    files = (p for p in directory.iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONS)
    return [
        quote(p.relative_to(ROOT).as_posix(), safe="/")
        for p in sorted(files, key=lambda p: p.name.lower())
    ]


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
    if not images:
        return None
    return {
        "date": day_date.isoformat(),
        "title": title.capitalize() if (title := label.replace("_", " ").replace("-", " ").strip()) else "",
        "poster": images[0],
        "detail": images[1:],
    }


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
        label = evening["title"] or "(sans titre)"
        print(f"  {evening['date']}  {label:<24} affiche + {len(evening['detail'])} au detail")
    print(f"photos.json : {len(evenings)} soiree(s)")

    stray = [p.name for p in PHOTOS.iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONS]
    for name in ignored + stray:
        print(f"  ignore : {name} (attendu : un dossier AAAA-MM-JJ_titre)", file=sys.stderr)

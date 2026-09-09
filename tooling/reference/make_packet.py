#!/usr/bin/env python3
"""Składa dla każdego filmu jeden pakiet roboczy dla zewnętrznego czatu.

Pakiet (`packet.md`) zawiera metryczkę z linkiem do YouTube, prompt, indeks klatek
i transkrypcję. Praca wygląda tak: wklejasz `packet.md`, dorzucasz pliki z `sheets/`
(a gdy czat je przyjmuje, także wideo), dostajesz YAML i zapisujesz go obok jako
`observations.yaml`. Scalaniem zajmuje się później merge_observations.py.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from common import hhmmss, reference_root, video_dirs

TEMPLATE = Path(__file__).resolve().parent / "prompt_template.md"
CUE = re.compile(r"^(\d\d):(\d\d):(\d\d)\.\d+\s+-->")
SKIP_PREFIX = ("WEBVTT", "Kind:", "Language:", "NOTE")


def parse_vtt(text: str) -> list[tuple[int, str]]:
    """Napisy jako pary (sekunda, linia). Napisy automatyczne powtarzają wers przy
    każdym przewinięciu, więc kolejne duplikaty lecą do kosza."""
    out: list[tuple[int, str]] = []
    stamp: int | None = None
    for line in text.splitlines():
        cue = CUE.match(line.strip())
        if cue:
            h, m, s = (int(g) for g in cue.groups())
            stamp = h * 3600 + m * 60 + s
            continue
        if stamp is None or line.startswith(SKIP_PREFIX):
            continue
        clean = re.sub(r"<[^>]+>", "", line).strip()
        if not clean or (out and out[-1][1] == clean):
            continue
        out.append((stamp, clean))
    return out


def transcript(vdir: Path) -> str:
    vtts = sorted(vdir.glob("*.vtt"))
    if not vtts:
        return "_brak napisów w katalogu filmu_"
    cues = parse_vtt(vtts[0].read_text(encoding="utf-8", errors="replace"))
    return "\n".join(f"[{hhmmss(t)}] {line}" for t, line in cues)


def frame_index(index: dict) -> str:
    per_sheet = index["cols"] * index["rows"]
    frames = index["frames"]
    lines = [
        f"Siatki po {index['cols']}x{index['rows']} klatek, czytane wierszami od lewego "
        f"górnego rogu. Klatki wybrane metodą: {index['source']}.",
        "",
    ]
    for sheet_no, sheet in enumerate(index["sheets"]):
        chunk = frames[sheet_no * per_sheet : (sheet_no + 1) * per_sheet]
        if not chunk:
            break
        marks = ", ".join(f"{pos}. {f['label']}" for pos, f in enumerate(chunk, start=1))
        lines.append(f"- `{sheet}` — klatki {chunk[0]['n']}–{chunk[-1]['n']}: {marks}")
    return "\n".join(lines)


def packet(vdir: Path) -> str | None:
    info_files = sorted(vdir.glob("*.info.json"))
    index_path = vdir / "frames" / "index.json"
    if not info_files or not index_path.exists():
        return None
    info = json.loads(info_files[0].read_text(encoding="utf-8", errors="replace"))
    index = json.loads(index_path.read_text(encoding="utf-8"))

    return "\n".join(
        [
            f"# {info.get('title', vdir.name)}",
            "",
            "## Metryczka",
            "",
            f"- identyfikator: `{info.get('id', vdir.name)}`",
            f"- YouTube: {info.get('webpage_url', 'brak')}",
            f"- czas trwania: {hhmmss(info.get('duration') or 0)}",
            f"- seria: {info.get('playlist_title') or vdir.parent.name}",
            "",
            "## Instrukcja",
            "",
            TEMPLATE.read_text(encoding="utf-8").strip(),
            "",
            "## Indeks klatek",
            "",
            frame_index(index),
            "",
            "## Transkrypcja",
            "",
            transcript(vdir),
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="katalog roboczy poza repozytorium")
    parser.add_argument("--force", action="store_true", help="nadpisz gotowe pakiety")
    args = parser.parse_args()

    root = reference_root(args.root)
    written = 0
    for vdir in video_dirs(root):
        target = vdir / "packet.md"
        if target.exists() and not args.force:
            continue
        text = packet(vdir)
        if text is None:
            print(f"pominięte (brak klatek albo metadanych): {vdir}")
            continue
        target.write_text(text, encoding="utf-8")
        written += 1
    print(f"pakietów zapisanych: {written}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Pobiera filmy referencyjne i napisy z playlist wypisanych w 3b1b-playlists.txt.

Układ katalogu roboczego:

    <root>/<tytul-playlisty>/<NNN-id>/<id>.mp4
                                     /<id>.info.json
                                     /<id>.en.vtt

Ponowne uruchomienie jest tanie: yt-dlp trzyma archiwum pobrań i pomija to,
co już jest na dysku.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from common import REPO_ROOT, reference_root, run

OUTPUT_TEMPLATE = "%(playlist_title)s/%(playlist_index)03d-%(id)s/%(id)s.%(ext)s"


def playlists(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [ln.strip() for ln in lines if ln.strip() and not ln.startswith("#")]


def fetch(url: str, root: Path, height: int, subs_only: bool) -> None:
    cmd: list[str | Path] = [
        "yt-dlp",
        "--paths",
        f"home:{root}",
        "--output",
        OUTPUT_TEMPLATE,
        "--restrict-filenames",
        "--trim-filenames",
        "80",
        "--download-archive",
        root / "archive.txt",
        "--write-info-json",
        "--write-subs",
        "--write-auto-subs",
        "--sub-langs",
        "en.*",
        "--convert-subs",
        "vtt",
        "--ignore-errors",
        "--no-abort-on-error",
    ]
    if subs_only:
        cmd += ["--skip-download"]
    else:
        cmd += [
            "--format-sort",
            f"res:{height},codec:h264:aac",
            "--merge-output-format",
            "mp4",
        ]
    cmd.append(url)
    run(cmd)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--playlists",
        type=Path,
        default=REPO_ROOT / "3b1b-playlists.txt",
        help="plik z adresami playlist, jeden na linię",
    )
    parser.add_argument("--root", help="katalog roboczy poza repozytorium")
    parser.add_argument(
        "--height",
        type=int,
        default=720,
        help="preferowana wysokość obrazu; niżej = mniejszy plik do wklejenia do czatu",
    )
    parser.add_argument(
        "--subs-only",
        action="store_true",
        help="tylko napisy i metadane, bez wideo",
    )
    args = parser.parse_args()

    root = reference_root(args.root)
    for url in playlists(args.playlists):
        fetch(url, root, args.height, args.subs_only)
    print(f"gotowe: {root}")


if __name__ == "__main__":
    main()

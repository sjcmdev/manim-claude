#!/usr/bin/env python3
"""Buduje lokalny indeks odcisków klonu `3b1b/videos` dla `no_3b1b_code.py`.

Indeks nie zawiera kodu źródłowego, tylko skróty:

- dla plików `.py` — SHA-256 znormalizowanych okien 50 znaczących tokenów
  (patrz `no_3b1b_code.significant_tokens`);
- dla plików binarnych/medialnych — SHA-256 całego pliku.

Zapisywany jako `<katalog roboczy>/fingerprint_index.json`. Katalog roboczy
leży poza repozytorium (`common.reference_root`), więc indeks — tak jak sam
klon — nigdy nie trafia do gita.

Uruchomienie: `uv run python tooling/hooks/build_fingerprint_index.py`,
wymaga wcześniejszego klonu `3b1b/videos` w `<katalog roboczy>/_code/videos`.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from no_3b1b_code import (  # reference_root: no_3b1b_code już go importuje z common
    CLONE_REL,
    INDEX_NAME,
    WINDOW_SIZE,
    is_probably_text,
    reference_root,
    sha256_bytes,
    significant_tokens,
    window_hashes,
)


def build(clone: Path) -> dict:
    token_hashes: set[str] = set()
    media_hashes: set[str] = set()
    for path in clone.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        data = path.read_bytes()
        if not is_probably_text(data):
            media_hashes.add(sha256_bytes(data))
        elif path.suffix == ".py":
            text = data.decode("utf-8", errors="ignore")
            token_hashes.update(window_hashes(significant_tokens(text), WINDOW_SIZE))
    return {
        "version": 1,
        "window": WINDOW_SIZE,
        "token_hashes": sorted(token_hashes),
        "media_hashes": sorted(media_hashes),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="katalog roboczy poza repozytorium")
    args = parser.parse_args()

    root = reference_root(args.root)
    clone = root / CLONE_REL
    if not clone.is_dir():
        raise SystemExit(f"brak klonu 3b1b/videos w {clone}; sklonuj go zanim zbudujesz indeks")

    index = build(clone)
    index_path = root / INDEX_NAME
    index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")
    print(
        f"indeks zapisany: {index_path} "
        f"({len(index['token_hashes'])} odcisków kodu, {len(index['media_hashes'])} mediów)"
    )


if __name__ == "__main__":
    main()

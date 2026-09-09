"""Wspólne pomocniki skryptów mielących materiał referencyjny.

Materiał referencyjny (3b1b, CC BY-NC-SA 4.0) nigdy nie trafia do drzewa projektu.
Katalog roboczy leży poza repozytorium i jest tu wymuszany maszynowo.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

DEFAULT_ROOT = Path.home() / "manim-claude-reference"
REPO_ROOT = Path(__file__).resolve().parents[2]
VIDEO_SUFFIXES = (".mp4", ".mkv", ".webm")


def reference_root(arg: str | None = None) -> Path:
    """Katalog roboczy: argument, zmienna MANIM_CLAUDE_REFERENCE albo wartość domyślna."""
    raw = arg or os.environ.get("MANIM_CLAUDE_REFERENCE") or DEFAULT_ROOT
    root = Path(raw).expanduser().resolve()
    if root == REPO_ROOT or REPO_ROOT in root.parents:
        sys.exit(
            f"odmowa: {root} leży w repozytorium; materiał referencyjny musi być poza nim"
        )
    root.mkdir(parents=True, exist_ok=True)
    return root


def run(cmd: list[str | Path], **kwargs) -> subprocess.CompletedProcess:
    argv = [str(c) for c in cmd]
    print("+", " ".join(argv), file=sys.stderr)
    return subprocess.run(argv, check=True, **kwargs)


def video_dirs(root: Path) -> list[Path]:
    """Katalogi pojedynczych filmów: <root>/<playlista>/<NNN-id>/."""
    return sorted({p.parent for p in root.glob("*/*/*.info.json")})


def video_file(vdir: Path) -> Path | None:
    for path in sorted(vdir.iterdir()):
        if path.suffix.lower() in VIDEO_SUFFIXES:
            return path
    return None


def hhmmss(seconds: float) -> str:
    total = int(seconds)
    h, rest = divmod(total, 3600)
    m, s = divmod(rest, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

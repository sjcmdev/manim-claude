#!/usr/bin/env python3
"""Uruchamia lokalne bramki techniczne w ustalonej kolejności."""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Stage:
    """Jedna bramka oraz opcjonalny skrypt wymagany do jej uruchomienia."""

    name: str
    command: tuple[str, ...]
    required_path: Path | None = None


def default_stages(root: Path, *, python: str) -> list[Stage]:
    """Bramki projektu w kolejności wiążącej dla lokalnego sprawdzenia."""
    license_scan = root / "tooling" / "hooks" / "no_3b1b_code.py"
    corpus_validator = root / "tooling" / "reference" / "validate_observations.py"
    return [
        Stage("formatowanie", ("ruff", "format", "--check", ".")),
        Stage("lint", ("ruff", "check", ".")),
        Stage("typowanie", ("mypy", ".")),
        Stage("testy", ("pytest",)),
        Stage(
            "skan licencyjny",
            (python, str(license_scan), "--scan"),
            license_scan,
        ),
        Stage(
            "walidacja korpusu",
            (python, str(corpus_validator)),
            corpus_validator,
        ),
    ]


def run_stages(stages: Sequence[Stage], *, cwd: Path) -> int:
    """Uruchamia bramki kolejno i zwraca kod pierwszej porażki."""
    for stage in stages:
        print(f"\n==> {stage.name}", flush=True)
        if stage.required_path is not None and not stage.required_path.is_file():
            print(f"POMINIĘTO: brak skryptu {stage.required_path}", flush=True)
            continue

        command = subprocess.list2cmdline(stage.command)
        print(f"$ {command}", flush=True)
        try:
            result = subprocess.run(stage.command, cwd=cwd, check=False)
        except OSError as exc:
            print(f"BŁĄD: nie można uruchomić komendy: {exc}", flush=True)
            return 127
        if result.returncode != 0:
            print(f"BŁĄD: {stage.name} (kod {result.returncode})", flush=True)
            return result.returncode
        print(f"OK: {stage.name}", flush=True)

    return 0


def main() -> int:
    return run_stages(default_stages(REPO_ROOT, python=sys.executable), cwd=REPO_ROOT)


if __name__ == "__main__":
    raise SystemExit(main())

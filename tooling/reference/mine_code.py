#!/usr/bin/env python3
"""Puszcza agenta Codex na katalogach tematycznych klonu `3b1b/videos`.

Jeden katalog tematyczny (`_ROK/temat/`) to jeden przebieg i jeden plik obserwacji.
Klon i wyniki leżą w katalogu roboczym poza repozytorium — patrz `common.py`.

Codex pracuje w trybie do odczytu, więc nie może niczego zapisać w klonie.
Wynik wraca przez `--output-last-message`, nie przez zapis do pliku przez agenta.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from common import reference_root

PROMPT = Path(__file__).with_name("code_miner_prompt.md")


def codex_argv() -> list[str]:
    """Jak wywołać Codeksa, żeby prompt dotarł w całości.

    Na Windowsie `codex` to shim `codex.cmd`, który przekazuje argumenty przez
    `%*`, czyli przez cmd.exe. Wielolinijkowy prompt jest tam obcinany do pierwszej
    linii i agent dostaje instrukcję bez nazwy katalogu. Dlatego wołamy `codex.js`
    wprost przez node, z pominięciem shima.
    """
    shim = shutil.which("codex")
    if not shim:
        raise SystemExit("brak `codex` w PATH")
    js = Path(shim).parent / "node_modules" / "@openai" / "codex" / "bin" / "codex.js"
    node = shutil.which("node")
    if js.is_file() and node:
        return [node, str(js)]
    return [shim]


def cel(topic: Path, rel: str) -> str:
    """Ostatnia linia promptu: co dokładnie agent ma przeczytać."""
    if topic.is_file():
        return f"Materiałem jest pojedynczy plik, nie katalog. Plik do analizy: {rel}"
    return f"Katalog do analizy: {rel}"


def py_lines(path: Path) -> int:
    return sum(
        len(f.read_text(encoding="utf-8", errors="replace").splitlines())
        for f in path.rglob("*.py")
    )


def topic_dirs(
    clone: Path, years: list[str], min_lines: int, skip: list[str], extra: list[str]
) -> list[Path]:
    """Katalogi tematyczne z podanych roczników, powyżej progu, plus doproszone ręcznie."""
    found = []
    for year in years:
        for path in sorted((clone / year).glob("*/")):
            if path.is_dir() and py_lines(path) >= min_lines:
                found.append(path)
    for rel in extra:
        path = clone / rel
        if not path.exists():
            raise SystemExit(f"brak {rel} w klonie")
        found.append(path)
    return [p for p in found if p.relative_to(clone).as_posix() not in skip]


def mine(
    topic: Path, clone: Path, out_dir: Path, prompt: str, codex: list[str], effort: str
) -> tuple[str, str]:
    rel = topic.relative_to(clone).as_posix()
    slug = rel[:-3] if rel.endswith(".py") else rel
    out = out_dir / (slug.replace("/", "-") + ".yaml")
    if out.exists():
        if out.read_text(encoding="utf-8").lstrip().startswith("observations:"):
            return rel, "pominięty, wynik już jest"
        out.unlink()
    cmd = [
        *codex, "exec",
        "-s", "read-only",
        "-c", f"model_reasoning_effort={effort}",
        "-o", str(out),
        f"{prompt}\n\n{cel(topic, rel)}",
    ]
    proc = subprocess.run(
        cmd,
        cwd=clone,
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=1800,
    )
    if proc.returncode != 0 or not out.exists():
        return rel, f"BŁĄD (kod {proc.returncode})"

    # Agent bywa, że zamiast analizy zwraca prośbę o wskazanie pliku. Taki wynik
    # kasujemy, żeby ponowny przebieg spróbował jeszcze raz zamiast go pominąć.
    text = out.read_text(encoding="utf-8")
    if not text.lstrip().startswith("observations:"):
        out.unlink()
        return rel, f"BŁĄD: to nie są obserwacje ({text.strip()[:60]}...)"
    return rel, f"gotowe, {len(text.splitlines())} linii"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="katalog roboczy poza repozytorium")
    parser.add_argument(
        "--years",
        nargs="+",
        default=["_2022", "_2023", "_2024", "_2025", "_2026"],
        help="roczniki do zmielenia; zakres kodu wg design-spec 9.2 to 2022 i później",
    )
    parser.add_argument("--min-lines", type=int, default=1000)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument(
        "--skip",
        nargs="*",
        default=[],
        help="katalogi do pominięcia, np. _2024/transformers",
    )
    parser.add_argument(
        "--extra",
        nargs="*",
        default=[],
        help="katalogi doproszone spoza skanowanych roczników, np. _2017/eoc",
    )
    parser.add_argument(
        "--effort",
        default="high",
        help="model_reasoning_effort dla przebiegu; abstrahowanie wzorców z kilkunastu "
        "tysięcy linii jest pracą rozumowaniem, więc domyślnie wyżej niż konfiguracja",
    )
    args = parser.parse_args()

    codex = codex_argv()

    root = reference_root(args.root)
    clone = root / "_code" / "videos"
    if not clone.is_dir():
        raise SystemExit(f"brak klonu w {clone}; sklonuj 3b1b/videos zanim uruchomisz miner")

    out_dir = root / "_observations" / "code"
    out_dir.mkdir(parents=True, exist_ok=True)
    prompt = PROMPT.read_text(encoding="utf-8")

    topics = topic_dirs(clone, args.years, args.min_lines, args.skip, args.extra)
    print(f"katalogów do zmielenia: {len(topics)}")

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        run = lambda t: mine(t, clone, out_dir, prompt, codex, args.effort)  # noqa: E731
        for rel, status in pool.map(run, topics):
            print(f"{rel:40s} {status}", flush=True)

    print(f"wyniki: {out_dir}")


if __name__ == "__main__":
    main()

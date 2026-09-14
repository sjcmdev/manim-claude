#!/usr/bin/env python3
"""Puszcza agenta Codex na katalogach tematycznych klonu `3b1b/videos`.

Jeden katalog tematyczny (`_ROK/temat/`) to jeden przebieg i jeden plik obserwacji.
Klon i wyniki leżą w katalogu roboczym poza repozytorium — patrz `common.py`.

Codex pracuje w trybie do odczytu, więc nie może niczego zapisać w klonie.
Wynik wraca przez `--output-last-message`, nie przez zapis do pliku przez agenta.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from common import reference_root
from manifest import build_manifest, sha256_file, write_manifest
from validate_observations import validate_pair

DEFAULT_PROMPT = Path(__file__).with_name("code_miner_prompt.md")


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
    topic: Path,
    clone: Path,
    out_dir: Path,
    prompt: str,
    codex: list[str],
    effort: str,
    *,
    prompt_path: Path = DEFAULT_PROMPT,
    manifest_dir: Path | None = None,
    timeout: int = 1800,
) -> tuple[str, str]:
    rel = topic.relative_to(clone).as_posix()
    slug = rel[:-3] if rel.endswith(".py") else rel
    out = out_dir / (slug.replace("/", "-") + ".yaml")
    document_type = out_dir.name
    if manifest_dir is None:
        manifest_dir = out_dir.parent / "manifests" / document_type
    manifest_out = manifest_dir / out.with_suffix(".json").name
    if out.exists() and manifest_out.exists():
        if not validate_pair(out, manifest_out, document_type):
            return rel, "pominięty, wynik już jest"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="mine-", dir=out_dir.parent) as temp_name:
        temp_dir = Path(temp_name)
        candidate = temp_dir / out.name
        candidate_manifest = temp_dir / manifest_out.name
        cmd = [
            *codex,
            "exec",
            "-s",
            "read-only",
            "-c",
            f"model_reasoning_effort={effort}",
            "-o",
            str(candidate),
            f"{prompt}\n\n{cel(topic, rel)}",
        ]
        try:
            proc = subprocess.run(
                cmd,
                cwd=clone,
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return rel, f"BŁĄD: timeout po {timeout} s"
        if proc.returncode != 0 or not candidate.exists():
            return rel, f"BŁĄD (kod {proc.returncode})"

        try:
            revision = subprocess.check_output(
                ["git", "-C", str(clone), "rev-parse", "HEAD"],
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except (OSError, subprocess.CalledProcessError):
            revision = None
        payload = build_manifest(
            candidate,
            document_type,
            f"{document_type}/{out.name}",
            provenance_status="generated",
            source_path=rel,
            source_revision=revision,
            prompt_path=prompt_path.as_posix(),
            prompt_sha256=sha256_file(prompt_path),
            effort=effort,
        )
        write_manifest(candidate_manifest, payload)
        errors = validate_pair(candidate, candidate_manifest, document_type)
        if errors:
            return rel, f"BŁĄD: walidacja ({errors[0]})"

        # Oba pliki są kompletne przed publikacją. Gdy drugi replace zawiedzie,
        # pierwszy jest cofany, żeby nie pozostawić osieroconego wyniku.
        backup = temp_dir / "previous.yaml"
        if out.exists():
            shutil.copy2(out, backup)
        os.replace(candidate, out)
        try:
            os.replace(candidate_manifest, manifest_out)
        except OSError:
            if backup.exists():
                os.replace(backup, out)
            else:
                out.unlink(missing_ok=True)
            raise
        text = out.read_text(encoding="utf-8")
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
        "--prompt",
        type=Path,
        default=DEFAULT_PROMPT,
        help="instrukcja dla agenta; różne analizy tego samego materiału różnią się"
        " wyłącznie tym plikiem",
    )
    parser.add_argument(
        "--out",
        default="code",
        help="podkatalog w _observations, do którego trafiają wyniki",
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

    out_dir = root / "_observations" / args.out
    manifest_dir = root / "_observations" / "manifests" / args.out
    prompt = args.prompt.read_text(encoding="utf-8")

    topics = topic_dirs(clone, args.years, args.min_lines, args.skip, args.extra)
    print(f"katalogów do zmielenia: {len(topics)}")

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        run = lambda t: mine(  # noqa: E731
            t,
            clone,
            out_dir,
            prompt,
            codex,
            args.effort,
            prompt_path=args.prompt,
            manifest_dir=manifest_dir,
        )
        for rel, status in pool.map(run, topics):
            print(f"{rel:40s} {status}", flush=True)

    print(f"wyniki: {out_dir}")


if __name__ == "__main__":
    main()

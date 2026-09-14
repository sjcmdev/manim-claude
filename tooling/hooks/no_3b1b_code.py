#!/usr/bin/env python3
"""Lokalna ochrona przed kopiowaniem kodu i mediów 3b1b/videos.

Dwa tryby:

- hook `PreToolUse` (domyślny) — czyta z stdin JSON opisujący wywołanie
  narzędzia Claude Code (`tool_name`, `tool_input`), sprawdza nową treść
  zapisu/edycji wobec lokalnego indeksu odcisków. Blokada = exit 2 i powód
  na stderr, zgodnie z protokołem hooków Claude Code.
- `--scan` — sprawdza pliki repozytorium (tekstowe wobec indeksu odcisków,
  binarne/medialne wobec hashy SHA-256 z indeksu). Exit != 0 przy naruszeniu.

Indeks buduje `build_fingerprint_index.py` z lokalnego klonu `3b1b/videos` i
zapisuje go w katalogu roboczym poza repozytorium (patrz `common.reference_root`),
więc indeks — tak jak sam klon — nigdy nie trafia do gita.

Zachowanie zgodne ze spec `docs/superpowers/specs/2026-09-14-repository-foundations-design.md`:
brak klonu przepuszcza, klon bez indeksu blokuje z komendą naprawczą, dopasowanie
odcisku albo zabronione medium blokuje z przyczyną, a każdy błąd wewnętrzny przy
obecnym klonie jest też blokadą — ochrona jest fail-closed, nie ciche zezwolenie.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import keyword
import subprocess
import sys
import tokenize
from io import StringIO
from pathlib import Path
from tokenize import TokenError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "reference"))
from common import REPO_ROOT, reference_root  # noqa: E402

CHECKED_TOOLS = {"Write", "Edit", "MultiEdit"}
CLONE_REL = Path("_code") / "videos"
INDEX_NAME = "fingerprint_index.json"
WINDOW_SIZE = 50


def significant_tokens(text: str) -> list[str]:
    """Znaczące tokeny źródła: bez komentarzy, bez linii `import`/`from ... import`,
    identyfikatory i literały znormalizowane do wspólnych placeholderów. Dzięki temu
    zmiana nazw zmiennych albo wartości stałych nie omija dopasowania — liczy się
    struktura, nie nazewnictwo.

    Best-effort: treść może nie być poprawnym Pythonem (np. hook dostaje Markdown).
    `tokenize` w takim wypadku rzuca wyjątek w miejscu błędu — łapiemy go i zwracamy
    tokeny rozpoznane do tego miejsca, zamiast wywalać cały hook.
    """
    tokens: list[str] = []
    line: list[str] = []

    def flush() -> None:
        if line and line[0] in ("import", "from"):
            line.clear()
            return
        tokens.extend(line)
        line.clear()

    try:
        for tok in tokenize.generate_tokens(StringIO(text).readline):
            kind, value = tok.type, tok.string
            if kind in (
                tokenize.COMMENT,
                tokenize.INDENT,
                tokenize.DEDENT,
                tokenize.ENCODING,
                tokenize.ENDMARKER,
                tokenize.NL,
            ):
                continue
            if kind == tokenize.NEWLINE:
                flush()
                continue
            if kind == tokenize.NAME and not keyword.iskeyword(value):
                line.append("ID")
            elif kind in (tokenize.NUMBER, tokenize.STRING):
                line.append("LIT")
            else:
                line.append(value)
        flush()
    except (TokenError, IndentationError, SyntaxError, ValueError):
        pass
    return tokens


def window_hashes(tokens: list[str], window: int = WINDOW_SIZE) -> list[str]:
    """Skróty SHA-256 znormalizowanych okien `window` kolejnych tokenów."""
    if len(tokens) < window:
        return []
    return [
        hashlib.sha256(" ".join(tokens[i : i + window]).encode("utf-8")).hexdigest()
        for i in range(len(tokens) - window + 1)
    ]


def is_probably_text(data: bytes) -> bool:
    """Plik jest tekstowy, jeśli daje się bezstratnie odczytać jako UTF-8.

    ponytail: heurystyka na sam dekoder UTF-8, bez sniffingu typu MIME — dla
    korpusu Pythona i typowych mediów (obraz/wideo/audio) to wystarcza; plik w
    innym kodowaniu tekstowym (np. latin-1) trafi błędnie do ścieżki binarnej.
    """
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return True


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract_contents(tool_name: str, tool_input: dict) -> list[str]:
    """Nowa treść tekstowa proponowana przez wywołanie narzędzia."""
    if tool_name == "Write":
        return [str(tool_input.get("content", ""))]
    if tool_name == "Edit":
        return [str(tool_input.get("new_string", ""))]
    if tool_name == "MultiEdit":
        return [str(e.get("new_string", "")) for e in tool_input.get("edits", [])]
    return []


def load_index(root: Path) -> dict:
    return json.loads((root / INDEX_NAME).read_text(encoding="utf-8"))


def evaluate(payload: dict, root_arg: str | None) -> tuple[int, str]:
    """Ocena jednego wywołania hooka. Zwraca (kod wyjścia, powód); 0 = zezwól, 2 = zablokuj.

    Może rzucić wyjątkiem (np. zepsuty indeks) — wołający ma go złapać jako błąd
    ochrony i zablokować, nie potraktować jako ciche zezwolenie.
    """
    tool_name = payload.get("tool_name", "")
    if tool_name not in CHECKED_TOOLS:
        return 0, ""

    root = reference_root(root_arg)
    clone = root / CLONE_REL
    if not clone.is_dir():
        return 0, ""  # brak lokalnego klonu 3b1b — nic do porównania

    if not (root / INDEX_NAME).is_file():
        return 2, (
            f"brak indeksu odcisków kodu 3b1b dla klonu w {root}; zbuduj go: "
            "uv run python tooling/hooks/build_fingerprint_index.py"
        )

    index = load_index(root)
    token_hashes = set(index.get("token_hashes", []))
    window = int(index.get("window", WINDOW_SIZE))
    for text in extract_contents(tool_name, payload.get("tool_input", {})):
        if token_hashes.intersection(window_hashes(significant_tokens(text), window)):
            return 2, (
                f"podobieństwo do indeksu odcisków kodu 3b1b: dopasowano okno "
                f"{window} znaczących tokenów; to wygląda na skopiowaną implementację, "
                "nie naukę ze źródła"
            )
    return 0, ""


def protect(payload: dict, root_arg: str | None = None) -> tuple[int, str]:
    """`evaluate` z fail-closed łapaniem błędów: wyjątek przy obecnym klonie to blokada."""
    try:
        return evaluate(payload, root_arg)
    except Exception as exc:  # ochrona ma priorytet nad wygodą — nie przepuszczamy po cichu
        return 2, f"błąd hooka ochrony przed kopiowaniem 3b1b: {exc!r}"


def hook(root_arg: str | None) -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError as exc:
        print(
            f"błąd hooka ochrony przed kopiowaniem 3b1b: nieprawidłowy JSON na wejściu ({exc})",
            file=sys.stderr,
        )
        return 2
    code, reason = protect(payload, root_arg)
    if code != 0:
        print(reason, file=sys.stderr)
    return code


def check_bytes(
    rel: str, data: bytes, token_hashes: set, media_hashes: set, window: int
) -> str | None:
    """Sprawdza zawartość jednego pliku repozytorium wobec indeksu. `None` = brak naruszenia."""
    if is_probably_text(data):
        text = data.decode("utf-8", errors="ignore")
        if token_hashes.intersection(window_hashes(significant_tokens(text), window)):
            return f"{rel}: podobieństwo do indeksu odcisków kodu 3b1b"
        return None
    digest = sha256_bytes(data)
    if digest in media_hashes:
        return f"{rel}: hash pliku zgodny z materiałem źródłowym 3b1b (zabronione medium)"
    return None


def repo_files() -> list[str]:
    """Pliki repozytorium tak, jak widzi je git: śledzone i nowe, bez zignorowanych."""
    proc = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files", "--cached", "--others", "--exclude-standard"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [ln for ln in proc.stdout.splitlines() if ln]


def scan(root_arg: str | None) -> int:
    try:
        root = reference_root(root_arg)
        clone = root / CLONE_REL
        if not clone.is_dir():
            print("brak lokalnego klonu 3b1b/videos — pomijam skan", file=sys.stderr)
            return 0
        if not (root / INDEX_NAME).is_file():
            print(
                f"brak indeksu odcisków kodu 3b1b dla klonu w {root}; zbuduj go: "
                "uv run python tooling/hooks/build_fingerprint_index.py",
                file=sys.stderr,
            )
            return 2
        index = load_index(root)
        token_hashes = set(index.get("token_hashes", []))
        media_hashes = set(index.get("media_hashes", []))
        window = int(index.get("window", WINDOW_SIZE))

        violations = []
        for rel in repo_files():
            path = REPO_ROOT / rel
            if not path.is_file():
                continue
            violation = check_bytes(rel, path.read_bytes(), token_hashes, media_hashes, window)
            if violation:
                violations.append(violation)
    except Exception as exc:  # jak w hooku: błąd przy obecnym klonie jest blokadą
        print(f"błąd skanu ochrony przed kopiowaniem 3b1b: {exc!r}", file=sys.stderr)
        return 2

    for v in violations:
        print(v, file=sys.stderr)
    if violations:
        print(f"skan: {len(violations)} naruszeń", file=sys.stderr)
        return 2
    print("skan: brak naruszeń", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scan",
        action="store_true",
        help="skanuj repozytorium zamiast czytać wywołanie hooka z stdin",
    )
    parser.add_argument("--root", help="katalog roboczy poza repozytorium (jak w reference_root)")
    args = parser.parse_args(argv)
    return scan(args.root) if args.scan else hook(args.root)


if __name__ == "__main__":
    sys.exit(main())

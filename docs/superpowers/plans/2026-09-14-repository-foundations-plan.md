# Plan implementacji: fundamenty repozytorium

Spec: `docs/superpowers/specs/2026-09-14-repository-foundations-design.md` — wiąże.
Odstępstwo od speca: zamiast trzech gałęzi jedna, `task/02-fundamenty-repozytorium`,
trzech wykonawców równolegle na rozłącznych plikach.

## Zasady wspólne

- Nie wykonujesz `git add/commit/push/switch/stash/reset`. Commity robi integrator.
- Dotykasz WYŁĄCZNIE plików ze swojej listy. Potrzebna zmiana poza nią → zapisz w raporcie.
- Test-first: najpierw test odtwarzający problem, potem implementacja.
- Python >=3.11, tylko stdlib + `pyyaml` (+ `pytest` do testów). Bez nowych zależności
  bez uzasadnienia w raporcie.
- Kod i komentarze w stylu istniejącego `tooling/reference/*.py` (komentarze po polsku).
- Raport końcowy: lista plików, co działa, jak uruchomić testy, co pominięte.

## W1 — hook licencyjny i licencje (agent Claude)

Pliki: `LICENSE`, `LICENSE-CONTENT.md`, `.claude/settings.json`,
`tooling/hooks/no_3b1b_code.py`, `tooling/hooks/build_fingerprint_index.py`,
`tooling/hooks/README.md`, `tests/test_no_3b1b_code.py`.

1. `LICENSE` MIT (rok 2026, właściciel: autorzy manim-claude) dla kodu;
   `LICENSE-CONTENT.md` CC BY-NC-SA 4.0 dla dokumentacji, `research/`, `observations/`,
   przyszłych `idioms/` — z jawną granicą obu zakresów i zastrzeżeniem o prawach źródeł.
2. Indeks: `build_fingerprint_index.py` czyta klon z `MANIM_CLAUDE_REFERENCE_ROOT`
   (domyślnie `~/manim-claude-reference`, reuse `tooling/reference/common.py:reference_root`),
   zapisuje lokalnie (poza gitem) odciski znormalizowanych okien 50 znaczących tokenów
   (tokenize, bez komentarzy/importów, identyfikatory i literały znormalizowane) jako hashe
   oraz SHA-256 plików binarnych/medialnych. Bez kodu źródłowego w indeksie.
3. `no_3b1b_code.py`, dwa tryby:
   - hook `PreToolUse` (Write|Edit|MultiEdit): JSON na stdin, sprawdza nową treść;
     blokada = exit 2 + powód na stderr;
   - `--scan`: pliki tekstowe repo + hashe binariów/mediów; exit ≠ 0 przy naruszeniu.
   Zachowanie: brak klonu → przepuść; klon bez indeksu → blokuj z komendą naprawczą;
   dopasowanie/zabronione medium → blokuj z przyczyną; wyjątek przy obecnym klonie → blokuj.
4. Rejestracja w `.claude/settings.json` bez ścieżek właściwych jednej maszynie.
5. Testy na fixture'ach w `tmp_path` (sztuczny „klon”): 4 scenariusze powyżej + config hooka.

## W2 — walidator korpusu, manifesty, miner (Codex)

Pliki: `tooling/reference/validate_observations.py`, `tooling/reference/mine_code.py`,
`tooling/reference/manifest.py` (jeśli potrzebny), `observations/code/**`,
`observations/animation/**`, `observations/recipes/**`, `observations/manifests/**`,
`observations/README.md`, `tests/test_validate_observations.py`, `tests/test_mine_code.py`.

Zakres: rozdziały „Kontrakt korpusu”, „Naprawa obecnych danych”, „Manifesty pochodzenia”
speca. Kolejność: testy klas błędów → walidator → mechaniczna naprawa danych (osobny
skrypt jednorazowy lub ręcznie, diff czytelny) → manifesty `legacy-unverified` z `null`
dla nieznanych → miner: tmp dir, walidacja pary, atomowe przeniesienie, `TimeoutExpired`
złapany per zadanie. Nie zmieniaj znaczenia obserwacji.

## W3 — bramki techniczne (agent Claude, niski model)

Pliki: `pyproject.toml`, `tooling/check.py`, `tests/test_check.py`,
oraz poprawki lint/typów wyłącznie w `tooling/reference/{common,fetch_reference,
extract_frames,make_packet}.py` i `tests/test_reference.py`.

`pyproject.toml` (Python >=3.11, zależności dev: ruff, mypy, pytest, pyyaml, types-PyYAML),
konfiguracja ruff/mypy/pytest. `uv run python tooling/check.py` uruchamia kolejno:
`ruff format --check`, `ruff check`, `mypy`, `pytest`, `no_3b1b_code.py --scan`,
`validate_observations.py`; pomija z komunikatem krok, którego skrypt jeszcze nie istnieje
(W1/W2 powstają równolegle); zatrzymuje się na pierwszym błędzie, pokazując komendę i wynik.
Bez GitHub Actions. Bez szerokich refaktoryzacji.

## Integracja (Claude główny)

Po W1–W3: pełne `uv run python tooling/check.py`, przegląd diffu, poprawki styku,
commity per wykonawca, aktualizacja `TODO.md` (numeracja zadań vs spec).

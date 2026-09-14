# tooling/hooks

Lokalna ochrona przed kopiowaniem kodu i mediów 3b1b/videos do tego repozytorium.
Uczymy się ze źródeł objętych CC BY-NC-SA, ale nie kopiujemy ich implementacji
ani zasobów — patrz „Lokalna ochrona” w
`docs/superpowers/specs/2026-09-14-repository-foundations-design.md`.

## Jak to działa

1. `build_fingerprint_index.py` czyta lokalny klon `3b1b/videos` z
   `<katalog roboczy>/_code/videos` (katalog roboczy: `MANIM_CLAUDE_REFERENCE`,
   domyślnie `~/manim-claude-reference` — patrz `tooling/reference/common.py`)
   i zapisuje `<katalog roboczy>/fingerprint_index.json`. Indeks nie zawiera
   kodu źródłowego: dla plików `.py` trzyma SHA-256 znormalizowanych okien
   50 znaczących tokenów (bez komentarzy i linii `import`, identyfikatory i
   literały znormalizowane), dla plików binarnych/medialnych SHA-256 całego
   pliku. Indeks leży w katalogu roboczym, poza repozytorium — nigdy nie
   trafia do gita.
2. `no_3b1b_code.py` sprawdza nową treść wobec tego indeksu, w dwóch trybach:
   - **hook `PreToolUse`** (domyślny, rejestrowany w `.claude/settings.json`
     dla `Write`, `Edit`, `MultiEdit`) — czyta JSON wywołania narzędzia z
     stdin, sprawdza proponowaną treść tekstową. Blokada = exit 2 i powód na
     stderr, co Claude Code pokazuje modelowi jako odrzucenie zapisu.
   - **`--scan`** — sprawdza pliki repozytorium widziane przez `git ls-files`:
     tekstowe wobec indeksu odcisków, binarne/medialne wobec hashy SHA-256.
     Exit != 0 przy naruszeniu. Ten tryb wchodzi w skład `tooling/check.py`.

## Zachowanie

| sytuacja | wynik |
|---|---|
| brak lokalnego klonu `3b1b/videos` | przepuszcza — nic do porównania |
| klon jest, ale indeksu brak | blokuje, podaje komendę naprawczą |
| dopasowanie odcisku albo zabroniony hash medium | blokuje, podaje przyczynę |
| błąd wewnętrzny przy obecnym klonie (np. zepsuty indeks) | blokuje — ochrona jest fail-closed, błąd nie oznacza cichego zezwolenia |

## Procedura

```bash
# jednorazowo albo po aktualizacji klonu (katalog roboczy: $MANIM_CLAUDE_REFERENCE,
# domyślnie ~/manim-claude-reference):
git clone https://github.com/3b1b/videos "${MANIM_CLAUDE_REFERENCE:-$HOME/manim-claude-reference}/_code/videos"
uv run python tooling/hooks/build_fingerprint_index.py

# ręczny skan całego repozytorium (to samo robi tooling/check.py):
uv run python tooling/hooks/no_3b1b_code.py --scan
```

Hook nie zastępuje przeglądu prawnego ani przeglądu kodu — to praktyczne
egzekwowanie zasady, nie jej cała treść. Domyślny próg dopasowania to 50
znaczących tokenów; import i standardowy boilerplate same z siebie nie
blokują, bo linie `import`/`from ... import` są wycinane z indeksu.

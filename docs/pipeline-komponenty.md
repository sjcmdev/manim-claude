# Pipeline wtyczki: co jest hookiem, co skryptem, co skillem, co agentem

**Status:** propozycja na spotkanie 2026-09-14. Nie wiąże, dopóki nie trafi do
`design-spec.md` albo `decision-log.md`. Porządkuje rozdziały 5.2 i 8 speca i rozstrzyga
rozjazdy między specem a `TODO.md`.

## 1. Reguła przydziału

Pytamy po kolei i zatrzymujemy się na pierwszym „tak” — od najtwardszego mechanizmu
do najmiękkiego (ta sama drabina co w peer review: hook → skrypt → skill → proza).

| pytanie | jeśli tak | cechy |
|---|---|---|
| Czy to sprawdzenie jest deterministyczne, tanie (< 1 s) i ma zablokować zapis? | **hook** | bez modelu, bez renderu, bez sieci; exit 0 / 2 / błąd ochrony |
| Czy to deterministyczna praca, może ciężka (render, ffmpeg, parsowanie)? | **skrypt** | bez modelu; wołany jawnie; wynik i status do pliku |
| Czy to przepływ z człowiekiem w pętli albo orkestracja kroków? | **skill** | działa w głównym kontekście; pyta użytkownika; zapisuje flagi akceptacji |
| Czy potrzebny osobny, wąski kontekst: świeże oczy, równoległość, inny model? | **agent** | widzi tylko swój wycinek; zwraca wynik, nie rozmawia z użytkownikiem |
| Nic z powyższych | **proza** (`idioms/*.md`, `CLAUDE.md`) | czytana przez agenta; najsłabsze egzekwowanie |

Dwie zasady pochodne:

- **Bramka to flaga, którą czyta maszyna.** Skill zapisuje `approved` w `storyboard.yaml`
  dopiero po odpowiedzi użytkownika; skrypt renderu odmawia, gdy flaga nie jest dosłownie
  `approved`. Model nie „pamięta” akceptacji.
- **Skrypt mierzy, zanim model oceni.** `visual-judge` dostaje wynik sprawdzeń
  mechanicznych (poza kadrem, nakładanie, minimalna wysokość tekstu) i ocenia tylko to,
  czego skrypt nie umie.

## 2. Tor B — przepływ produkcyjny (paczka użytkownika)

```text
wejście: opis + dokumenty + szkice + narration-profile + lessons
  │
  ├─ SKILL plan ─────────── samo-grill, parametry z pochodzeniem ──► plan.md
  │     └─ BRAMKA 1: użytkownik poprawia plan.md; skill zapisuje plan: approved
  │
  ├─ SKRYPT storyboard.py ─ plan.md ──► storyboard.yaml (generated) + archiwum
  │     └─ HOOK storyboard_integrity.py (PreToolUse): nikt ręcznie nie pisze w generated
  │
  ├─ SKILL build ────────── pętla po blokach, status każdego kroku w storyboard.state
  │     ├─ AGENT scene-coder ── storyboard bloku + idioms/ ──► scenes/<blok>.py
  │     ├─ HOOK check_scene_contract.py (PostToolUse): parse, klasa, sekcje, lint idiomów
  │     ├─ SKRYPT render.py --frame ── klatka statyczna
  │     ├─ SKRYPT layout_checks.py ── poza kadrem, nakładanie, wysokość tekstu
  │     ├─ AGENT visual-judge ── klatka + opis bloku + wynik checks ──► lista poprawek
  │     ├─ BRAMKA 2: SKRYPT contact_sheet.py; skill pyta; zapisuje layout: approved
  │     ├─ SKRYPT render.py --section (skip_animations dla poprzednich; odmawia bez approved)
  │     └─ AGENT visual-judge ── ocena sekcji, sufit prób z config
  │
  ├─ SKRYPT assemble.py ─── --save_sections + ffmpeg concat ──► podgląd ze znacznikami
  │
  └─ SKILL review ───────── BRAMKA 3: wybory blok.sekcja + werdykt ──► lessons.yaml
```

## 3. Tor A — przepływ deweloperski (`tooling/`, nie trafia do paczki)

```text
SKILL mine ──► AGENT code-miner (dziś: mine_code.py + Codex) ──► kandydaci YAML + manifest
           └─► AGENT narrative-miner (dziś: pakiet + zewnętrzny czat) ──► obserwacje z czasem
SKRYPT validate_observations.py ── kontrakt + manifest ──► observations/
SKRYPT merge_observations.py ──── duplikaty, konflikty, pochodzenie
SKILL curate ──► AGENT idiom-curator ──► propozycja; autor decyduje ──► idioms/ + lint-rules.yaml
HOOK no_3b1b_code.py (PreToolUse, zapis) ── pilnuje całego toru
```

## 4. Inwentarz po przydziale

| komponent | rodzaj | zdarzenie / wywołanie | model | stan |
|---|---|---|---|---|
| `plan` | skill | użytkownik | główny | planowany |
| `build` | skill | użytkownik | główny | planowany |
| `review` | skill | koniec `build` | główny | planowany |
| `probe` | skill | użytkownik | główny | planowany |
| `profile` | skill | jednorazowo | główny | planowany |
| `assemble` | **skrypt** (było: skill) | `build` | — | planowany |
| `scene-coder` | agent | `build` | tier średni | planowany |
| `visual-judge` | agent | `build` | tier najwyższy, obraz | planowany |
| `check_scene_contract.py` | hook PostToolUse | zapis `scenes/*.py` | — | planowany |
| `storyboard_integrity.py` | hook PreToolUse | zapis `storyboard.yaml` | — | planowany |
| `storyboard.py`, `render.py`, `layout_checks.py`, `contact_sheet.py`, `sections.py` | skrypty | skill `build` | — | planowane; `layout_checks.py` nowy |
| `mine`, `curate` | skille dev | autor | główny | planowane |
| `code-miner` | agent dev | `mine` | Codex (wyjątek od D2) | działa jako skrypt |
| `narrative-miner` | agent dev | `mine` | — | ręcznie przez czat |
| `idiom-curator` | agent dev | `curate` | tier średni | planowany |
| `no_3b1b_code.py` | hook PreToolUse + `--scan` | zapis; `check.py` | — | w budowie (task/02) |

## 5. Decyzje do podjęcia na spotkaniu

1. **`build` to skill czy `build.py`?** Spec 5.2 mówi skill, `TODO.md` task/19 mówi
   `build.py`. Propozycja: skill prowadzi pętlę i rozmowę, `build.py` jest zbiorem
   podkomend bez modelu, status w `storyboard.state`. Oba zostają, z podziałem ról.
2. **`assemble` ze skilla do skryptu.** Nie ma w nim decyzji ani rozmowy.
3. **Nowy skrypt `layout_checks.py`** przed `visual-judge` (peer review, „Design gaps”).
4. **Tiery zamiast nazw modeli** w `config.default.yaml` (`frontier`/`mid`/`cheap`
   + mapowanie w jednym miejscu).
5. **Codex w torze A** — zapisać w `decision-log.md` jako wyjątek deweloperski od D2.
6. **Tanie wyspecjalizowane agenty** (agenda 3d): updater / własny mobject jako agent czy
   skill z szablonem. Reguła z §1: agent tylko wtedy, gdy potrzebuje własnej pętli
   render–ocena; inaczej skill.
7. **Trzy kody wyjścia hooków:** 0 przepuść, 2 blokada merytoryczna, inny = hook nie
   zadziałał (fail-closed tam, gdzie stawką jest licencja).
8. **Forma dystrybucji:** `package/` jako wtyczka Claude Code (`.claude-plugin/plugin.json`,
   `skills/`, `agents/`, `hooks/hooks.json`, `scripts/`) — potwierdzić, zanim powstanie
   task/10-struktura.

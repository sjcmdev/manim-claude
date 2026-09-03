# TODO

Plan całego projektu i rejestr zadań. Jedno zadanie = jedna gałąź. Każda gałąź wraca
do `dev`. Do `main` trafia wyłącznie skończony etap.

Uzasadnienie i szczegóły techniczne zadań: `roadmap.md` oraz `design-spec.md`.
Ten plik jest listą roboczą, nie dokumentacją projektową.

## Polityka gałęzi

```
main          tylko stan gotowy do wydania; jeden merge na skończony etap, tagowany
 └── dev      gałąź integracyjna; tu ląduje każde zadanie
      └── task/01-krotki-tytul
      └── task/02-krotki-tytul
```

- Każde zadanie odbija się od `dev` i wraca do `dev`. Nazwa gałęzi:
  `task/xx-krotki-tytul`, gdzie `xx` to numer zadania z listy poniżej.
- `dev` wchodzi do `main` dopiero wtedy, gdy etap jest skończony i daje spójną
  całość funkcjonalną. Ten merge jest tagowany.
- Tory A i B (patrz `roadmap.md`) są niezależne, ale dzielą jedną gałąź `dev`
  i jedną numerację zadań. Numer mówi, kiedy zadanie powstało, nie w jakiej
  kolejności ma być zrobione.
- Zadanie wchodzi do `dev` dopiero, gdy przechodzą wszystkie bramki techniczne
  obowiązujące w danym momencie (lint, typy, testy — zestaw ustala zadanie 09).
- Wyjątek od reguły gałęzi: poprawka literówki w dokumencie może iść prosto do `dev`.
- Commity w konwencji [Conventional Commits](https://www.conventionalcommits.org/):
  `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`. Temat do 72 znaków,
  uzasadnienie w treści, gdy nie jest oczywiste.
- Gałąź zadania kasujemy po scaleniu. Poza `main` i `dev` nie ma gałęzi długo żyjących.

## Etap 0 — fundament

Musi być gotowe, zanim cokolwiek zostanie pobrane lub napisane.

### task/01-repozytorium

- [x] `git init`, gałęzie `main` i `dev`
- [x] `.gitignore` (Python, narzędzia, artefakty Manima, materiał referencyjny)
- [x] Dokumentacja projektowa w repozytorium
- [x] Zdalne repozytorium `sjcmdev/manim-claude`
- [ ] Ochrona gałęzi `main` i `dev` na GitHubie: pull request plus zielone CI
- [ ] `CONTRIBUTING.md` — środowisko, styl kodu, testy, ADR-y

### task/02-hook-licencyjny

Powstaje **przed** pobraniem czegokolwiek. Materiał na CC BY-NC-SA nigdy nie trafia
do drzewa projektu.

- [ ] `no_3b1b_code.py` — blokada wprowadzenia materiału objętego ShareAlike
- [ ] Katalog roboczy na materiał referencyjny poza repozytorium, wpis w `.gitignore`
- [ ] Test hooka: próba zapisu fragmentu kodu źródłowego 3b1b jest odrzucana
- [ ] Rejestracja hooka w konfiguracji Claude Code

## Etap 1A — pierwsza biblioteka idiomów (tor A)

Skończone, gdy `idioms/` zawiera zestaw reguł falsyfikowalnych z uzasadnieniem,
a `VERSION` wynosi 0.1.

### task/03-fetch-reference

- [ ] `fetch_reference.py` — napisy z czasami (`yt-dlp --write-auto-sub --skip-download`)
- [ ] Klatki kluczowe przez ffmpeg
- [ ] Zapis do katalogu roboczego poza repozytorium
- [ ] Lista źródeł z `3b1b-playlists.txt` jako wejście

### task/04-code-miner

- [ ] Agent `code-miner` — analiza kodu scen w katalogu tymczasowym
- [ ] Zakres: serie z roku 2022 i późniejsze
- [ ] Warstwa wzorców projektowych i architektonicznych, nie tylko idiomy powierzchniowe
- [ ] Wynik jako YAML obserwacji, zapisywany przez subagenta do pliku

### task/05-analiza-narracji

- [ ] Prompt wg szablonu z `design-spec.md`, rozdział 9.4
- [ ] Transkrypcje plus siatki klatek jako wejście dla zewnętrznego czatu
- [ ] Sztywny format odpowiedzi YAML
- [ ] Zakres obejmuje starsze klasyki, ale wyłącznie budowę wyjaśnienia

### task/06-merge-observations

- [ ] `merge_observations.py` — scalanie YAML-i do `observations/`
- [ ] Wykrywanie duplikatów i konfliktów między obserwacjami
- [ ] Zachowanie pochodzenia każdej obserwacji

### task/07-idiom-curator

- [ ] Agent `idiom-curator` — kategoryzacja i ranking obserwacji
- [ ] Falsyfikowalność jako warunek awansu
- [ ] Wynik jako propozycja do przeglądu autorskiego, nie gotowy `idioms/`

### task/08-idioms-0.1

- [ ] Przegląd autorski propozycji kuratora
- [ ] `idioms/` w wersji 0.1, każda reguła z uzasadnieniem
- [ ] `VERSION` biblioteki niezależny od wersji narzędzia

## Etap 1B — szkielet, który chodzi (tor B)

Skończone, gdy jedno realne zagadnienie fizyczne przechodzi całą drogę od opisu do
sklejonego materiału, a wszystkie trzy bramki działają.

### task/09-struktura-repozytorium

- [ ] Katalogi `package/` i `tooling/`
- [ ] Test zakazujący importów z `tooling/` do `package/`
- [ ] `pyproject.toml`, środowisko przez `uv`
- [ ] Bramki techniczne: `ruff check`, `ruff format --check`, `mypy`, `pytest`
- [ ] GitHub Actions uruchamiające te bramki

### task/10-config-default

- [ ] `config.default.yaml` z pełnym zestawem kluczy
- [ ] Modele, bramki, limity prób, limity czasu, wierność szkicu
- [ ] Przydział modeli wyłącznie jako konfiguracja, nic zaszytego w kodzie

### task/11-skill-plan

**Bramka 1.**

- [ ] Skill `plan` — samo-grill wg stałej listy kategorii
- [ ] Ekstrakcja parametrów z pochodzeniem
- [ ] Interpretacja szkicu wg poziomu wierności z konfiguracji
- [ ] Wynik: `plan.md`

### task/12-storyboard

- [ ] Generator `storyboard.yaml` z `plan.md`
- [ ] Wersjonowanie i archiwum poprzednich wersji
- [ ] Hook `storyboard_integrity.py` — rozdział sekcji `generated` i `state`

### task/13-scene-coder

- [ ] Agent `scene-coder` — jedna klasa `Scene` z nazwanymi sekcjami na blok
- [ ] Czytanie `idioms/` — punkt spotkania torów A i B
- [ ] Pusty `idioms/` nie blokuje działania

### task/14-check-scene-contract

- [ ] Hook `check_scene_contract.py` — parsowanie pliku
- [ ] Obecność klasy w storyboardzie
- [ ] Nazwane sekcje zgodne ze storyboardem
- [ ] Bez renderu i bez wywołania modelu

### task/15-render-klatki

**Bramka 2.**

- [ ] Render klatki statycznej
- [ ] `contact_sheet.py` — siatka klatek do przeglądu

### task/16-visual-judge

- [ ] Agent `visual-judge` — ocena klatek względem `plan.md`
- [ ] Wynik jako konkretne poprawki, nie ogólna ocena
- [ ] Rozdzielenie błędów technicznych od decyzji intencjonalnych
- [ ] Sufit prób i limit czasu na blok

### task/17-render-sekcji

- [ ] Render sekcji z `skip_animations`
- [ ] `sections.py` — parser indeksu JSON sekcji

### task/18-build

**Bramka 3.**

- [ ] `build.py` — orkiestracja całego przebiegu
- [ ] Sklejanie klas przez ffmpeg
- [ ] Status każdego kroku zapisywany do pliku, nie trzymany w kontekście rozmowy
- [ ] Przebieg końcowy na jednym realnym zagadnieniu fizycznym

## Etap 2 — egzekwowanie i próbki

Skończone, gdy złamanie reguły z biblioteki jest wychwytywane automatycznie przy zapisie
pliku, a użytkownik może wskazać konkretny moment materiału jednym identyfikatorem.

### task/19-lint-rules

- [ ] `lint-rules.yaml` — reguły z `idioms/` przełożone na sprawdzenia
- [ ] Podpięcie pod `check_scene_contract.py`
- [ ] Test: każda reguła ma przykład łamiący i przykład przechodzący

### task/20-skill-probe

- [ ] Skill `probe` — izolowana brudna scena na jedno pytanie stylistyczne
- [ ] Wynik `probe` może zasilić obserwacje toru A

### task/21-znaczniki-sekcji

- [ ] Znaczniki `blok.sekcja` wypalane w rogu renderów roboczych
- [ ] Znikają w renderze finalnym

## Etap 3 — pamięć i personalizacja

Skończone, gdy dziesiąty projekt tego samego użytkownika startuje z jego tempem
i kolejnością tłumaczenia bez powtarzania ustawień.

### task/22-skill-profile

- [ ] Skill `profile` — ankieta plus presety typów filmu
- [ ] Bez wymagania pisania prozy przez użytkownika
- [ ] Wynik: `~/.manim-claude/narration-profile.md`

### task/23-lessons

- [ ] `lessons.yaml` — preferencje zbierane na bramkach
- [ ] Obowiązują globalnie, z możliwością wyjątku projektowego

### task/24-idioms-local

- [ ] `idioms-local.yaml` — własne reguły użytkownika, czytane po rdzeniowych
- [ ] Twarda zasada: preferencje użytkownika nigdy nie awansują do idiomów rdzeniowych

## Etapy dalsze

Numeracja zadań rusza dalej, gdy etap 1B jest zamknięty. Zakres wg `roadmap.md`:

- **Etap 4 — ManimGL.** Drugi agent kodujący, zakres ograniczony do jednego pliku agenta.
  Warunek wejścia: etapy 1A i 1B zamknięte, co najmniej trzy materiały na ManimCE.
- **Etap 5 — Blender.** Przeniesienie kształtu procesu, nie kodu.
  Warunek wejścia: proces na Manimie udowodniony w praktyce.
- **Etap końcowy — dystrybucja.** Bootstrap środowiska, degradacja bez LaTeX-a, instalacja.

## Do rozstrzygnięcia poza gałęziami

Decyzje, które nie są zadaniami inżynierskimi. Pełny opis w `roadmap.md`, rozdział 7.

- [ ] Nazwa produktu — przybija do Manima, a w planie jest Blender
- [ ] Limit liczby idiomów rdzeniowych — wartość po pierwszej kuracji
- [ ] Licencja produktu — rekomendacja: CC BY-NC-SA 4.0 na materiały, osobna na kod
- [x] Gdzie mieszka repozytorium — `github.com/sjcmdev/manim-claude`

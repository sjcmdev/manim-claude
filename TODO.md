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
- Numer zadania to kolejność wykonania **w obrębie toru**. Tory A i B (patrz
  `roadmap.md`) są z założenia niezależne i idą równolegle, więc numery nie ustawiają
  kolejności między torami: zadanie 09 może być robione przed 04. Wyjątek: etap 0
  wyprzedza wszystko, bo zadanie 02 blokuje pobranie czegokolwiek.
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
- [x] Katalog roboczy na materiał referencyjny poza repozytorium, wpis w `.gitignore`
- [ ] Test hooka: próba zapisu fragmentu kodu źródłowego 3b1b jest odrzucana
- [ ] Rejestracja hooka w konfiguracji Claude Code

## Etap 1A — pierwsza biblioteka idiomów (tor A)

Skończone, gdy `idioms/` zawiera zestaw reguł falsyfikowalnych z uzasadnieniem,
a `VERSION` wynosi 0.1.

### task/03-fetch-reference

- [x] `fetch_reference.py` — wideo, napisy z czasami i metadane, katalog na film
- [x] `extract_frames.py` — klatki kluczowe przez detekcję cięć w ffmpegu plus siatki
- [x] `make_packet.py` — `packet.md` na film: metryczka, prompt, indeks klatek, transkrypcja
- [x] Zapis do katalogu roboczego poza repozytorium, wymuszony maszynowo
- [x] Lista źródeł z `3b1b-playlists.txt` jako wejście
- [ ] Kalibracja `--threshold` na pierwszej serii; wartość domyślna 0.35 jest zgadywana
- [ ] Decyzja, czy pobierać całe wideo (`design-spec.md` 9.3 mówi, że nie — patrz niżej)

### task/04-code-miner

- [x] Agent `code-miner` — `mine_code.py`, analiza kodu w klonie poza repozytorium
- [x] Zakres poszerzony poza plan: całość 2016–2026, bo starsze serie okazały się nośne
- [x] Warstwa wzorców projektowych i architektonicznych, nie tylko idiomy powierzchniowe
- [x] Wynik jako YAML obserwacji — `observations/code/`, 324 reguły z 21 serii
- [x] Drugi przebieg tym samym skryptem, inny prompt — `observations/animation/`, 491 reguł
- [x] Trzeci przebieg na bibliotekach społecznościowych — `observations/recipes/`, 85 technik
- [x] Syntezy w dwóch niezależnych przebiegach plus porównania — `observations/synthesis/`
- [ ] Domknięcie rozbieżności między syntezami; wymaga sesji z autorem

### task/05-porzadek-repo

Wykonane po task/04, żeby repozytorium dało się pokazać osobie dołączającej
do projektu.

- [x] Katalog `research/` na analizy poboczne, ze spisem treści
- [x] `README.md` opisujący stan faktyczny: co jest, czego nie ma, mapa repozytorium
- [x] `observations/README.md` — pochodzenie korpusu, schemat YAML, numeracja syntez
- [x] Odhaczenie w `TODO.md` tego, co faktycznie zrobione
- [x] `/local/` w `.gitignore` — katalog na pliki robocze poza gitem

### task/06-analiza-narracji

- [x] Prompt wg szablonu z `design-spec.md`, rozdział 9.4 — `prompt_template.md`
- [x] Transkrypcje plus siatki klatek jako wejście dla zewnętrznego czatu
- [x] Sztywny format odpowiedzi YAML; odpowiedź ląduje jako `observations.yaml` przy filmie
- [ ] Przejście pierwszego filmu przez czat i weryfikacja, czy prompt daje sprawdzalne reguły
- [ ] Zakres obejmuje starsze klasyki, ale wyłącznie budowę wyjaśnienia

### task/07-merge-observations

- [ ] `merge_observations.py` — scalanie YAML-i do `observations/`
- [ ] Wykrywanie duplikatów i konfliktów między obserwacjami
- [ ] Zachowanie pochodzenia każdej obserwacji

### task/08-idiom-curator

- [ ] Agent `idiom-curator` — kategoryzacja i ranking obserwacji
- [ ] Falsyfikowalność jako warunek awansu
- [ ] Wynik jako propozycja do przeglądu autorskiego, nie gotowy `idioms/`

### task/09-idioms-0.1

- [ ] Przegląd autorski propozycji kuratora
- [ ] `idioms/` w wersji 0.1, każda reguła z uzasadnieniem
- [ ] `VERSION` biblioteki niezależny od wersji narzędzia

## Etap 1B — szkielet, który chodzi (tor B)

Skończone, gdy jedno realne zagadnienie fizyczne przechodzi całą drogę od opisu do
sklejonego materiału, a wszystkie trzy bramki działają.

### task/10-struktura-repozytorium

- [ ] Katalogi `package/` i `tooling/`
- [ ] Test zakazujący importów z `tooling/` do `package/`
- [ ] `pyproject.toml`, środowisko przez `uv`
- [ ] Bramki techniczne: `ruff check`, `ruff format --check`, `mypy`, `pytest`
- [ ] GitHub Actions uruchamiające te bramki

### task/11-config-default

- [ ] `config.default.yaml` z pełnym zestawem kluczy
- [ ] Modele, bramki, limity prób, limity czasu, wierność szkicu
- [ ] Przydział modeli wyłącznie jako konfiguracja, nic zaszytego w kodzie

### task/12-skill-plan

**Bramka 1.**

- [ ] Skill `plan` — samo-grill wg stałej listy kategorii
- [ ] Ekstrakcja parametrów z pochodzeniem
- [ ] Interpretacja szkicu wg poziomu wierności z konfiguracji
- [ ] Wynik: `plan.md`

### task/13-storyboard

- [ ] Generator `storyboard.yaml` z `plan.md`
- [ ] Wersjonowanie i archiwum poprzednich wersji
- [ ] Hook `storyboard_integrity.py` — rozdział sekcji `generated` i `state`

### task/14-scene-coder

- [ ] Agent `scene-coder` — jedna klasa `Scene` z nazwanymi sekcjami na blok
- [ ] Czytanie `idioms/` — punkt spotkania torów A i B
- [ ] Pusty `idioms/` nie blokuje działania

### task/15-check-scene-contract

- [ ] Hook `check_scene_contract.py` — parsowanie pliku
- [ ] Obecność klasy w storyboardzie
- [ ] Nazwane sekcje zgodne ze storyboardem
- [ ] Bez renderu i bez wywołania modelu

### task/16-render-klatki

**Bramka 2.**

- [ ] Render klatki statycznej
- [ ] `contact_sheet.py` — siatka klatek do przeglądu

### task/17-visual-judge

- [ ] Agent `visual-judge` — ocena klatek względem `plan.md`
- [ ] Wynik jako konkretne poprawki, nie ogólna ocena
- [ ] Rozdzielenie błędów technicznych od decyzji intencjonalnych
- [ ] Sufit prób i limit czasu na blok

### task/18-render-sekcji

- [ ] Render sekcji z `skip_animations`
- [ ] `sections.py` — parser indeksu JSON sekcji

### task/19-build

**Bramka 3.**

- [ ] `build.py` — orkiestracja całego przebiegu
- [ ] Sklejanie klas przez ffmpeg
- [ ] Status każdego kroku zapisywany do pliku, nie trzymany w kontekście rozmowy
- [ ] Przebieg końcowy na jednym realnym zagadnieniu fizycznym

## Etap 2 — egzekwowanie i próbki

Skończone, gdy złamanie reguły z biblioteki jest wychwytywane automatycznie przy zapisie
pliku, a użytkownik może wskazać konkretny moment materiału jednym identyfikatorem.

### task/20-lint-rules

- [ ] `lint-rules.yaml` — reguły z `idioms/` przełożone na sprawdzenia
- [ ] Podpięcie pod `check_scene_contract.py`
- [ ] Test: każda reguła ma przykład łamiący i przykład przechodzący

### task/21-skill-probe

- [ ] Skill `probe` — izolowana brudna scena na jedno pytanie stylistyczne
- [ ] Wynik `probe` może zasilić obserwacje toru A

### task/22-znaczniki-sekcji

- [ ] Znaczniki `blok.sekcja` wypalane w rogu renderów roboczych
- [ ] Znikają w renderze finalnym

## Etap 3 — pamięć i personalizacja

Skończone, gdy dziesiąty projekt tego samego użytkownika startuje z jego tempem
i kolejnością tłumaczenia bez powtarzania ustawień.

### task/23-skill-profile

- [ ] Skill `profile` — ankieta plus presety typów filmu
- [ ] Bez wymagania pisania prozy przez użytkownika
- [ ] Wynik: `~/.manim-claude/narration-profile.md`

### task/24-lessons

- [ ] `lessons.yaml` — preferencje zbierane na bramkach
- [ ] Obowiązują globalnie, z możliwością wyjątku projektowego

### task/25-idioms-local

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
- [ ] `design-spec.md` 9.3 mówi, że pełne wideo nie jest pobierane; skrypty pobierają je,
      bo wideo trafia ręcznie do zewnętrznego czatu. Do poprawienia w specyfikacji
- [ ] Limit liczby idiomów rdzeniowych — wartość po pierwszej kuracji
- [ ] Licencja produktu — rekomendacja: CC BY-NC-SA 4.0 na materiały, osobna na kod
- [x] Gdzie mieszka repozytorium — `github.com/sjcmdev/manim-claude`

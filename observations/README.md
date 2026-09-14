# observations

Korpus obserwacji wydobytych maszynowo z cudzego kodu Manima oraz syntezy zrobione
na tym korpusie. To materiał wejściowy dla przyszłej biblioteki idiomów (`idioms/`),
a nie sama biblioteka: obserwacja staje się idiomem dopiero po przeglądzie autorskim.

Materiał źródłowy nie leży w tym repozytorium. Kod 3b1b jest na licencji CC BY-NC-SA,
więc klon i wyniki pośrednie trzymamy w katalogu roboczym poza drzewem projektu
(`~/manim-claude-reference`, patrz `tooling/reference/common.py`). Tutaj trafiają
wyłącznie reguły plus odwołania do plików i linii.

## Skąd to pochodzi

Jeden przebieg minera to jeden katalog tematyczny źródła i jeden plik wynikowy.
Analizy różnią się wyłącznie promptem — ten sam skrypt `tooling/reference/mine_code.py`
obsługuje wszystkie trzy, przez `--prompt` i `--out`.

| podkatalog | prompt | źródło | pliki | reguły |
|---|---|---|---|---|
| `code/` | `code_miner_prompt.md` | klon `3b1b/videos`, katalogi tematyczne od 2016 do 2026 | 21 | 324 |
| `animation/` | `animation_miner_prompt.md` | jak wyżej, plus trzy biblioteki społecznościowe | 24 | 491 |
| `recipes/` | `recipe_miner_prompt.md` | gisty i repozytoria autorów: `abul4fia`, `mf_tools`, `uwezi` | 3 | 85 |

`code/` odpowiada na pytanie „jak ten kod jest zorganizowany" — dekompozycja scen,
ponowne użycie, gdzie mieszka stan. `animation/` odpowiada na pytanie „jak ta animacja
jest zrobiona" — updatery, tempo, kamera, kompozycja kadru. `recipes/` to gotowe
techniki opisane od strony problemu, który rozwiązują, a nie od strony kodu.

Nazwa pliku to identyfikator materiału źródłowego: `_2023-clt.yaml` pochodzi
z `_2023/clt/` w klonie, `mf_tools.yaml` z biblioteki o tej nazwie.

## Schemat

`code/` i `animation/` mają wspólny schemat. Lista pod kluczem `observations:`,
każdy wpis:

```yaml
- id: stan-w-setup            # slug, unikalny w całym korpusie
  topic: stan-i-updatery      # kategoria tematyczna
  rule: "..."                 # reguła w trybie rozkazującym, jedno zdanie
  falsifiable: true           # czy da się wskazać kod, który ją łamie
  evidence:                   # co najmniej jedno odwołanie
    - {source: _2023/clt, file: dice_sims.py, line: 21}
  confidence: high            # high | medium | low
  applies_to: "Stosuj, gdy..."  # warunek stosowalności, nie powtórzenie reguły
```

`recipes/` ma schemat własny, bo opisuje technikę, nie regułę. Lista pod kluczem
`techniques:`, pola: `nazwa`, `problem` (co boli bez tej techniki), `zamiast`
(co ta technika wypiera), `kiedy` (warunek sięgnięcia po nią), `dotyczy_bolaczki`
(kategoria problemu), `zrodlo` (plik i linia), `przenosnosc` (wysoka, średnia, niska).

Kanoniczne tematy obserwacji kodu to: `dekompozycja`, `ponowne-uzycie`,
`stan-i-updatery`, `kompozycja`, `dane-a-obraz`, `czas-i-tempo` i `anty-wzorce`.
Obserwacje animacji używają: `stan-i-updatery`, `klasy-animacji`,
`wejscie-i-sprzatanie` i `custom-mobject`. Dla recipes kanoniczne bolączki to:
`ponowne-uzycie`, `pokretla-czasowe`, `iteracja-bez-renderu`,
`przeksztalcanie-wzorow`, `relacje-wielkosci`, `przekazywanie-parametrow`,
`reset`, `buff` i `szybkosc-vs-dlugosc`; `null` oznacza brak przypisanej kategorii.

Dowód wskazuje pojedynczą linię przez `line` albo jawny zakres przez
`line_start` i `line_end`. Każdy identyfikator musi być niepusty i globalnie
unikalny, również pomiędzy podkatalogami korpusu.

## Manifesty i walidacja

Każdy YAML ma odpowiadający mu manifest JSON pod `manifests/`, z odwzorowaniem
podkatalogu danych, na przykład `code/_2023-clt.yaml` ma manifest
`manifests/code/_2023-clt.json`. Manifest zapisuje typ dokumentu, pochodzenie,
parametry przebiegu oraz SHA-256 YAML-a i promptu. Historyczne dane mają status
`legacy-unverified`, a nieznane metadane są zapisane jako `null` zamiast
odgadywane.

Pełny korpus sprawdza komenda:

```console
uv run --with pyyaml python tooling/reference/validate_observations.py
```

Walidator agreguje błędy składni, schematu, taksonomii, identyfikatorów i
manifestów. Miner najpierw tworzy YAML i manifest w katalogu tymczasowym,
waliduje parę, a dopiero potem publikuje oba pliki w katalogu wynikowym.

Warunkiem awansu obserwacji do biblioteki idiomów jest `falsifiable: true`.
Reguła, której nie da się złamać, nie niesie informacji.

## Syntezy

`synthesis/` zawiera streszczenia korpusu zrobione przez agenta. Każdy przebieg
syntezy puszczany jest **dwa razy niezależnie**, na osobnych sesjach, bez wglądu
w wynik tego drugiego. Dwa przebiegi noszą nazwy **terra** i **sol** — nie znaczą
nic poza „pierwszy" i „drugi", służą wyłącznie rozróżnieniu. Zgodność dwóch
niezależnych przebiegów jest przesłanką, że reguła siedzi w materiale, a nie
w sposobie zadania pytania.

Numeracja plików: dziesiątki oznaczają etap, jedności wariant przebiegu.

| plik | co zawiera |
|---|---|
| `11-codex-terra.md`, `12-codex-sol.md` | dwie niezależne syntezy korpusu `code/` — konstrukcja i organizacja scen |
| `20-porownanie.md` | porównanie 11 z 12: zgodne, rozbieżne, sprzeczne |
| `31-anim-terra.md`, `31-anim-sol.md` | dwie niezależne syntezy korpusu `animation/` |
| `40-porownanie-animacje.md` | porównanie obu syntez animacyjnych |

Prompt syntezy: `tooling/reference/synthesis_prompt.md`.

## Przegląd autorski

`autor-grill.md` to zapis rozmów, w których autor projektu konfrontuje wydobyte
reguły z własną praktyką: co potwierdza, co odrzuca, gdzie miner zobaczył wzorzec,
którego nie ma. Korpus jest maszynowy i bez tej konfrontacji nie ma prawa awansować
do `idioms/`.

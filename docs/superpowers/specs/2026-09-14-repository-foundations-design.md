# Fundamenty repozytorium: Git, licencje, bramki lokalne i korpus

**Data:** 2026-09-14  
**Status:** zatwierdzony projekt przed planem implementacji

## Cel

Przygotować repozytorium do bezpiecznego rozwijania pierwszego pionowego
wycinka systemu Manim Claude. Zakres obejmuje uporządkowanie gałęzi `dev` i
PR-a Adama Krzysztopy, jawne licencjonowanie, lokalną ochronę przed kopiowaniem
kodu 3Blue1Brown, powtarzalne bramki techniczne oraz walidowany korpus z
manifestami pochodzenia.

Repozytorium pozostaje na tym etapie repozytorium badawczo-projektowym. Ten
zakres nie implementuje jeszcze generatora animacji ani Toru B.

## Zakres

Prace zostaną wykonane kolejno na trzech małych gałęziach:

1. `task/02-hook-licencyjny`
2. `task/10-bramki-techniczne`
3. `task/07-corpus-validator`

Każda gałąź powstanie z aktualnego `dev`, przejdzie testy i przegląd, a dopiero
potem zostanie zintegrowana. Przed rozpoczęciem prac aktualny lokalny `dev`
zostanie wypchnięty do `origin/dev`. Po wypchnięciu trzeba potwierdzić, że PR #1
Adama Krzysztopy jest widoczny w GitHub jako scalony, a jego commit należy do
historii `dev`.

Poza zakresem pozostają:

- GitHub Actions, zdalne CI i reguły ochrony gałęzi zależne od CI;
- implementacja generatora animacji i Toru B;
- rekonstrukcja nieznanych metadanych historycznego korpusu;
- automatyczna publikacja pakietu lub dokumentacji.

## Licencjonowanie

Kod repozytorium będzie udostępniony na licencji MIT w pliku `LICENSE`.
Dokumentacja, materiały badawcze, korpus obserwacji i przyszłe idiomy będą
objęte licencją CC BY-NC-SA 4.0 opisaną w `LICENSE-CONTENT.md`.

Pliki licencyjne mają jednoznacznie opisywać granicę obu zakresów. Dokumentacja
repozytorium ma odsyłać do obu licencji. Dane i materiały pochodzące ze źródeł
zewnętrznych zachowują prawa swoich właścicieli; licencja projektu obejmuje
jedynie oryginalny dobór, opis i opracowanie wykonane w tym repozytorium.

## Lokalna ochrona przed kopiowaniem kodu 3Blue1Brown

Repozytorium otrzyma konfigurację Claude Code w `.claude/settings.json` oraz
hook `tooling/hooks/no_3b1b_code.py`. Hook będzie sprawdzać treść proponowanych
zapisów przed ich wykonaniem.

Katalog referencyjny będzie wskazywany zmienną
`MANIM_CLAUDE_REFERENCE_ROOT`, a bez niej zgodnie z istniejącym narzędziem jako
`~/manim-claude-reference`. Konfiguracja repozytorium nie będzie zawierać
ścieżki właściwej dla jednego komputera.

Ochrona obejmuje dwa rodzaje naruszeń:

1. podobieństwo do indeksu odcisków kodu z lokalnego klonu 3Blue1Brown;
2. próby dodania materiałów binarnych lub medialnych skopiowanych ze źródła.

Indeks będzie generowany lokalnie i nie będzie zawierał pełnego kodu źródłowego.
Dla kodu zapisze odciski znormalizowanych okien tokenów, a dla plików binarnych
sumy SHA-256. Domyślnie blokowane będzie dopasowanie co najmniej 50 znaczących
tokenów; importy i standardowy boilerplate nie będą samodzielnie powodować
blokady. Do repozytorium trafi jedynie skrypt budujący indeks oraz opis
procedury. Sam indeks pozostanie artefaktem lokalnym ignorowanym przez Git.

Hook `PreToolUse` dla operacji zapisu i edycji będzie sprawdzać nową treść
tekstową. Ten sam skrypt w trybie skanowania repozytorium sprawdzi pliki
tekstowe oraz dokładne hashe nowych plików binarnych i medialnych; tryb ten
zostanie włączony do lokalnej bramki technicznej.

Zachowanie hooka:

- brak lokalnego klonu 3Blue1Brown pozwala kontynuować zwykłą pracę;
- obecny klon bez gotowego indeksu blokuje chroniony zapis i podaje komendę
  naprawczą;
- wykryte podobieństwo lub zabronione medium blokuje zapis i wskazuje przyczynę;
- błąd wewnętrzny hooka przy obecnym klonie jest traktowany jako błąd ochrony,
  nie jako ciche zezwolenie.

Hook nie zastępuje przeglądu prawnego ani przeglądu kodu. Jego rolą jest
praktyczne egzekwowanie przyjętej zasady: uczymy się ze źródeł, ale nie kopiujemy
ich implementacji ani zasobów.

## Lokalne bramki techniczne

Projekt otrzyma `pyproject.toml`, deklarację Python `>=3.11` i konfigurację dla:

- `ruff` — formatowanie i lint;
- `mypy` — kontrola typów;
- `pytest` — testy;
- walidatora korpusu.

Środowisko i zależności będą zarządzane przez `uv`. Komenda
`uv run python tooling/check.py` uruchomi kolejno format-check, lint, typowanie,
testy, skan licencyjny i walidację korpusu. Zatrzyma się z kodem różnym od zera,
jeżeli którakolwiek bramka zawiedzie, ale pokaże komendę oraz wynik wadliwego
etapu. Ten lokalny punkt wejścia będzie w przyszłości możliwy do podpięcia do CI
bez zmiany kontraktu deweloperskiego. W tym zakresie nie powstanie żaden
workflow GitHub Actions.

Konfiguracja ma obejmować istniejące skrypty i testy. Zaostrzenie reguł nie może
prowadzić do szerokich, niezwiązanych refaktoryzacji; poprawiamy tylko problemy
potrzebne do przejścia uzgodnionych bramek.

## Kontrakt korpusu

Walidator `tooling/reference/validate_observations.py` będzie obsługiwać trzy
jawnie rozdzielone rodzaje dokumentów:

- obserwacje kodu;
- obserwacje animacji;
- recipes.

Dla każdego rodzaju zostaną zdefiniowane wymagane pola, typy i dozwolone
wartości. Walidacja obejmie co najmniej:

- poprawność składni YAML;
- niepuste identyfikatory i ich globalną unikalność;
- wymagane pola i właściwe typy;
- dozwolone poziomy `confidence`;
- logiczną wartość `falsifiable` w obserwacjach;
- strukturę dowodów, w tym numery linii albo znaczniki czasu zależnie od typu;
- zgodność tematów z jedną kanoniczną taksonomią;
- istnienie i zgodność manifestu odpowiadającego plikowi danych.

Recipes mają własny kontrakt i nie muszą posiadać pól charakterystycznych dla
obserwacji. Raport walidatora będzie podawać plik, ścieżkę pola oraz zrozumiały
opis każdego błędu. Proces zakończy się kodem różnym od zera, jeżeli wystąpi
choć jeden błąd.

## Naprawa obecnych danych

Istniejący korpus zostanie doprowadzony do kontraktu bez zmiany jego znaczenia:

- niecytowana wartość zawierająca dwukropek w `_2022-puzzles.yaml` zostanie
  poprawiona;
- powtarzające się identyfikatory otrzymają stabilny prefiks wynikający ze
  źródłowego pliku; identyfikatory już unikalne pozostaną bez zmian;
- zakresy linii zostaną zapisane jawnie jako `line_start` i `line_end`, a
  pojedyncza linia jako `line`;
- warianty tematów zostaną zmapowane do kanonicznych nazw, przykładowo
  `updatery` do `stan-i-updatery`.

Zmiany mechaniczne muszą być możliwe do przejrzenia w diffie. Walidator ma
najpierw otrzymać testy odtwarzające obecne klasy błędów, a dopiero potem dane
zostaną naprawione.

## Manifesty pochodzenia

Manifesty będą osobnymi plikami JSON w `observations/manifests/`, po jednym dla
każdego pliku YAML w `observations/code`, `observations/animation` i
`observations/recipes`. Układ katalogów zostanie odwzorowany: przykładowo
`observations/code/_2022-puzzles.yaml` otrzyma manifest
`observations/manifests/code/_2022-puzzles.json`. Dzięki temu pliki o tej samej
nazwie w różnych częściach korpusu nie będą kolidować.

Manifest będzie zawierać:

- wersję schematu manifestu;
- względną ścieżkę pliku danych;
- typ dokumentu;
- ścieżkę źródła i jego rewizję Git, jeśli są znane;
- ścieżkę promptu i SHA-256 jego treści;
- użyty model i poziom effort, jeśli są znane;
- czas wygenerowania w UTC;
- SHA-256 pliku YAML;
- status pochodzenia.

Dla obecnego korpusu status będzie miał wartość `legacy-unverified`. Nieznane
wartości będą zapisane jawnie jako `null`; nie wolno ich odgadywać. Nowe wyniki
wydobycia otrzymają status `generated` i kompletny zestaw metadanych dostępnych
w momencie uruchomienia.

`mine_code.py` zapisze kandydacki YAML i manifest do katalogu tymczasowego,
zweryfikuje parę, a dopiero potem przeniesie oba pliki do katalogu wynikowego.
Katalog wynikowy minera nie jest automatycznie traktowany jako zatwierdzony
korpus. Przekroczenie limitu czasu pojedynczego zadania zostanie zaraportowane,
katalog tymczasowy usunięty, a pozostałe zadania puli będą mogły się zakończyć.

## Przepływ danych

Nowy przebieg wydobycia będzie wyglądać następująco:

1. operator uruchamia miner dla wskazanego źródła i promptu;
2. miner zapisuje kandydacki YAML poza zatwierdzonym korpusem;
3. powstaje manifest z parametrami przebiegu i hashami;
4. kandydat przechodzi walidację składni i kontraktu;
5. dopiero poprawna para YAML–manifest może zostać włączona do korpusu;
6. lokalna bramka sprawdza cały korpus przed integracją gałęzi.

Hash w manifeście uniemożliwia niezauważoną zmianę danych bez aktualizacji
informacji o przebiegu. Walidator nie uznaje samego istnienia manifestu za
dowód jakości obserwacji; potwierdza jedynie spójność i udokumentowane
pochodzenie.

## Obsługa błędów

Narzędzia wiersza poleceń mają zwracać przewidywalne kody wyjścia i komunikaty
przeznaczone dla człowieka. Błędy jednego pliku korpusu będą agregowane, aby
użytkownik mógł poprawić kilka problemów w jednym przebiegu. Błędy infrastruktury
minera, takie jak timeout albo brak programu zależnego, zostaną odróżnione od
błędów jakości wygenerowanych danych.

Żaden błąd nie może pozostawić poprawnie wyglądającego, lecz niekompletnego
pliku w miejscu przeznaczonym na zaakceptowane wyniki.

## Strategia testów

Implementacja będzie prowadzona test-first. Testy obejmą:

- konfigurację i wywołanie hooka Claude Code;
- brak klonu, obecny klon bez indeksu, dopasowanie odcisku i niedozwolone media;
- poprawne dokumenty każdego z trzech rodzajów korpusu;
- błędny YAML, brakujące pola, złe typy, niepoprawne dowody i tematy;
- identyfikatory powtarzające się między plikami;
- brakujący, niezgodny i poprawny manifest;
- generowanie manifestu i zgodność hashy;
- timeout minera oraz brak pozostawionego pliku częściowego;
- uruchomienie pełnego istniejącego korpusu przez walidator.

Testy jednostkowe będą używać katalogów tymczasowych i małych fixture'ów.
Pełny korpus będzie osobnym testem integracyjnym. Przed integracją każdej gałęzi
zostaną uruchomione wszystkie lokalne bramki, nie tylko testy nowego modułu.

## Kryteria ukończenia

Zakres jest ukończony, gdy:

- `origin/dev` zawiera zaakceptowaną lokalną historię, a stan PR #1 został
  zweryfikowany;
- zakres obu licencji jest jednoznaczny i opisany w repozytorium;
- hook blokuje zdefiniowane naruszenia i zachowuje się fail-closed przy obecnym
  klonie bez indeksu;
- projekt można odtworzyć przez `uv` i sprawdzić jedną lokalną komendą;
- nie istnieje workflow GitHub Actions dodany przez ten zakres;
- cały korpus parsuje się i przechodzi kontrakt;
- wszystkie pliki korpusu mają zgodne manifesty;
- timeout minera nie przerywa pozostałych zadań ani nie pozostawia częściowych
  wyników;
- pełny zestaw lokalnych bramek kończy się powodzeniem.

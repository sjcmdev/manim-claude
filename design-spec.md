# manim-claude — projekt systemu

Data: 2026-09-02
Status: spec do zatwierdzenia
Źródło decyzji: wywiad z autorem projektu

## 1. Cel

Narzędzie, które zamienia opis słowny, materiały wykładowe (PDF, Markdown, prezentacje)
i odręczny szkic w dobrą animację Manim, z weryfikacją wizualną i bramkami akceptacji.

Rdzeniem wartości jest **autorska biblioteka idiomów i wzorców projektowania animacji**
oraz agenty piszące kod, które z niej korzystają. Pipeline produkcyjny jest opakowaniem
tej biblioteki, nie odwrotnie.

Projekt jest niezależny od repozytoriów kursu `University-Of-Physics`. Nie korzysta z
`course-state.json`, nie podlega polityce kodowania Part I i nie obowiązuje go zakaz
auto-renderowania obowiązujący w repozytoriach kursu.

## 2. Odbiorcy

1. Wykładowca bez umiejętności technicznych, wspierany przez studenta znającego podstawy
   Claude Code. Wrzuca własne notatki i slajdy, dostaje animację w swojej kolejności
   tłumaczenia.
2. Autor projektu — produkcja materiału do kursu Manim i do własnych wykładów.

Produkt jest niekomercyjny.

## 3. Zakres

W zakresie:

- Manim Community Edition (>= 0.21), Python >= 3.14.
- Wejście: prompt tekstowy, dokumenty, szkice rastrowe, profil narracji użytkownika.
- Weryfikacja przez render: klatka statyczna, sekcje, pełny podgląd.
- Biblioteka idiomów wersjonowana niezależnie od kodu narzędzia.

Poza zakresem w tej wersji:

- ManimGL (faza 4), Blender (faza 5).
- Weryfikacja fizyki. Źródłem prawdy dla wzorów, stałych i modeli jest użytkownik.
  System nigdy nie zmienia po cichu podanego wzoru; gdy go nie rozumie, pyta.
- Instalatory i bootstrap środowiska (osobne zadanie na koniec).

## 4. Decyzje

Zapis rozstrzygnięć wraz z uzasadnieniem, żeby nie były renegocjowane bez powodu.

| # | Decyzja | Uzasadnienie |
|---|---|---|
| D1 | Osobny produkt, osobne repozytorium `repos/manim-claude` | Inna publiczność, inna licencja, inny cykl życia niż kurs |
| D2 | Tylko Claude Code w v1; treści pisane jako czysty Markdown i skrypty Pythona | Drugi harness podwaja pracę, zanim wiadomo, czy produkt jest dobry; neutralny zapis czyni port tanim |
| D3 | Auto-render dozwolony | Zakaz dotyczył repozytoriów kursu; tutaj render jest jedynym sposobem sprawdzenia obrazu |
| D4 | Wiele klas `Scene`, sekcje wewnątrz klasy | Klasa to zamknięty blok rzeczy zależnych od siebie, renderowalny niezależnie i parametryzowalny; sekcje to kroki weryfikacji podczas budowy |
| D5 | `plan.md` czytelny dla człowieka, `storyboard.yaml` generowany z niego | Człowiek poprawia prozę, maszyna czyta strukturę |
| D6 | Nowa wersja `storyboard.yaml` przy każdej regeneracji, stara do archiwum | Niedestruktywność, możliwość powrotu |
| D7 | Hooki wykonują wyłącznie tanie, deterministyczne bramki; render jest jawnym krokiem skilla | Ocena renderu wymaga spojrzenia na obraz przez model z kontekstem, czego hook nie potrafi |
| D8 | Bramki blokujące: plan, statyczny layout, pełny podgląd. Statyczny layout domyślnie włączony | Większość nieporozumień widać na klatkach statycznych, zanim cokolwiek zostanie zanimowane |
| D9 | Parametry z pochodzeniem (`source: user / document / assumed / probe`) w `plan.md` | Pozwala przejrzeć wyłącznie to, co system zgadł |
| D10 | Prawdą fizyczną jest użytkownik | Brak weryfikacji symbolicznej i biblioteki zweryfikowanych modeli, mniejszy zakres |
| D11 | Idiomy rdzeniowe są autorskie: z mielenia 3b1b oraz z niezależnego osądu autorów | Biblioteka jest kuratorowana, nie zbierana automatycznie |
| D12 | Feedback użytkownika trafia do `lessons`, nigdy do idiomów rdzeniowych | Preferencja osobista to nie reguła sztuki |
| D13 | Zero kodu z `3b1b/videos` w drzewie projektu; wynikiem mielenia jest wyłącznie własna proza | Repozytorium jest na CC BY-NC-SA 4.0, a klauzula share-alike zaraziłaby produkt, gdyby powstało dzieło zależne |
| D14 | `package/` i `tooling/` rozdzielone; `package/` nie importuje z `tooling/` | Narzędzia deweloperskie nigdy nie trafiają do użytkownika |
| D15 | Biblioteka idiomów wersjonowana niezależnie, paczka deklaruje zgodną wersję | Idiomy będą się zmieniać szybciej niż kod |
| D16 | Przydział modeli w konfiguracji, nic nie zaszyte w kodzie | Koszt i jakość są decyzją operatora |
| D17 | Profil narracji na poziomie użytkownika, budowany ankietą i presetami | Styl tłumaczenia nie zmienia się między tematami, a użytkownik nie ma pisać prozy |
| D18 | Domyślna wierność szkicu zależy od typu źródła | Figura z książki i szybki szkic na tablecie niosą różną ilość informacji |

## 5. Architektura

### 5.1 Dwa tory

**Tor A — biblioteka (rdzeń produktu).** Nie zależy od pipeline'u.

```text
kod 3b1b + transkrypcje + klatki  ->  observations/  ->  curate  ->  idioms/ + reguly lintu
```

**Tor B — harness produkcyjny.** Działa z pustym idiom-bookiem, po prostu gorzej.

```text
wejscie  ->  plan.md  ->  storyboard.yaml  ->  build (na blok)  ->  assemble  ->  podglad
```

Tory spotykają się w agencie `scene-coder`, który czyta `idioms/`.

### 5.2 Przepływ toru B

```text
wejscie: prompt + dokumenty + szkice + narration-profile + lessons
  |
  |-- [skill plan] samo-grill wg stalej listy kategorii
  |      -> plan.md: narracja, bloki, obiekty, params z pochodzeniem, topologia ze szkicu
  |      BRAMKA 1 (blokujaca): uzytkownik czyta i poprawia plan.md
  |
  |-- [skrypt storyboard] plan.md -> storyboard.yaml (nowa wersja, stara do archiwum)
  |
  |-- [skill build] petla po blokach:
  |      [agent scene-coder]   klasa Scene + nazwane sekcje
  |      [hook]                tanie bramki: import, klasa w storyboard, nazwy sekcji, lint idiomow
  |      [skrypt]              render jednej klatki statycznej
  |      [agent visual-judge]  porownanie klatki z planem, konkretne poprawki
  |      BRAMKA 2 (blokujaca, domyslnie wl.): kontaktowka klatek statycznych wszystkich blokow
  |      [skrypt]              render sekcji (skip_animations dla poprzednich)
  |      [agent visual-judge]  ocena, max N iteracji wg config
  |
  |-- [skrypt assemble] --save_sections + ffmpeg concat miedzy klasami
  |
  |-- BRAMKA 3 (blokujaca): pelny podglad, znaczniki `blok.sekcja` wypalone w rogu
  |
  |-- [skill review] pytanie z wyborami -> observations/ (dev) + lessons.yaml (uzytkownik)
```

Bramki 1, 2 i 3 blokują. Wszystko pomiędzy nimi wykonuje się bez pytania, z sufitem prób
z `config.yaml`.

### 5.3 Mechanizm sekcji

Manim CE udostępnia `self.next_section(name=..., skip_animations=...)` od wersji 0.12 oraz
flagę `--save_sections`, która produkuje osobny plik wideo na sekcję plus JSON z indeksem
(nazwa, plik, długość). `skip_animations=True` wykonuje kod bez renderowania klatek, dzięki
czemu stan sceny narasta poprawnie, a renderowana jest tylko sekcja badana.

Konsekwencje:

- sklejanie wewnątrz jednej klasy jest darmowe,
- ffmpeg jest potrzebny wyłącznie do sklejenia wielu klas,
- JSON sekcji jest naturalnym źródłem znaczników `blok.sekcja` dla feedbacku.

## 6. Układ repozytorium

```text
manim-claude/
  package/                     # instalowane u uzytkownika
    skills/      plan  build  probe  review  profile  assemble
    agents/      scene-coder  visual-judge
    hooks/       check_scene_contract.py  storyboard_integrity.py
    scripts/     build.py  sections.py  contact_sheet.py  archive_storyboard.py
    presets/     typy filmow
    config.default.yaml
  idioms/                      # wersjonowane niezaleznie (D15)
    VERSION
    kompozycja.md  czas-i-tempo.md  stan-i-updatery.md  czytelnosc.md  anty-wzorce.md
    lint-rules.yaml
  tooling/                     # nigdy nie trafia do paczki
    skills/      mine  curate
    agents/      code-miner  narrative-miner  idiom-curator
    hooks/       no_3b1b_code.py
    scripts/     fetch_reference.py  merge_observations.py
  observations/                # surowe, dev-only
  workbench/                   # projekty testowe autorow
  docs/specs/
```

Reguła egzekwowana testem: żaden moduł w `package/` nie importuje niczego z `tooling/`.

## 7. Artefakty

| plik | zakres | zapisuje | czyta |
|---|---|---|---|
| `plan.md` | projekt | skill `plan`, poprawia użytkownik | wszyscy |
| `storyboard.yaml` | projekt | skrypt na podstawie `plan.md` | skille, hooki, skrypty |
| `storyboard/archive/*.yaml` | projekt | skrypt | człowiek, gdy wraca do starszej wersji |
| `probes/` | projekt | skill `probe` | `visual-judge` |
| `observations/*.yaml` | narzędzie | minerzy, kuratorzy | `curate` |
| `idioms/*.md`, `lint-rules.yaml` | zasób wersjonowany | autorzy | `scene-coder`, hook lintu |
| `~/.manim-claude/lessons.yaml` | użytkownik | skill `review` | `plan`, `scene-coder` |
| `~/.manim-claude/idioms-local.yaml` | użytkownik | użytkownik | `scene-coder`, po idiomach rdzeniowych |
| `~/.manim-claude/narration-profile.md` | użytkownik | skill `profile` | `plan` |
| `config.yaml` | narzędzie plus nadpisanie w projekcie | użytkownik | wszyscy |

### 7.1 `plan.md`

Sekcje: cel dydaktyczny, narracja (kolejność wyjaśniania), bloki (jeden na klasę `Scene`),
obiekty i relacje, topologia ze szkicu, tabela parametrów, otwarte założenia do odrzucenia.

Tabela parametrów niesie pochodzenie:

```yaml
params:
  omega:   {value: 2.0,     unit: rad/s, source: user,     status: confirmed}
  hbar:    {value: 1.0,     unit: "-",   source: assumed,  status: needs-review, note: "jednostki naturalne"}
  x_range: {value: [-4, 4], unit: m,     source: document, ref: "notatki.pdf s.7", status: needs-review}
```

Wszystko o statusie `needs-review` jest treścią bramki 2.

### 7.2 `storyboard.yaml`

Dwie rozdzielne sekcje: `generated` (nadpisywana przy regeneracji) i `state` (statusy,
ścieżki renderów, znaczniki akceptacji — zachowywana). Hook pilnuje, by nikt nie mieszał
jednej z drugą. Każdy blok ma `class`, `sections`, `depends_on`, `params` oraz `status`
w cyklu `draft -> layout-ok -> rendered -> approved`.

### 7.3 `config.default.yaml`

```yaml
models:
  planner:       opus
  scene_coder:   sonnet
  visual_judge:  opus
  code_miner:    sonnet
  idiom_curator: sonnet
  escalation:    opus

gates:
  plan:          on
  static_layout: on
  full_preview:  on

retries:
  technical:           3
  technical_in_loop:   5
  per_block_timeout_s: 600

loop: true

sketch_fidelity:
  book_figure:   strict
  slide:         layout
  tablet_sketch: topology
  verbal_only:   loose

idioms:
  required_version: ">=0.1,<0.2"
```

### 7.4 Poziomy wierności szkicu

| poziom | co jest wiążące |
|---|---|
| `loose` | tylko lista obiektów |
| `topology` | relacje: co obok, nad, pod czym, co się czego dotyka, co większe |
| `layout` | dodatkowo proporcje i podział kadru |
| `strict` | pozycje odczytane ze szkicu, minimalna korekta czytelności |

Kadr Manima ma proporcje inne niż kartka, więc `strict` zawsze wymaga skalowania do kadru.
"Ściśle" nigdy nie znaczy "identycznie".

## 8. Inwentarz komponentów

### 8.1 Skille w paczce

| skill | rola |
|---|---|
| `profile` | ankieta plus presety typów filmu, jednorazowo na użytkownika; wynik: `narration-profile.md` |
| `plan` | czyta wejście, przeprowadza samo-grill wg stałej listy kategorii, wyciąga parametry z pochodzeniem, interpretuje szkic wg poziomu wierności; wynik: `plan.md` |
| `build` | pętla po blokach: kodowanie, tanie bramki, klatka statyczna, ocena, sekcje, ocena |
| `probe` | izolowana brudna scena rozstrzygająca jedno pytanie stylistyczne; wniosek trafia do `params` i `lessons` |
| `assemble` | sekcje plus ffmpeg do pełnego podglądu |
| `review` | bramka 3: pytanie z wyborami, pozycje `blok.sekcja` plus aspekt plus werdykt; wynik do `lessons` i `observations` |

Samo-grill w skillu `plan` ma stałą listę kategorii: kadr i skala, co statyczne a co
dynamiczne, co steruje czasem, jednostki i zakresy, kolejność pojawiania się, tekst i wzory,
tempo, co widz ma zrozumieć. Agent wypełnia je z materiału samodzielnie i pyta wyłącznie
o pola, których nie da się wywnioskować; resztę wypisuje jako jawne założenia do odrzucenia
jednym słowem.

### 8.2 Skille deweloperskie

| skill | rola |
|---|---|
| `mine` | orkiestracja mielenia: kod lokalnie przez subagentów, transkrypcje i klatki do zewnętrznego czatu |
| `curate` | kategoryzacja i ranking obserwacji, przygotowanie przeglądu dla autora |

### 8.3 Agenci

| agent | domyślny model | zakres widzenia |
|---|---|---|
| `scene-coder` | sonnet | storyboard bloku, idiomy, parametry; nic więcej |
| `visual-judge` | opus | klatki plus opis bloku z planu; zwraca konkretne poprawki |
| `code-miner` | sonnet | pliki źródłowe w katalogu tymczasowym; wynik: obserwacje |
| `narrative-miner` | sonnet | transkrypcje i klatki; wynik: obserwacje |
| `idiom-curator` | sonnet | obserwacje; wynik: kategorie i ranking |
| `manimgl-coder` | — | faza 4 |

### 8.4 Hooki

| hook | zdarzenie | zakres | działanie |
|---|---|---|---|
| `check_scene_contract.py` | PostToolUse, zapis `scenes/*.py` | package | parsowanie, obecność klasy w storyboardzie, nazwane sekcje, podzbiór lintu idiomów |
| `storyboard_integrity.py` | PreToolUse, zapis `storyboard.yaml` | package | wymusza wersjonowanie i archiwum, blokuje ręczną edycję sekcji generowanej |
| `no_3b1b_code.py` | PreToolUse, zapis | tooling | blokuje wprowadzenie do drzewa treści pochodzącej z `3b1b/videos` |

Wszystkie hooki są tanie i deterministyczne. Żaden hook nie renderuje.

### 8.5 Skrypty bez modelu

`build.py` (orkiestracja renderów i ffmpeg), `sections.py` (parser JSON sekcji),
`contact_sheet.py` (siatka klatek), `archive_storyboard.py`,
`fetch_reference.py` (yt-dlp: napisy z czasami; ffmpeg: klatki kluczowe),
`merge_observations.py`.

## 9. Mielenie materiału referencyjnego

### 9.1 Ograniczenie prawne

`3b1b/videos` jest na CC BY-NC-SA 4.0. Produkt jest niekomercyjny, więc klauzula
NonCommercial nie blokuje korzystania, ale klauzula ShareAlike zaraziłaby projekt, gdyby
powstało dzieło zależne. Dlatego:

- żaden plik ani fragment kodu z tego repozytorium nie trafia do drzewa projektu,
- analiza odbywa się w katalogu tymczasowym poza repozytorium,
- wynikiem jest wyłącznie własna proza opisująca zaobserwowane regularności,
- pochodzenie inspiracji jest wskazane w dokumentacji wraz z opisem wartości dodanej.

Hook `no_3b1b_code.py` egzekwuje pierwszy punkt maszynowo.

### 9.2 Zakres

Wzorce kodu: serie z roku 2022 i późniejsze — splot i rozkład Gaussa oraz CLT, optyka
(w tym seria Optics Puzzles), hologramy, transformata Laplace'a, obliczenia kwantowe,
równania Maxwella.

Wzorce narracyjne: również starsze klasyki — algebra liniowa, rachunek różniczkowo-całkowy,
równania różniczkowe, transformata Fouriera — ale wyłącznie na poziomie budowy wyjaśnienia,
bez analizy kodu. Styl kodowania autora ewoluował i stare pliki uczyłyby nawyków, których
on sam już nie stosuje.

Repozytorium ma około 190 MB, więc mielenie kodu wykonują subagenci zapisujący wynik do
plików. Do rozmowy głównej wraca jedna strona ustaleń na subagenta.

Punkt startowy: repozytorium zawiera własny plik `CLAUDE.md` z konwencjami spisanymi przez
autora. Służy jako szkielet hipotez, weryfikowany następnie na próbce kodu. Hipotezy
przepisujemy własnymi słowami.

Analiza obejmuje również warstwę wzorców projektowych i architektonicznych, nie tylko
idiomy powierzchniowe.

### 9.3 Materiał wideo

Do analizy narracji i tempa pobierane są wyłącznie napisy z czasami
(`yt-dlp --write-auto-sub --skip-download`) oraz klatki kluczowe wyciągane ffmpeg-iem co
ustalony interwał. Pełne pliki wideo nie są potrzebne i nie są pobierane.

Artefakty zostają w katalogu roboczym mielenia, dzięki czemu ten sam prompt można powtórzyć
później i otrzymać porównywalny wynik.

### 9.4 Format wymiany z zewnętrznym czatem

Zewnętrzny czat otrzymuje transkrypcję z czasami plus siatkę klatek i zwraca sztywny YAML,
scalany skryptem. Proza nie jest akceptowana, ponieważ czyniłaby człowieka parserem.

Szablon promptu:

```text
Analizujesz fragment filmu edukacyjnego pod katem WZORCOW PROJEKTOWANIA ANIMACJI.
Materialy: transkrypcja z czasami oraz siatka klatek co N sekund.

Nie streszczaj tresci. Nie opisuj fizyki ani matematyki.
Interesuja mnie wylacznie powtarzalne decyzje autora dotyczace:
  - kompozycji kadru i hierarchii uwagi
  - czasu: tempa, pauz, kolejnosci pojawiania sie elementow
  - czytelnosci: kolor, kontrast, rozmiar, podpisy
  - budowy wyjasnienia: od czego zaczyna, kiedy wprowadza formalizm

Zwroc WYLACZNIE YAML w ponizszym schemacie, bez komentarza przed ani po.
Kazda regula musi byc FALSYFIKOWALNA: da sie spojrzec na animacje i orzec,
czy regula jest zlamana, czy nie. Reguly niesprawdzalne pomijaj.

observations:
  - id: <krotki-slug>
    topic: kompozycja | czas-i-tempo | czytelnosc | narracja
    rule: <jedno zdanie w trybie rozkazujacym>
    falsifiable: true | false
    evidence:
      - {source: <identyfikator materialu>, timestamp: "MM:SS"}
    confidence: high | medium | low
    applies_to: <kiedy regula obowiazuje, jedno zdanie>
```

### 9.5 Kategoryzacja i przegląd

Wszystkie obserwacje trafiają do `observations/` bez filtra wstępnego. Model o roli
`idiom_curator` grupuje je w kategorie (kompozycja, czas i tempo, stan i updatery,
czytelność, anty-wzorce) i szereguje według własnej oceny jakości wzorca w połączeniu
z powtarzalnością w niezależnych źródłach. Autor przegląda listę od góry.

Pole `falsifiable` nie służy do sortowania, ale jest wymagane, ponieważ tylko reguły
sprawdzalne mogą później zasilić lint w hooku.

Awans obserwacji do `idioms/` wymaga jawnej decyzji autora.

## 10. Błędy i eskalacja

Klasyfikacja błędu renderu:

- **techniczny** — błąd API, brak LaTeX-a, przekroczenie czasu, błąd składni. Naprawia agent;
  po wyczerpaniu `retries.technical` następuje eskalacja do modelu z pola `models.escalation`;
  dopiero potem pytanie do użytkownika.
- **intencjonalny** — pusta scena, zła kompozycja, "nie o to chodziło". Trafia do użytkownika
  natychmiast, bez eskalacji, ponieważ żaden model nie odgadnie intencji.

Tryb `loop` podnosi limit prób, nigdy nie zmienia klasyfikacji i nie znosi sufitu. Obowiązuje
twardy limit czasu na blok (`per_block_timeout_s`), ponieważ updater bez warunku stopu potrafi
renderować bez końca.

Brak LaTeX-a w systemie degraduje generowanie do `Text` z unicode zamiast `Tex` i `MathTex`,
zamiast przerywać pracę.

## 11. Fazowanie

| faza | zawartość |
|---|---|
| 1A | Tor A: `mine`, `code-miner`, `narrative-miner`, `curate`, pierwsze `idioms/` |
| 1B | Tor B: `plan`, storyboard, `build`, bramka statyczna, `assemble` — równolegle z 1A |
| 2 | `lint-rules.yaml` w hooku, `probe`, znaczniki w renderach roboczych |
| 3 | `profile`, presety, `lessons`, `idioms-local` |
| 4 | ManimGL jako drugi agent kodujący |
| 5 | Blender: przeniesienie kształtu procesu, nie kodu |
| — | Instalacja i bootstrap środowiska: na końcu |

Tory 1A i 1B są niezależne i mogą powstawać równolegle. Tor B powinien wcześnie mieć jeden
działający blok jako poligon do weryfikowania reguł z toru A.

## 12. Ryzyka

| ryzyko | przeciwdziałanie |
|---|---|
| Zaśmiecenie biblioteki idiomów regułami bez wartości | Dwa poziomy (`observations` i `idioms`), awans wyłącznie decyzją autora, wymóg falsyfikowalności |
| Zarażenie licencją ShareAlike | D13 plus hook `no_3b1b_code.py` plus zakaz przechowywania materiału w drzewie |
| Wyciek narzędzi deweloperskich do paczki | D14 plus test zakazujący importów z `tooling/` |
| Koszt tokenów przy mieleniu 190 MB | Subagenci piszący do plików; do rozmowy głównej wraca strona ustaleń |
| Pętla kosmetycznych poprawek renderu | Sufit prób w konfiguracji, limit czasu na blok, klasyfikacja błędów |
| Rozjazd `plan.md` i `storyboard.yaml` | Rozdział `generated` i `state`, wersjonowanie z archiwum, hook integralności |

## 13. Kwestie otwarte

1. Nazwa jest utylitarna i przybija produkt do Manima. Blender będzie wymagał albo zmiany
   nazwy, albo osobnego opakowania nad wspólnym rdzeniem.
2. Docelowy limit liczby idiomów rdzeniowych nie został ustalony. Postulat: limit ma istnieć,
   wartość do ustalenia po pierwszej kuracji.
3. Workspace `CLAUDE.md` wymaga dopisania piątego obszaru, gdy projekt ruszy.
4. Repozytorium nie zostało zainicjowane w gicie ani opublikowane zdalnie.
5. Licencja produktu do formalnego wyboru. Rekomendacja: CC BY-NC-SA 4.0 dla materiałów
   (zgodna z pochodzeniem inspiracji i z niekomercyjnym charakterem), osobna licencja
   dla kodu narzędzia.

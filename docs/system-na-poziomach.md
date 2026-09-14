# manim-claude na różnych poziomach szczegółowości

**Status:** mapa orientacyjna, 2026-09-14. Nie wprowadza nowych decyzji — porządkuje to,
co już jest w `design-spec.md`, `docs/pipeline-komponenty.md`, `docs/otwarte-pytania.md`
i `research/`. Czytaj od góry; każdy poziom przybliża poprzedni. Zatrzymaj się na tym,
który wystarcza.

Oznaczenia statusu w całym dokumencie:

- **[jest]** — działa w repozytorium,
- **[spec]** — ustalone w `design-spec.md`, jeszcze nie zbudowane,
- **[propozycja]** — w `docs/`, czeka na decyzję,
- **[pomysł]** — w `research/`, niewiążące.

---

## Poziom 0 — jedno zdanie

Wykładowca opisuje zjawisko fizyczne, a system pomaga mu zrobić z tego animację
w stylu dobrych filmów matematycznych, pytając go tylko w trzech momentach.

---

## Poziom 1 — widok użytkownika

```text
   co wkładam                         co dostaję
   ──────────                         ──────────
   opis zagadnienia        ┌──────┐   plan wyjaśnienia do poprawienia     (bramka 1)
   notatki, PDF, szkice ──►│system│──►kontaktówka klatek do akceptacji    (bramka 2)
   (później: wideo)        └──────┘   film z podglądem blok.sekcja        (bramka 3)
```

- Użytkownik **nie pisze kodu ani YAML-a**. Poprawia prozę (`plan.md`) i wybiera z opcji.
- Między bramkami system pracuje sam, z limitem prób.
- Fizyka jest prawdą użytkownika. System dba o formę, nie ustala treści merytorycznej.

---

## Poziom 2 — dwie maszyny i jedno źródło wiedzy

To jest poziom, na którym najłatwiej się zgubić, bo w repozytorium siedzą **dwie różne
rzeczy**, które łączy tylko biblioteka idiomów.

```text
 TOR A — FABRYKA WIEDZY (tooling/, tylko dla autorów)        TOR B — PRODUKT (package/, u użytkownika)
 ─────────────────────────────────────────────────────        ─────────────────────────────────────────
 kod 3b1b, filmy, biblioteki społecznościowe                  opis zagadnienia od użytkownika
            │                                                              │
            ▼                                                              ▼
   miner → observations/  [jest]                                   plan → storyboard
            │                                                              │
            ▼                                                              ▼
   kurator + autor → idioms/  [spec] ─────── czyta ──────────►    scene-coder → render → ocena
                                                                           │
                                                                           ▼
                                                                         film
```

- **Tor A** działa rzadko, na maszynie autora, na cudzym materiale. Wynik: reguły.
- **Tor B** działa przy każdym filmie, u użytkownika. Wynik: film.
- **Punkt styku: `idioms/`.** Tor B działa także z pustą biblioteką, tylko gorzej.
- Materiał źródłowy toru A (CC BY-NC-SA) nigdy nie trafia do repozytorium ani do paczki.
  Pilnuje tego hook `no_3b1b_code.py` **[jest]**.

---

## Poziom 3 — tor B krok po kroku

Każdy krok ma: kto go wykonuje, co czyta, co zapisuje.

| # | krok | wykonawca | czyta | zapisuje | status |
|---|---|---|---|---|---|
| 1 | zrozumienie zagadnienia, samo-grill | skill `plan` | opis, dokumenty, szkice | `plan.md` | [spec] |
| — | **BRAMKA 1**: użytkownik poprawia plan | człowiek | `plan.md` | `plan: approved` | [spec] |
| 2 | rozpisanie planu na bloki i sekcje | skrypt `storyboard.py` | `plan.md` | `storyboard.yaml` | [spec] |
| 3 | kod jednej sceny na blok | agent `scene-coder` | blok storyboardu, `idioms/` | `scenes/<blok>.py` | [spec] |
| 4 | tanie sprawdzenie kodu | hook `check_scene_contract.py` | plik sceny, storyboard | blokada albo OK | [spec] |
| 5 | klatka statyczna | skrypt `render.py --frame` | scena | PNG | [spec] |
| 6 | sprawdzenia mechaniczne | skrypt `layout_checks.py` | klatka / geometria | lista problemów | [propozycja] |
| 7 | ocena obrazu | agent `visual-judge` | klatka, plan bloku, wynik kroku 6 | lista poprawek | [spec] |
| — | **BRAMKA 2**: kontaktówka wszystkich bloków | człowiek | siatka klatek | `layout: approved` | [spec] |
| 8 | render sekcji | skrypt `render.py --section` | scena, flaga approved | wideo sekcji | [spec] |
| 9 | złożenie filmu | skrypt `assemble.py` (ffmpeg) | sekcje | podgląd | [spec → skrypt wg propozycji] |
| — | **BRAMKA 3**: przegląd filmu | skill `review` + człowiek | podgląd ze znacznikami | `lessons.yaml` | [spec] |

Pętla 3 → 7 powtarza się do limitu prób z `config.yaml`. Całą pętlą steruje skill `build`.

---

## Poziom 4 — tor A krok po kroku

| # | krok | wykonawca | wynik | status |
|---|---|---|---|---|
| 1 | pobranie materiału (wideo, napisy, klatki) | skrypty `fetch_reference.py`, `extract_frames.py`, `make_packet.py` | pakiet na film, poza repo | [jest] |
| 2 | analiza kodu 3b1b | `mine_code.py` + Codex | YAML obserwacji + manifest | [jest] |
| 3 | analiza narracji filmu | pakiet → zewnętrzny czat | YAML obserwacji z czasem | [jest narzędzie, 0 przebiegów] |
| 4 | walidacja | `validate_observations.py` | korpus spójny z manifestami | [jest] |
| 5 | scalanie, duplikaty, konflikty | `merge_observations.py` | jeden korpus | [spec] |
| 6 | kategoryzacja i ranking | agent `idiom-curator` | propozycja reguł | [spec] |
| 7 | decyzja autorska | autor | `idioms/` 0.1 + `lint-rules.yaml` | [spec] |

Stan dziś: **900 obserwacji** (324 kod, 491 animacja, 85 technik), zwalidowane, z manifestami
`legacy-unverified`. Kroki 5–7 nie istnieją.

---

## Poziom 5 — z czego system jest zbudowany (rodzaje komponentów)

Każdy element jest jednym z czterech rodzajów. Wybór według pierwszego pasującego pytania:

| rodzaj | kiedy | przykłady |
|---|---|---|
| **hook** | tanie, deterministyczne, ma zablokować zapis | `no_3b1b_code.py`, `check_scene_contract.py`, `storyboard_integrity.py` |
| **skrypt** | deterministyczne, może być ciężkie (render, ffmpeg) | `render.py`, `assemble.py`, `validate_observations.py` |
| **skill** | rozmowa z użytkownikiem albo orkestracja | `plan`, `build`, `review`, `probe`, `profile` |
| **agent** | potrzebny wąski, świeży kontekst | `scene-coder`, `visual-judge`, `idiom-curator` |

Dwie zasady, które trzymają całość:

1. **Akceptacja to flaga w pliku**, którą skrypt czyta i bez której odmawia. Model niczego
   „nie pamięta”.
2. **Skrypt mierzy, zanim model oceni.**

Szczegóły: `docs/pipeline-komponenty.md`.

---

## Poziom 6 — pliki, które krążą w systemie

| plik | kto pisze | kto czyta | rola | status |
|---|---|---|---|---|
| `plan.md` | skill `plan`, poprawia użytkownik | wszyscy | **co i w jakiej kolejności wyjaśniamy** | [spec] |
| `storyboard.yaml` | skrypt z `plan.md` | skille, agenty, hooki, skrypty | **jak to pokazujemy**: bloki, sekcje, parametry, backend, stan akceptacji | [spec] |
| `scenes/*.py` | `scene-coder` | hook, render | implementacja | [spec] |
| `config.yaml` | użytkownik | wszyscy | modele, limity, progi | [spec] |
| `idioms/*.md`, `lint-rules.yaml` | autorzy | `scene-coder`, hook lintu | reguły stylu | [spec] |
| `observations/**/*.yaml` + `manifests/` | minery | walidator, kurator | surowiec dla idiomów | [jest] |
| `~/.manim-claude/lessons.yaml` | skill `review` | `plan`, `scene-coder` | preferencje użytkownika | [spec, etap 3] |
| `~/.manim-claude/narration-profile.md` | skill `profile` | `plan` | sposób prowadzenia narracji | [spec, etap 3] |
| `inputs.yaml` | użytkownik / `plan` | `plan`, skrypty | wejścia z rolami | [propozycja] |
| `edits/*.yaml` | skill, zatwierdza użytkownik | `assemble.py` | lista montażowa innego filmu | [propozycja] |

---

## Poziom 7 — słownik: które pojęcie z research to który plik u nas

Dużo zamieszania bierze się stąd, że `research/` używa innych nazw na **te same role**.
Większość „nowych formatów” to po prostu przyszłe, bogatsze wersje plików, które już są
w specu.

| pojęcie z `research/` | odpowiednik w specu | różnica | kiedy |
|---|---|---|---|
| `ExplanationSpec` | `plan.md` | research chce jawnych ruchów wyjaśnienia, nieporozumień, intuicji z granicami | pole po polu, gdy `plan.md` okaże się za ubogi |
| `AnimationSpec` / IR | `storyboard.yaml` | research chce intencji wizualnej niezależnej od backendu (`expose_structure`, `morph`) zamiast wprost klas Manima | razem z Blenderem (etap 5); do tego czasu zostawić miejsce na pole `intent` |
| Visual Explanation Pattern Atlas | `idioms/` | idiom = reguła stylu; atlas = wzorzec „problem poznawczy → strategia wizualna → implementacja” | po `idioms/` 0.1; decyzja w `otwarte-pytania.md` pyt. 6 |
| Pedagogy Pattern Atlas, `ExplanationMove` | `narration-profile.md` + lista kategorii samo-grilla w `plan` | research chce ontologii ruchów wydobywanej automatycznie | pomysł; osobny tor badawczy |
| `CognitiveRepairAtlas`, `learning_episode.yaml` | `lessons.yaml` | lessons = preferencje z bramek; atlas = zapis naprawianych nieporozumień z rozmów | pomysł; wymaga decyzji o prywatności |
| `Visual Director` | brak (ukryte w `plan` → `storyboard.py`) | nazwana rola wybierająca strategię wizualną | do decyzji |
| `Compiler Agent` | `scene-coder` | ta sama rola | — |
| `Critic / QA` | `visual-judge` + `layout_checks.py` | ta sama rola | — |
| `blender/*` capabilities | brak | pakiety wiedzy per domena | etap 5 |

**Reguła porządkująca:** nowy pomysł nie tworzy nowego pliku, dopóki nie da się wskazać,
którego istniejącego pliku rolę rozszerza i dlaczego ten plik nie wystarcza.

---

## Poziom 8 — horyzonty: co kiedy

```text
TERAZ (zrobione)     fundamenty: licencje, hook licencyjny, bramki lokalne, walidator korpusu
                     korpus 900 obserwacji
        │
MVP1 [propozycja]    tor B: jedno zagadnienie do filmu, tylko Manim 2D, jeden film
                     tor A: 5 idiomów z parą scen, egzekwowanych lintem
        │
ETAP 2               lint z biblioteki, probe, znaczniki blok.sekcja
ETAP 3               profile, lessons, idioms-local — personalizacja
ETAP 4               ManimGL
ETAP 5               Blender: AnimationSpec z intencją, blender/* capabilities, kamera 3D
        │
BADANIA (równolegle, niewiążące)
                     analiza wideo na GPU · wielopoziomowa analiza 3b1b
                     model wyjaśnienia (pedagogika) · historia rozmów
                     manim-slides, wiele wejść, montaż wielu filmów
```

Jeśli pomysł nie mieści się w MVP1, jego miejsce jest w `research/` albo
w `otwarte-pytania.md` — nie w kodzie.

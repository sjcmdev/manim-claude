# Otwarte pytania projektowe

**Status:** lista robocza, 2026-09-14. Każde pytanie ma opcje i rekomendację wyjściową
do zakwestionowania. Rozstrzygnięcie trafia do `decision-log.md`, a pytanie zostaje tu
oznaczone jako zamknięte z odnośnikiem do decyzji.

Powiązane: `docs/pipeline-komponenty.md` (przydział hook / skrypt / skill / agent),
`research/manim_blender_agent_system_review.md` (przegląd narzędzi Blendera).

---

## 1. Jaki jest zakres MVP1?

**Problem.** Mamy trzy kierunki, które chcą być pierwsze: tor B (szkielet produkcyjny),
tor A (idiomy z korpusu) i nowe analizy (wideo GPU, pedagogika, historia rozmów).
Bez granicy MVP1 każdy z nich rośnie równolegle i żaden nie daje filmu.

**Opcje.**

| opcja | zakres | ryzyko |
|---|---|---|
| A. pionowy wycinek Manim | opis → `plan.md` → `storyboard.yaml` → jedna scena → klatka → ocena → sekcje → film; jedno realne zagadnienie | idiomy puste albo prowizoryczne |
| B. biblioteka najpierw | `idioms/` 0.1 z parami scen łamiąca/przechodząca, bez harnessu | reguły nieoperacyjne, nikt ich nie czyta |
| C. hybryda | A + 5 idiomów z parą scen, czytanych przez `scene-coder` i sprawdzanych lintem | większy zakres, ale jedyny wariant sprawdzający styk torów |

**Rekomendacja: C.** MVP1 kończy się, gdy jedno zagadnienie fizyczne przechodzi całą drogę
do pliku wideo, a 5 reguł z korpusu jest egzekwowanych automatycznie.

**Poza MVP1:** Blender, manim-slides, wiele wejść wideo, analiza GPU, pedagogika, historia
rozmów, personalizacja (`profile`, `lessons`), dystrybucja.

**Do ustalenia.**
- Które zagadnienie jest testem akceptacyjnym? (Kandydaci: oscylator harmoniczny
  w przestrzeni fazowej, pakiet falowy, precesja spinu w 2D.)
- Które 5 idiomów? Kryterium: mechaniczne, sprawdzalne lintem, potwierdzone w ≥ 3 seriach.
- Ile bramek akceptacji w MVP1: wszystkie trzy czy tylko bramka 1 i 3?
- Kto jest użytkownikiem testowym MVP1 — autor, czy wykładowca spoza projektu?

---

## 2. Kto decyduje, które narzędzie wykonuje zadanie?

**Problem.** Zadanie „pokaż X” może zrobić Manim, Blender, manim-slides, ffmpeg albo
matplotlib. Jeśli wybór zostanie w głowie agenta, będzie niepowtarzalny i nieaudytowalny.

**Opcje.**

| kto decyduje | jak | ocena |
|---|---|---|
| agent-router | osobny agent czyta blok i wybiera backend | niedeterministyczne, trudne do testowania; odrzucić w MVP |
| skill `plan` + użytkownik | skill proponuje `backend` per blok wg tabeli reguł, użytkownik zatwierdza na bramce 1 | jawne, zapisane w pliku, zgodne z D7 |
| skrypt wg reguł | deterministyczna tabela cech bloku → backend | tanie, ale nie obsłuży niejasnych przypadków |
| hook | — | hook nie decyduje, tylko **waliduje**: backend dostępny, pola kompletne, zakazane kombinacje |

**Rekomendacja.** Decyzja jest **polem w `storyboard.yaml`** (`block.backend`,
`project.outputs`), nigdy stanem rozmowy:

1. skill `plan` wypełnia pole wg jawnej tabeli reguł (np. wzory, wykresy, 2D → `manim`;
   bryły, pola objętościowe, cząsteczki, kryształy → `blender`; zdjęcia, nagrania → `footage`),
2. przypadki niejasne trafiają do listy „założeń do odrzucenia” na bramce 1,
3. skrypty i agenty wykonawcze czytają pole i **odmawiają**, gdy go brak,
4. hook `storyboard_integrity.py` sprawdza spójność pola z dostępnymi backendami.

**Do ustalenia.** Gdzie mieszka tabela reguł (config vs idiomy)? Czy scena hybrydowa
(Manim overlay na renderze Blendera) to jeden blok z dwoma backendami, czy dwa bloki?

---

## 3. Wiele wejść wideo, prezentacje manim-slides, osobne filmy, montaż

### 3a. Wiele wejść wideo

Wejście wideo ma różne **role**, i to rola decyduje, co się z nim dzieje:

| rola | przykład | przetwarzanie |
|---|---|---|
| `reference-style` | film 3b1b, dobrze poprowadzony wykład | analiza (GPU), wynik do `observations/`, nigdy do materiału |
| `content-source` | nagranie wykładu, z którego bierzemy treść | transkrypcja → wejście skilla `plan` |
| `footage` | nagranie eksperymentu wstawiane do filmu | blok `backend: footage`, cięcie i montaż |

**Rekomendacja.** Manifest wejść w projekcie (`inputs.yaml`: ścieżka, rola, licencja,
zakres czasu). Brak roli = błąd walidacji. Materiał `reference-style` podlega tej samej
zasadzie licencyjnej co 3b1b.

### 3b. Prezentacja przez manim-slides

manim-slides dzieli animację na slajdy przez `next_slide()` w klasie `Slide`. Nasz
storyboard już dzieli blok na nazwane sekcje (`next_section`). Wniosek: **sekcja
storyboardu jest naturalnym kandydatem na slajd**.

**Rekomendacja.** `project.outputs: [video, slides]`. `scene-coder` generuje jedną scenę;
skrypt wybiera wariant klasy bazowej (`Scene` vs `Slide`) i mapuje granice sekcji na
`next_slide()`. Bez osobnego agenta.

**Do ustalenia.** Czy każda sekcja to slajd, czy potrzebne jest pole `slide_break` w
sekcji? Czy slajdy mają inne tempo (pauzy zamiast czasu trwania)? Eksport HTML vs PPTX?

### 3c. Osobny film z tego samego materiału

Np. pełny wykład 20 min i skrót 3 min, albo wersja pionowa. **Rekomendacja:** bloki są
wspólne, film to **lista montażowa** (`edits/<nazwa>.yaml`: kolejność bloków i sekcji,
cięcia, format). Renderów nie dublujemy — skrypt składa z tych samych plików sekcji.

### 3d. Montaż: agent, skill, hook czy ffmpeg?

| czynność | rodzaj | uzasadnienie |
|---|---|---|
| sklejanie sekcji i bloków, przejścia, ścieżka audio, format | **skrypt `assemble.py` na ffmpeg** | deterministyczne; brak decyzji |
| wybór kolejności i cięć do skrótu | **skill** (propozycja listy montażowej, użytkownik zatwierdza) | decyzja narracyjna należy do użytkownika |
| sprawdzenie, że lista montażowa wskazuje istniejące sekcje | **hook** lub walidator | tanie, deterministyczne |
| osobny agent montażysty | **nie w MVP** | brak zadania, którego nie robi skrypt + skill |

**Do ustalenia.** Czy montaż obejmuje audio (lektor, muzyka)? To zmienia zakres ffmpeg
(miksowanie, normalizacja głośności, synchronizacja z sekcjami).

---

## 4. Których narzędzi Blendera potrzebujemy?

**Kontekst.** Blender jest etapem 5 w `roadmap.md`, po udowodnieniu procesu na Manimie.
Pytanie dotyczy więc wyboru na potem, ale wpływa na format `storyboard.yaml` już teraz.
Licencje i stan utrzymania poniżej są **do weryfikacji** przed jakąkolwiek decyzją.

| narzędzie | czym jest | rola u nas | rekomendacja |
|---|---|---|---|
| [ahujasid/blender-mcp](https://github.com/ahujasid/blender-mcp) | ogólny most model ↔ Blender (MCP) | **transport**: wykonanie poleceń w Blenderze, podgląd viewportu | kandydat na warstwę komunikacji; porównać z oficjalnym Blender Lab MCP (Blender 5.1+) |
| [3d-agent.com](https://3d-agent.com) | wieloagentowy system perceive → reason → act → verify dla Blendera | **wzorzec architektury**, nie zależność | przeczytać opis pętli weryfikacji obrazem; nie integrować |
| [westNeighbor/Blender_math_anim](https://github.com/westNeighbor/Blender_math_anim) | addon inspirowany Manimem: wykresy, ODE, funkcje zespolone, LaTeX/Typst, morphing | **backend matematyki 2.5D/3D** | najbliższy naszemu zakresowi; pierwszy do statycznej analizy jak 3b1b |
| [nortikin/sverchok](https://github.com/nortikin/sverchok) | parametryczne węzły (>600), pola, powierzchnie | **proceduralne instrumenty** (pola wektorowe, powierzchnie) | tylko jeśli Geometry Nodes nie wystarczą; duża zależność |
| [josemarinfarina/SciBlend-Core](https://github.com/josemarinfarina/SciBlend-Core) | wizualizacja naukowa: VTK, VDB, netCDF, dane zależne od czasu, kolormapy | **dane symulacyjne i objętościowe** | gdy materiał pochodzi z symulacji; nie w pierwszym kroku |
| [BradyAJohnston/MolecularNodes](https://github.com/BradyAJohnston/MolecularNodes) | struktury molekularne i trajektorie przez Geometry Nodes | **domena: cząsteczki** | pakiet domenowy na żądanie |
| [beautiful-atoms/beautiful-atoms](https://github.com/beautiful-atoms/beautiful-atoms) | atomy i kryształy z ASE / Pymatgen | **domena: ciało stałe, kryształy** | pakiet domenowy; istotny dla fizyki materiałowej |

**Rekomendacja wyjściowa.**
- Rdzeń: czysty `bpy` + Geometry Nodes + jedno narzędzie transportowe (MCP).
- Pierwszy backend matematyczny do zbadania: `Blender_math_anim`.
- Pakiety domenowe (`MolecularNodes`, `beautiful-atoms`, `SciBlend`) jako osobne
  „capabilities” włączane per projekt, nie jako zależności rdzenia.
- Nie wykonywać dowolnego Pythona od modelu jako ścieżki głównej: wysokopoziomowe,
  przetestowane funkcje, surowy `bpy` tylko jako wyjście awaryjne.

**Do ustalenia.**
- Licencje: addony Blendera są często GPL. Używanie jako zależności uruchomieniowej to co
  innego niż kopiowanie kodu do repozytorium na MIT — potrzebna reguła jak dla 3b1b.
- Minimalna wersja Blendera (część narzędzi wymaga 5.1+).
- Czy analizujemy te repozytoria minerem kodu, tak jak 3b1b?

---

## 5. Kamera w 3D: jak mieć pewność, że widać to, co trzeba?

**Problem.** W 2D kadr jest stały i sprawdzenie „czy obiekt jest w kadrze” jest proste.
W 3D obiekt może być poza kadrem, zasłonięty, zbyt mały, oglądany pod kątem, który ukrywa
właśnie tę cechę, którą narracja tłumaczy (np. degenerację poziomów).

**Proponowany mechanizm: kamera jako specyfikacja z weryfikowalnymi warunkami.**

1. **Deklaracja w storyboardzie, nie współrzędne.** Sekcja opisuje intencję kamery:
   ```yaml
   camera:
     subject: [ket_psi, bloch_sphere]   # co ma być widoczne
     move: orbit                        # słownik: hold, orbit, dolly, push-in, pan, track
     keep_visible: [ket_psi]            # przez cały ruch
     min_screen_fraction: 0.15          # minimalny udział w kadrze
     margin: 0.05                       # bezpieczny margines
     forbidden_views: [edge-on]         # kąty ukrywające cechę
   ```
2. **Ograniczony słownik ruchów** realizowany przez przetestowane skrypty (constraint
   Track To, orbita wokół pustego obiektu, ścieżka), nie przez dowolne klatki kluczowe
   od modelu.
3. **Sprawdzenia mechaniczne przed oceną modelu** (skrypt, bez renderu pełnego):
   - rzut prostopadłościanów ograniczających na współrzędne kamery w próbkowanych
     klatkach (w Blenderze `world_to_camera_view`) → czy w kadrze, z marginesem,
     jaki udział powierzchni;
   - zasłonięcie: promienie z kamery do punktów kontrolnych obiektu (`scene.ray_cast`),
     odsetek niezasłoniętych;
   - kąt widzenia względem osi cechy (np. normalna płaszczyzny, oś spinu).
4. **Podgląd tani przed drogim:** klatki kluczowe w niskiej rozdzielczości (Workbench /
   EEVEE), kontaktówka ruchu kamery, dopiero potem pełny render.
5. **`visual-judge` ocenia to, czego skrypt nie umie:** czytelność, czy ruch nie
   dezorientuje, czy widać zależność, którą narracja tłumaczy.

**W Manimie 3D** (`ThreeDScene`: `set_camera_orientation`, `move_camera`) ten sam
kontrakt: deklaracja w storyboardzie, słownik ruchów, próbkowane klatki i sprawdzenie
rzutu obiektów przed oceną wizualną.

**Do ustalenia.**
- Czy progi (`min_screen_fraction`, `margin`) idą do `config.default.yaml`, zgodnie z
  zasadą „próg w konfiguracji, reguła mówi o niezmienniku”?
- Czy korpus 3b1b ma sceny 3D wystarczające do wydobycia idiomów kamery?
- Jak często próbkować klatki ruchu (stała liczba vs co zmianę kierunku)?

---

## 6. Role agentów i pakiety umiejętności z przeglądu Blendera — przyjąć?

**Źródło.** `research/manim_blender_agent_system_review.md`, rozdziały 8–9. Propozycja:
3–4 role agentowe plus dużo deterministycznych skilli i narzędzi, zamiast wielu agentów
przekazujących sobie streszczenia.

### 6a. Role — zestawienie z obecnym projektem (`design-spec.md` 8, `docs/pipeline-komponenty.md`)

| propozycja z przeglądu | odpowiednik u nas | ocena |
|---|---|---|
| `Research/Pedagogy Director` — źródła, poprawność fizyczna, tok wyjaśnienia | skill `plan` | **skill, nie agent**: prowadzi bramkę 1 z użytkownikiem, więc musi działać w głównym kontekście. Poprawność fizyczna należy do użytkownika (fizyka to prawda użytkownika); director może ją sprawdzać, nie ustanawiać |
| `Visual Director` — problem poznawczy → visual beats, wzorce z Pattern Atlas | **brak**; dziś ukryte między `plan` a `storyboard.py` | **luka warta nazwania.** Kandydat: osobny krok skilla `plan` albo agent czytający `idioms/` i atlas; wynik = sekcje storyboardu z intencją wizualną |
| `Compiler Agent` — IR → Manim/Blender, dwa skille | agent `scene-coder` (później `manimgl-coder`, backend Blender) | zgodne; „dwa skille” = osobne pakiety wiedzy per backend, jeden kontrakt wejścia |
| `Critic / QA` — preview vs specyfikacja | agent `visual-judge` | zgodne, pod warunkiem że dostaje wynik sprawdzeń mechanicznych (`layout_checks.py`, kamera z pyt. 5) |

### 6b. Pakiety wiedzy (`*-skills`)

| pakiet | ocena |
|---|---|
| `manim-*` (API, styl, recipes, atlas 3b1b) | zgodne z torem A: `idioms/` + `observations/recipes` jako materiał skilla |
| `blender-*` (bpy, Geometry Nodes, receptury domenowe) | zgodne z rekomendacją z pyt. 4 |
| `physics-*` (QM, teoria grup, przestrzenie wektorowe) | **ostrożnie**: jako retrieval/instrukcje tak, jako autorytet merytoryczny nie; nowy zakres poza MVP1 |
| `export-*` (slides, PDF, wideo, miniatury) | **raczej skrypty, nie skille** (pyt. 3d): eksport jest deterministyczny; skill tylko tam, gdzie jest decyzja (np. wybór klatek do PDF) |

### 6c. Hooki — co z listy przeglądu naprawdę może być hookiem

D7: hooki wyłącznie tanie i deterministyczne, żaden hook nie renderuje.

| pozycja z przeglądu | rodzaj u nas |
|---|---|
| schema validation | **hook** (`storyboard_integrity.py`, walidator korpusu) |
| lint | **hook** (`check_scene_contract.py` + `lint-rules.yaml`) |
| SymPy / numeric checks | **hook**, jeśli < 1 s; inaczej skrypt w `build` |
| git snapshot | **hook** (tani) — do decyzji, czy potrzebny |
| render smoke test | **skrypt**, nie hook (render) |
| vision QA | **agent `visual-judge`**, nie hook (model + obraz) |

### 6d. Podział Blendera na capabilities

```text
przekrojowe (każdy projekt 3D):   blender/core   blender/camera   blender/material   blender/compositor
domenowe (włączane per projekt):  blender/math-geometry     → Blender_math_anim, Geometry Nodes, ew. Sverchok
                                  blender/scientific-fields → SciBlend
                                  blender/volume            → SciBlend (VDB), Geometry Nodes
                                  blender/crystal           → beautiful-atoms
                                  blender/molecule          → MolecularNodes
```

`blender/camera` realizuje kontrakt kamery z pytania 5 (słownik ruchów + sprawdzenia
widoczności).

**Rekomendacja.** Przyjąć ideę „mało agentów, dużo deterministycznych pakietów” — jest
zgodna z D7 i z przydziałem w `docs/pipeline-komponenty.md`. Nie przyjmować dosłownie:
director pedagogiczny to skill, eksport to skrypty, render i vision QA nie są hookami.
Jedyna nowość do decyzji to **Visual Director**.

**Do ustalenia.**
- Czy Visual Director wchodzi do MVP1, czy intencja wizualna zostaje polem wypełnianym
  przez `plan`?
- Czy „Pattern Atlas” (wzorce: problem poznawczy → strategia wizualna → implementacja)
  to przyszły format `idioms/`, czy osobny artefakt?
- Czy nazwy pakietów `manim-*` / `blender-*` / `physics-*` przyjmujemy jako konwencję
  katalogów w `package/skills/`?

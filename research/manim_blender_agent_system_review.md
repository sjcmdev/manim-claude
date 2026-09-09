Tak. Przejrzałem GitHuba, Blender DevTalk, Blender Artists i oficjalny katalog rozszerzeń Blendera. Stan na **9 września 2026** jest taki: **bardzo dużo potrzebnych Ci klocków już istnieje, ale nie znalazłem projektu, który spinałby cały pipeline, który opisujesz**.

Najbliższe projekty rozwiązują osobno trzy fragmenty problemu: agentowe sterowanie Blenderem, programistyczne animacje matematyczno-fizyczne w Blenderze oraz scientific visualization. Nie ma natomiast dojrzałego systemu:

> źródła naukowe → model pedagogiczny → scenariusz → semantyczny opis animacji → wybór Manim/Blender → generacja kodu → render → automatyczna analiza renderu → poprawki → film + slides + PDF

I właśnie **ta warstwa pośrednia i orkiestracja** wydaje mi się najciekawszą częścią Twojego pomysłu.

## 1. Najważniejsze rzeczy, które znalazłem

| Projekt | Czym jest | Co jest dla Ciebie interesujące |
|---|---|---|
| **Official Blender MCP Server** | Oficjalny Blender Lab MCP dla Blendera 5.1+ | Natural-language → Blender Python API. Model-agnostic, oficjalnie pokazują także lokalne/open-weight modele i llama.cpp. To powinien być kandydat na **warstwę komunikacyjną**, nie na mózg systemu. ([blender.org](https://www.blender.org/lab/mcp-server/?utm_source=chatgpt.com)) |
| **ahujasid/blender-mcp** | Bardzo popularny community MCP, Python, MIT | Ogólny most LLM ↔ Blender; obecnie ~27,8k stars. Dobry do studiowania protokołu i narzędzi, ale jest nastawiony na ogólne sterowanie Blenderem. |
| **Blender MCP Pro** | MCP z >100 wyspecjalizowanymi operacjami | Keyframes, interpolation, NLA, Geometry Nodes, shadery, kamery, modifiers. Świetny wzorzec **jak rozbić wielkie `execute_python()` na semantyczne tools**. ([blenderartists.org](https://blenderartists.org/t/blender-mcp-pro-100-tool-mcp-server-for-controlling-blender-from-ai-assistants/1633350?utm_source=chatgpt.com)) |
| **3D-Agent** | Multi-agentowy eksperyment opisany na Blender DevTalk | Prawdopodobnie **najbliższy architektonicznie temu, co chcesz zrobić**: perceive → reason → act → verify; Blender + Python + MCP + screenshot/VLM verification. ([devtalk.blender.org](https://devtalk.blender.org/t/3d-agent-blender-ai-assistant-built-a-multi-agent-system-on-top-of-blenders-mcp-and-python-api-and-sharing-architecture-learnings-for-the-lab-discussion/44260?utm_source=chatgpt.com)) |
| **Blender SuperSkill** | Gotowy **Codex skill** do Blendera | Ma `SKILL.md`, references, `blender_orchestrator.py`, `agents/openai.yaml`; używa trwałego stanu, ma build/repair/review loops. Bardzo dobry template pod Twój system. |
| **BlenderMathAnim** | Biblioteka animacji matematycznych oparta bezpośrednio na `bpy` | Blenderowy odpowiednik filozofii code-first: `.blend` nie tworzy się ręcznie; scena powstaje z Pythona. Repo ma własne obiekty, compositions, Geometry Nodes, examples. |
| **westNeighbor/Blender_math_anim** | Blender addon jawnie inspirowany **3Blue1Brown/Manim** | Bardzo istotny: wykresy, ODE, funkcje zespolone, LaTeX/Typst/PDF, Grease Pencil, morphing tekst↔wykres↔rysunek, preset animations. |
| **Peeps** | Starsza programistyczna biblioteka animacji w Blenderze | Historyczny przykład podejścia „Manim, ale z Blenderem”. Kodowo warto obejrzeć, ale projekt jest raczej przestarzały. |
| **Node To Python** | Oficjalne rozszerzenie zamieniające Geometry Nodes/material/compositor graphs na Python | **Bardzo ważne dla Twojego procesu uczenia agenta**: robisz dobry node graph raz → eksportujesz do czytelnego Pythona → powstaje recipe/example dla modelu. Wersja 4.2 obsługuje Blender 5.2. ([extensions.blender.org](https://extensions.blender.org/add-ons/node-to-python/?utm_source=chatgpt.com)) |
| **MolecularNodes** | Scientific/molecular animation przez Geometry Nodes | Gotowy backend dla struktur atomowych, cząsteczek i trajectory. Aktywny Python/GPL projekt. |
| **Beautiful Atoms** | Python + Blender + ASE/Pymatgen | Bardzo interesujące dla Twojej fizyki ciała stałego: atomy, kryształy, struktury z VASP/ASE/Pymatgen, rendering programistyczny. |
| **SciBlend** | Pełny toolkit scientific visualization w Blenderze | VTK/VDB/netCDF, dane zależne od czasu, colormaps, legendy, annotation, Geometry Nodes, compositor. Blender 5.1+, Python 3.13. ([extensions.blender.org](https://extensions.blender.org/add-ons/sciblend/?utm_source=chatgpt.com)) |
| **Sverchok** | Ogromny parametryczny system node'owy | >600 nodes; geometria, surfaces, scalar/vector fields, custom Python nodes. Nie jest narracyjnym Manimem, ale może być biblioteką „proceduralnych instrumentów”. |

Jest jeszcze świeży `claude-in-blender`: Claude Code działa bezpośrednio z N-panelu Blendera, zachowując kontekst sesji. To ciekawe dla interaktywnej „burzy mózgów”, ale nie rozwiązuje problemu automatycznego tworzenia dobrych animacji. ([blenderartists.org](https://blenderartists.org/t/claude-in-blender-ask-claude-code-directly-from-blenders-n-panel-free-gpl-3-0/1651408?utm_source=chatgpt.com))

## 2. Najważniejsze znalezisko z forum Blendera

Opis **3D-Agent** jest bardzo pouczający. Autor zrobił dokładnie klasyczny błąd, którego warto u Ciebie uniknąć: początkowo można myśleć, że wystarczy dać modelowi dokumentację `bpy` + przykłady + RAG i powiedzieć „stwórz scenę”.

Nie wystarcza.

Ich architektura rozdzieliła role na vision, planning/reasoning i code generation, a całość chodziła jako:

```text
perceive
   ↓
reason
   ↓
act
   ↓
render / inspect viewport
   ↓
verify
   └──────→ repair ──────┐
                          ↓
                       next step
```

Autor podkreśla, że **verification przez obraz okazało się najważniejszą częścią systemu**. Bez niego po kilku iteracjach model zaczyna dryfować i scena degeneruje się w coś, co określił jako „geometry soup”. ([devtalk.blender.org](https://devtalk.blender.org/t/3d-agent-blender-ai-assistant-built-a-multi-agent-system-on-top-of-blenders-mcp-and-python-api-and-sharing-architecture-learnings-for-the-lab-discussion/44260?utm_source=chatgpt.com))

To jest bardzo ważne również dla Manima.

Ty tylko masz dodatkową przewagę: Twoja animacja nie jest dowolnym obiektem 3D. Ma **znaczenie matematyczne**. Możesz więc sprawdzać ją dwutorowo:

```text
semantic / numerical verification
                +
      visual verification
```

Czyli nie tylko:

> „czy screenshot wygląda dobrze?”

ale również:

> „czy obiekt oznaczony `ket_psi` naprawdę transformuje się w `U psi`?”

> „czy koniec wektora jest w punkcie wyliczonym z równania?”

> „czy trzy poziomy energetyczne mają właściwe uporządkowanie?”

> „czy kamera nie ukrywa degeneracji, którą narracja właśnie tłumaczy?”

To jest znacznie silniejszy system QA niż typowy Blender-agent.

---

# 3. Nie budowałbym „agenta do Blendera”

Budowałbym coś szerszego:

```text
                 ┌──────────────────────┐
                 │    SOURCE LAYER      │
                 │ PDF / MD / web       │
                 │ video / lecture      │
                 │ slides / papers      │
                 └──────────┬───────────┘
                            ↓
                 ┌──────────────────────┐
                 │ KNOWLEDGE / EVIDENCE │
                 │ equations, claims,   │
                 │ concepts, citations  │
                 └──────────┬───────────┘
                            ↓
                 ┌──────────────────────┐
                 │ PEDAGOGICAL DIRECTOR │
                 │ "co trzeba wyjaśnić" │
                 └──────────┬───────────┘
                            ↓
                 ┌──────────────────────┐
                 │ VISUAL DIRECTOR      │
                 │ "jak to pokazać"     │
                 └──────────┬───────────┘
                            ↓
                  AnimationSpec / IR
                    ↙             ↘
              Manim compiler    Blender compiler
                    ↓             ↓
              Manim scene      bpy / GN scene
                    ↘             ↙
                   PREVIEW RENDER
                         ↓
                 critic / VLM / tests
                         ↓
                       repair
                         ↓
           ┌─────────────┼─────────────┐
           ↓             ↓             ↓
         video      manim-slides      PDF
```

**Blender i Manim powinny być backendami renderującymi**, a nie miejscem, w którym mieszka wiedza pedagogiczna.

To według mnie jest najważniejsza decyzja architektoniczna w całym projekcie.

---

# 4. Potrzebujesz wspólnego IR pomiędzy scenariuszem a kodem

To również ładnie łączy się z tym, co obecnie robicie z 3b1b.

Nie chciałbym, żeby po analizie filmu agent nauczył się:

```python
self.play(obj.animate.shift(LEFT * 2.3))
```

Interesujące jest:

```yaml
action:
  type: expose_structure
  subject: tensor_product
  technique: spatial_separation
  intent:
    show_that: factors_are_independent_spaces
```

a dopiero niżej:

```yaml
renderer:
  manim:
    animation: shift
    vector: [-2.3, 0, 0]
```

Dlatego Wasza obecna analiza 3b1b powinna mieć **minimum trzy poziomy**:

```text
video semantics
        ↕
animation semantics
        ↕
implementation
```

Czyli dla fragmentu filmu:

```text
"Grant chce pokazać, że dwie reprezentacje opisują ten sam obiekt"
```

może istnieć:

```yaml
visual_intent:
  relation: equivalence
  strategy: morph

objects:
  source: position_representation
  target: frequency_representation

temporal_pattern:
  preserve_identity: true
  change_representation: true
```

i dopiero potem:

```yaml
manim:
  primitive: TransformMatchingTex
```

To jest dokładnie warstwa, która pozwoli później powiedzieć:

> „zrób to samo w Blenderze”

bez konieczności kopiowania kodu Manima.

---

# 5. Wasza analiza 3b1b może być czymś znacznie bardziej wartościowym niż dataset code/video

Ja bym budował z niej **Visual Explanation Pattern Atlas**.

Przykładowo agent może odkryć z wielu filmów:

```text
concept:
    change_of_basis

pedagogical_problem:
    same_object_different_coordinates

effective_visual_patterns:
    - preserve object shape while axes rotate
    - temporarily show both coordinate systems
    - keep one invariant visually fixed
    - transform labels after geometry
    - delay equation until visual correspondence is established
```

oraz wiedzieć:

```text
observed_in:
    video_17:
        02:31-02:47
    video_43:
        04:12-04:29

implementations:
    manim:
        ...
```

I wtedy po paru setkach skorelowanych przykładów nie uczysz modelu:

> „jak Grant używa `Transform`”

tylko:

> **jak pewien problem poznawczy bywa zamieniany na język wizualny.**

To jest dużo ciekawsze naukowo i dużo bardziej uniwersalne.

---

# 6. BlenderMathAnim i Blender_math_anim są dla Ciebie ważniejsze niż typowe Blender MCP

`BlenderMathAnim` robi coś, co bardzo pasuje do Twojego sposobu pracy: Blender jest rendererem, ale scena jest tworzona **w całości z Pythona**, bez ręcznego budowania `.blend`. Autor wręcz wskazuje version control jako jedną z zalet takiego workflow.

Natomiast `westNeighbor/Blender_math_anim` jest wręcz zadeklarowany jako projekt inspirowany Manimem i przeznaczony do wyjaśnień matematyczno-fizycznych. Ma już gotowe rozwiązania dla funkcji jawnych, parametrycznych, polarnych, ODE, funkcji zespolonych, formuł z LaTeX/Typst/PDF, free drawing i — szczególnie interesujące — **morphing między tekstem, wykresem i rysunkiem**.

Nie forkowałbym jednak żadnego z nich i nie budował całej architektury wokół ich API.

Potraktowałbym je jako:

```text
corpus of Blender animation design patterns
```

dokładnie tak samo, jak teraz traktujecie 3b1b.

---

# 7. Geometry Nodes mogą być dla modelu dużo lepsze niż generowanie `bpy` od zera

Tutaj `Node To Python` jest wręcz idealnym narzędziem.

Możesz sam lub z pomocą kogoś znającego Blendera zrobić raz dobry proceduralny node group:

```text
VectorField
WaveSurface
CrystalLattice
Isosurface
BlochSphere
EnergyLandscape
NormalMode
OrbitalSurface
CameraOrbit
PhotonPacket
```

następnie `Node To Python` zamienia cały graph na czytelny Python. Rozszerzenie potrafi eksportować Geometry Nodes, materiały i compositor graphs wraz z layoutem, defaultami, subgroupami itd. ([extensions.blender.org](https://extensions.blender.org/add-ons/node-to-python/?utm_source=chatgpt.com))

Wtedy LLM nie musi za każdym razem projektować 70-node'owego graphu.

Może wykonywać:

```python
wave = WaveSurface(
    amplitude=A,
    wavelength=lamb,
    phase=phi,
    domain=(-8, 8),
)
```

i zmieniać kilka semantycznych parametrów.

Dla lokalnego modelu ma to kolosalne znaczenie: zmniejszasz przestrzeń wyszukiwania o kilka rzędów wielkości.

---

# 8. Scientific Blender jest obecnie dużo bogatszy, niż przypuszczałem

Tutaj pojawiło się kilka rzeczy, które wręcz pasują do Twoich przyszłych zastosowań.

**SciBlend** jest aktywnym Pythonowym frameworkiem naukowej wizualizacji i obsługuje m.in. VTK, VDB, netCDF, time-varying data, colormaps, annotations, grids i compositing. Najnowsza wersja jest już dostosowana do Blender 5.1/Python 3.13. ([extensions.blender.org](https://extensions.blender.org/add-ons/sciblend/?utm_source=chatgpt.com))

**MolecularNodes** daje bardzo rozwinięty poziom abstrakcji dla struktur molekularnych i animacji.

**Beautiful Atoms** jest szczególnie interesujące dla fizyki materiałowej, bo jest pythonowym modułem do atomów/molekuł w Blenderze i ma ekosystem ASE/Pymatgen.

To sugeruje, że Twój Blender backend nie powinien mieć jednego monolitycznego skillu:

```text
blender
```

tylko zestaw **domain capabilities**:

```text
blender/core
blender/math-geometry
blender/scientific-fields
blender/crystal
blender/molecule
blender/volume
blender/camera
blender/material
blender/compositor
```

Agent wybiera właściwe capability.

---

# 9. Jak podzieliłbym agentów, skille i hooki

Nie robiłbym dwudziestu agentów. To bardzo łatwo zmienia się w agentic-slop, gdzie modele przekazują sobie coraz mniej precyzyjne streszczenia.

Raczej **3–4 agentowe role + dużo deterministycznych skills/tools**.

| Element | Odpowiedzialność |
|---|---|
| `Research/Pedagogy Director` | rozumie źródła, kontroluje poprawność fizyczną, buduje tok wyjaśnienia |
| `Visual Director` | zamienia problemy poznawcze na visual beats i wybiera wzorce z Pattern Atlas |
| `Compiler Agent` | kompiluje IR do Manim/Blender; może mieć dwa odrębne skills |
| `Critic / QA` | ogląda preview, porównuje ze specyfikacją i szuka błędów |
| `physics-* skills` | QM, group theory, vector spaces itd. jako retrieval/instruction packs |
| `manim-* skills` | API, style, recipes, 3b1b pattern atlas |
| `blender-* skills` | bpy/GN/domain-specific recipes |
| `export-* skills` | slides, PDF, video, thumbnails |
| hooks | schema validation, SymPy/numeric checks, lint, render smoke test, vision QA, git snapshot |

Co ważne: **scientific correctness powinno być sprawdzane przed generowaniem grafiki**, a nie pozostawione VLM-owi oglądającemu film.

---

# 10. Twój agent piszący scenariusze powinien mieć dwie warstwy pamięci

Tutaj użyłbym Twoich dokumentów trochę inaczej niż klasyczny „RAG over PDFs”.

Pierwsza warstwa:

```text
CONTENT MODEL
```

czyli to, co materiał rzeczywiście mówi:

```text
definitions
relations
derivations
assumptions
equations
examples
dependencies
citations
```

Druga:

```text
PEDAGOGICAL STYLE MODEL
```

czyli to, **jak Ty budujesz wyjaśnienie**:

```text
co wprowadzasz najpierw
kiedy formalizujesz intuicję
jak długo pozostajesz przy jednym problemie
kiedy wprowadzasz symbol
jak wracasz do wcześniejszego pojęcia
jak przechodzisz od obiektu fizycznego do konstrukcji matematycznej
czego unikasz
```

Nie trenowałbym na początku modelu na Twoim stylu.

Zrobiłbym coś w rodzaju:

```text
StyleProfile
+
retrieval of structurally similar passages
+
few-shot complete examples
```

Dopiero gdy zbierzesz np. kilkaset par:

```text
source material
      ↓
your finished explanation
      ↓
your finished animation script
```

sensownie będzie zastanawiać się nad distillation/fine-tuningiem.

---

# 11. I tutaj pojawia się bardzo ciekawy format pośredni

Wyobrażam sobie np.:

```yaml
scene:
  id: "dual-space-pairing-03"

  objective:
    learner_should_understand:
      - "covector acts on a vector"
      - "the scalar pairing is basis-independent"

  narrative:
    voiceover_ref: narration.md#beat-17

  objects:
    - id: v
      semantic_type: vector
      space: V

    - id: omega
      semantic_type: covector
      space: V_star

    - id: pairing
      semantic_type: scalar
      expression: "\\omega(v)"

  beats:
    - id: B01
      intent: establish_objects
      duration: 4.0

    - id: B02
      intent: apply_map
      subject: omega
      target: v

    - id: B03
      intent: reveal_invariant
      preserve:
        - pairing

  renderer:
    preferred: manim

  validation:
    semantic:
      - "omega.space == dual(v.space)"
      - "pairing.output_dimension == 1"

    visual:
      - "labels_not_overlapping"
      - "pairing_visible_for_at_least_2s"
```

Ten plik powinien być **źródłem prawdy**.

Nie skrypt Manima.

Nie skrypt Blendera.

Nie video.

---

# 12. Wtedy połączenie Manim + Blender robi się proste koncepcyjnie

Nie próbowałbym robić:

```text
Manim → Blender
```

ani:

```text
Blender → Manim
```

tylko:

```text
                AnimationSpec
               /             \
          Manim AST       Blender AST
              |                |
          renderer          renderer
```

Manim dostaje wszystko, w czym jest doskonały:

```text
równania
diagramy
grafy
przestrzenie abstrakcyjne
2D/2.5D
transformacje symboliczne
axes
plots
text choreography
```

Blender:

```text
real 3D
crystals
molecular structures
orbitals / isosurfaces
vector/scalar fields
volumes
lighting
camera motion
geometry nodes
particle / physical scenes
```

A scena może być hybrydowa:

```text
Manim overlay
      +
Blender transparent render
      +
shared timeline
```

lub odwrotnie.

---

# 13. PDF i manim-slides nie są wtedy osobnymi projektami

To też jest ważne.

Jeżeli każdy `beat` ma:

```text
learning objective
formula
visual
narration
source
```

to możesz z tego samego dokumentu wygenerować:

```text
VIDEO
beat → pełna animacja

SLIDES
beat → interactive stop / reveal

PDF
beat → selected keyframe + equation + explanation
```

To umożliwia coś naprawdę fajnego:

> jedna semantyczna reprezentacja wykładu, kilka mediów wyjściowych.

I nagle Twoja praca nad generowaniem animacji przestaje być „AI robi filmy”, tylko staje się czymś w rodzaju **compiler toolchain for mathematical explanation**.

To jest moim zdaniem znacznie lepsza definicja projektu.

---

# 14. Bardzo ostrożnie z bezpośrednim `exec()` w Blenderze

Oficjalny Blender MCP obecnie jawnie ostrzega, że kod wygenerowany przez LLM jest wykonywany w Blenderze **bez guardów** i rekomenduje izolowane środowisko, jeśli istnieją wrażliwe dane. ([blender.org](https://www.blender.org/lab/mcp-server/?utm_source=chatgpt.com))

U Ciebie dorzuciłbym do tego jeszcze powód inżynierski, nie tylko security.

Jeżeli pozwolisz agentowi wszędzie robić:

```python
execute_arbitrary_python(...)
```

to nie zbudujesz stabilnego systemu. Agent za każdym razem wymyśli inną implementację.

Zdecydowanie lepiej:

```text
high-level deterministic tools
        ↓
well-tested Python implementation
        ↓
bpy
```

i raw Python zostawić jako escape hatch.

---

# 15. Blender Foundation dochodzi zresztą do podobnego rozdzielenia odpowiedzialności

Brecht Van Lommel na DevTalk napisał wprost, że **MCP Server jest API**, a nie agentem ani systemem orkiestracji. ([devtalk.blender.org](https://devtalk.blender.org/t/3d-agent-blender-ai-assistant-built-a-multi-agent-system-on-top-of-blenders-mcp-and-python-api-and-sharing-architecture-learnings-for-the-lab-discussion/44260?page=3&utm_source=chatgpt.com))

To dobrze pasuje do Twojego projektu:

```text
MCP = transport / capability interface
Agent = reasoning
Skill = procedural knowledge
IR = contract
Renderer = execution
Critic = verification
```

Nie mieszajmy tych warstw.

---

# 16. Co bym zrobił teraz, zanim w ogóle zaczniesz „uczyć Blendera”

Moja proponowana kolejność wyglądałaby tak:

| Etap | Cel | Produkt |
|---|---|---|
| **0. Architecture prototype** | udowodnić IR → Manim/Blender | `AnimationSpec v0.1` + po jednej scenie w każdym backendzie |
| **1. 3b1b code analysis** | wydobyć implementacyjne primitives | `code_events.yaml` |
| **2. 3b1b video analysis** | wydobyć visual/pedagogical events | `visual_events.yaml` |
| **3. Alignment** | nauczyć się związku intent ↔ visual ↔ code | `pattern_atlas/` |
| **4. Blender corpus** | zrobić analogiczną analizę BlenderMathAnim, Blender_math_anim, GN recipes | `blender_patterns/` |
| **5. Scenario pipeline** | source → explanation → visual beats | `lesson.yaml` |
| **6. Dual compiler** | `lesson.yaml`/IR → engines | `manim_backend`, `blender_backend` |
| **7. Closed-loop QA** | preview → inspect → repair | automated render critic |
| **8. Multi-artifact build** | film/slides/PDF | jeden `build` command |

Już na **etapie 0** zrobiłbym trzy trudne testy, a nie banalne kulki: np. pakiet falowy i transformata Fouriera, precesja spinu na sferze Blocha oraz struktura krystaliczna/defekt z izopowierzchnią. Jeżeli IR potrafi sensownie obsłużyć te trzy różne klasy problemów, fundament będzie rozsądny.

---

## Najciekawszy wzorzec repo, który znalazłem dla Ciebie

`Blender-Superskill` warto wręcz rozebrać linia po linii.

To nie jest skill do nauki matematyki, ale **architektonicznie trafia bardzo blisko Twojego pomysłu**. Ma trwały orchestrator, rozdziela generic runner od asset-specific recipe i zapisuje `state.json`, `plan.json`, wyniki poszczególnych kroków i logi. Worker dostaje tylko ograniczony bieżący problem, zamiast całej historii.

Ja bym z tego ukradł **strukturę idei**, nie konkretną logikę modelowania:

```text
persistent state
bounded worker context
plan
execute
inspect
repair
final review
```

i zastosował ją do:

```text
pedagogy
visual design
Manim
Blender
scientific QA
```

## Czyli: czy ktoś już zrobił Twój projekt?

**Nie. Ale jest zaskakująco dużo gotowej infrastruktury, dzięki której nie musisz zaczynać od `bpy.ops.mesh.primitive_cube_add()`.**

Najważniejsze jest też to, że po tym przeglądzie zmieniłbym nieco cel projektu. Nie pisałbym „AI agenta do generowania animacji w Manimie i Blenderze”.

Pisałbym:

> **system kompilacji wyjaśnień fizyczno-matematycznych z semantycznego scenariusza do wielu reprezentacji wizualnych, z agentowym planowaniem i zamkniętą pętlą walidacji.**

Manim i Blender są wtedy tylko dwoma backendami.

I to bardzo ładnie uzasadnia również to, co obecnie robicie ze statyczną analizą 3b1b — **o ile wynikiem tej analizy nie będzie tylko katalog API Manima, lecz katalog zależności `pedagogical intent ↔ visual strategy ↔ implementation`.**

Jeżeli chcesz, następnym krokiem mogę rozpisać już **konkretną architekturę repozytorium** dla tego projektu: katalogi `agents/`, `skills/`, `hooks/`, `schemas/`, `pattern_atlas/`, `backends/manim/`, `backends/blender/`, formaty YAML, kontrakty między agentami oraz dokładnie które z powyższych repo warto sklonować i statycznie przeanalizować w pierwszej kolejności.

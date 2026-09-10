# research

Analizy poboczne i materiał wejściowy do decyzji projektowych. Zapisy rozpoznania
terenu: przeglądy istniejących narzędzi, literatury i możliwych kierunków, które
trzeba było zrobić, zanim dało się cokolwiek rozstrzygnąć.

**Czym ten katalog nie jest.** Nie jest dokumentacją projektową — ta stoi w korzeniu
repozytorium (`vision.md`, `roadmap.md`, `design-spec.md`, `decision-log.md`) i tylko
ona wiąże. Nie jest też korpusem obserwacji — ten stoi w `observations/` i powstaje
maszynowo, z dowodami w postaci odwołań do konkretnych linii kodu.

**Status treści.** Pliki są w większości wynikiem rozmów z zewnętrznymi modelami.
Nie były weryfikowane linia po linii i nie mają statusu ustaleń. Twierdzenie stąd staje
się wiążące dopiero wtedy, gdy trafi do dokumentu projektowego albo do `decision-log.md`.

## Zawartość

| plik | co zawiera |
|---|---|
| [`manim_blender_agent_system_review.md`](manim_blender_agent_system_review.md) | przegląd istniejących projektów spinających agentów, Blender i animację matematyczną; wniosek: klocki istnieją, brakuje warstwy pośredniej i orkiestracji |
| [`pedagogy_epistemic_style_analysis.md`](pedagogy_epistemic_style_analysis.md) | przegląd literatury i narzędzi pod kątem modelowania procesu budowania wyjaśnienia, a nie stylu językowego |
| [`chat_history_learning_process_mining.md`](chat_history_learning_process_mining.md) | pomysł na wykorzystanie historii własnych rozmów jako zapisu procesu uczenia się; źródło danych o tym, gdzie powstaje nieporozumienie |
| [`peer-review/comparison-with-informant-video.md`](peer-review/comparison-with-informant-video.md) | zestawienie z projektem `informant-video` (działający pipeline z artykułu do wideo): co każdy z projektów robi lepiej, z odnośnikami do konkretnych plików |
| [`peer-review/peer-review-manim-claude.md`](peer-review/peer-review-manim-claude.md) | zewnętrzny przegląd repozytorium z listą działań do odhaczenia; każde działanie wskazuje działającą implementację w `informant-video` jako punkt odniesienia |

Nowy plik w tym katalogu dopisujemy do tabeli powyżej. Katalog bez spisu treści
w ciągu miesiąca staje się śmietnikiem.

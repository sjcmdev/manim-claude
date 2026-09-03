# manim-claude

Narzędzie zamieniające opis słowny, materiały wykładowe i odręczny szkic w animację Manim,
z weryfikacją wizualną i bramkami akceptacji. Rdzeniem jest autorska biblioteka idiomów
i wzorców projektowania animacji oraz agenty piszące kod, które z niej korzystają.

Projekt niekomercyjny. Etap: dokumentacja projektowa zamknięta, kod nie powstał.

## Dokumenty

| plik | dla kogo | co zawiera |
|---|---|---|
| [`vision.md`](vision.md) | współpracownicy, osoby z zewnątrz | problem, odbiorcy, dlaczego to ma szansę zadziałać, czego świadomie nie robimy, kwestie prawne |
| [`roadmap.md`](roadmap.md) | zespół | dwa tory prac, etapy z kryteriami zakończenia, podział na role, zasady pracy, najbliższe kroki |
| [`design-spec.md`](design-spec.md) | wykonawcy | architektura, przepływ, układ repozytorium, schematy artefaktów, inwentarz skilli, agentów, hooków i skryptów |
| [`decision-log.md`](decision-log.md) | wszyscy | przebieg ustaleń, uzasadnienia, odrzucone kierunki |

Kolejność czytania dla nowej osoby: `vision.md`, potem `roadmap.md`, potem `design-spec.md`.
`decision-log.md` służy do sprawdzenia, dlaczego coś wygląda tak, a nie inaczej, zanim ktoś
zaproponuje zmianę.

## Skrót w pięciu punktach

1. **Wejście**: prompt, dokumenty (PDF, Markdown, prezentacja), odręczny szkic.
2. **Trzy bramki blokujące**: plan, statyczny układ, pełny podgląd. Pomiędzy nimi system
   pracuje sam, z limitem prób i limitem czasu.
3. **Model ogląda swoją pracę**: render klatki, ocena wizualna, poprawka. Nie tylko
   „kod się kompiluje”.
4. **Wiedza jest skodyfikowana**: biblioteka falsyfikowalnych reguł, wersjonowana niezależnie
   od kodu narzędzia.
5. **Dwa niezależne tory prac**: biblioteka i harness produkcyjny mogą powstawać równolegle.

## Wymagania techniczne

Manim Community Edition >= 0.21, Python >= 3.14, ffmpeg, LaTeX (opcjonalnie — bez niego
generowanie degraduje się do `Text` z unicode zamiast `Tex`). Claude Code jako harness.

## Stan i najbliższe kroki

1. Inicjalizacja repozytorium produktu.
2. Hook chroniący przed wprowadzeniem materiału na licencji ShareAlike — **przed** pierwszym
   pobraniem materiału referencyjnego.
3. Równolegle: pobieranie materiału referencyjnego (tor A) oraz szkielet `package/`
   z konfiguracją domyślną (tor B).

Szczegóły w [`roadmap.md`](roadmap.md).

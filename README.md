# manim-claude

Narzędzie zamieniające opis słowny, materiały wykładowe i odręczny szkic w animację Manim,
z weryfikacją wizualną i bramkami akceptacji. Rdzeniem jest autorska biblioteka idiomów
i wzorców projektowania animacji oraz agenty piszące kod, które z niej korzystają.

Projekt niekomercyjny. Etap: dokumentacja projektowa zamknięta, powstaje materiał
wejściowy do biblioteki idiomów. Właściwe narzędzie jeszcze nie powstało.

## Stan faktyczny

**Co już jest.**

- **Pipeline materiału referencyjnego** (`tooling/reference/`) — pobieranie filmów, napisów
  i metadanych, wyciąganie klatek kluczowych przez detekcję cięć, składanie pakietów
  roboczych dla zewnętrznego czatu. Materiał ląduje poza drzewem projektu, co jest
  wymuszane maszynowo, bo źródła są na licencji CC BY-NC-SA.
- **Miner** (`tooling/reference/mine_code.py`) — puszcza agenta na katalogach tematycznych
  klonu cudzego kodu i zwraca obserwacje jako YAML. Jeden skrypt, trzy analizy; różnią się
  wyłącznie plikiem promptu.
- **Korpus obserwacji** (`observations/`) — 900 reguł wydobytych z kodu 3b1b z lat 2016–2026
  oraz z trzech bibliotek społecznościowych: 324 o organizacji kodu, 491 o konstrukcji
  animacji, 85 gotowych technik.
- **Syntezy porównawcze** (`observations/synthesis/`) — korpus streszczony przez dwa
  niezależne przebiegi agenta i zestawiony w tabelach zgodności i rozbieżności.
- **Przegląd autorski** (`observations/autor-grill.md`) — konfrontacja wydobytych reguł
  z praktyką autora projektu.
- **Testy** (`tests/`) — samosprawdzenie logiki skryptów referencyjnych, bez sieci i dysku.

**Czego jeszcze nie ma.**

- `idioms/` — biblioteka idiomów. Korpus obserwacji jest surowcem, nie biblioteką;
  reguła awansuje dopiero po przeglądzie autorskim.
- `package/` — właściwe narzędzie: agenty, skille, hooki, konfiguracja domyślna.
- Harness produkcyjny: trzy bramki akceptacji, pętla render–ocena–poprawka.
- `pyproject.toml`, bramki techniczne, CI.

## Mapa repozytorium

| katalog lub plik | co zawiera |
|---|---|
| [`vision.md`](vision.md) | problem, odbiorcy, dlaczego to ma szansę zadziałać, czego świadomie nie robimy, kwestie prawne |
| [`roadmap.md`](roadmap.md) | dwa tory prac, etapy z kryteriami zakończenia, podział na role, zasady pracy |
| [`design-spec.md`](design-spec.md) | architektura, przepływ, układ repozytorium, schematy artefaktów, inwentarz skilli, agentów, hooków i skryptów |
| [`decision-log.md`](decision-log.md) | przebieg ustaleń, uzasadnienia, odrzucone kierunki |
| [`TODO.md`](TODO.md) | lista zadań, polityka gałęzi, stan wykonania |
| [`observations/`](observations/) | korpus obserwacji wydobytych z cudzego kodu plus syntezy; opis schematu w [`observations/README.md`](observations/README.md) |
| [`research/`](research/) | analizy poboczne i rozpoznanie terenu; nie wiążą, opis w [`research/README.md`](research/README.md) |
| [`tooling/reference/`](tooling/reference/) | skrypty i prompty do mielenia materiału referencyjnego |
| [`tests/`](tests/) | testy skryptów referencyjnych |
| `3b1b-playlists.txt` | lista playlist wejściowych dla `fetch_reference.py` |

Kolejność czytania dla nowej osoby: `vision.md`, potem `roadmap.md`, potem `design-spec.md`.
`decision-log.md` służy do sprawdzenia, dlaczego coś wygląda tak, a nie inaczej, zanim ktoś
zaproponuje zmianę.

## Uruchomienie

```bash
# testy — bez sieci, bez ffmpega, bez dysku
pytest tests/          # albo bez pytesta: python tests/test_reference.py

# pobranie materiału referencyjnego do katalogu roboczego poza repozytorium
python tooling/reference/fetch_reference.py

# jeden przebieg minera; analizę wybiera prompt, katalog wyniku wybiera --out
python tooling/reference/mine_code.py \
    --prompt tooling/reference/animation_miner_prompt.md --out animation
```

Miner wymaga klonu `3b1b/videos` w katalogu roboczym i zalogowanego `codex` w `PATH`.
Katalog roboczy to domyślnie `~/manim-claude-reference`, zmienia go `--root`.

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
Do mielenia materiału referencyjnego dodatkowo `yt-dlp` oraz `codex`.

## Materiał referencyjny a licencja

Kod i filmy 3b1b są na CC BY-NC-SA 4.0. Nic z tego materiału nie trafia do drzewa projektu:
klon i wyniki pośrednie leżą w katalogu roboczym poza repozytorium, a do repozytorium wracają
wyłącznie reguły wraz z odwołaniami do plików i linii. Wymusza to `tooling/reference/common.py`.

## Najbliższe kroki

1. Rewizja rozbieżności między syntezami i przegląd autorski korpusu.
2. `merge_observations.py` — scalanie obserwacji z wykryciem duplikatów i konfliktów.
3. `idioms/` w wersji 0.1.
4. Równolegle, tor B: szkielet `package/` z konfiguracją domyślną i bramkami technicznymi.

Szczegóły w [`roadmap.md`](roadmap.md), stan zadań w [`TODO.md`](TODO.md).

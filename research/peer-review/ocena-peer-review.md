# Ocena dwóch dokumentów peer review

Data: 2026-09-14. Oceniane: [`peer-review-manim-claude.md`](peer-review-manim-claude.md)
i [`comparison-with-informant-video.md`](comparison-with-informant-video.md)
(Adam Krysztopa, 2026-09-10). Twierdzenia o stanie manim-claude sprawdzono przed scaleniem
PR #1; twierdzeń o `informant-video` nie da się zweryfikować z konta autora (repozytorium
prywatne, brak dostępu).

## Werdykt

Oba dokumenty są rzetelne i warto je traktować jako listę roboczą. Każde sprawdzone
twierdzenie o manim-claude okazało się prawdziwe: brak hooka, brak `LICENSE`, zepsuty
`_2022-puzzles.yaml`, 33 powtórzone identyfikatory, dryf taksonomii, `line: 420-422` jako
napis, nieobsłużony `TimeoutExpired`. Mocną stroną jest uczciwe rozdzielenie „lepsza
praktyka” od „większa dojrzałość” i osobny rozdział o słabościach własnego projektu.

Słabość jest jedna, ale istotna: rekomendacje przenoszą ciężar procesowy projektu
o innej skali. `informant-video` ma 117 bramek, z czego 29 nigdy niczego nie odrzuciło,
i archiwum ~200 lekcji — recenzent sam nazywa to kosztem. Część zaleceń trzeba więc
przyjąć jako kierunek, nie jako zadanie na dziś.

## Mocne strony

- **Konkret i sprawdzalność.** Liczby z parsowania całego korpusu, nazwy plików, numery
  linii. Da się odhaczać.
- **Trafna diagnoza główna:** projekt jest zbiorem obietnic bez mechanizmu, a jedyna reguła
  nazwana bezwzględną (hook przed pobraniem) została złamana.
- **Uczciwość wobec atutów manim-claude:** korpus, podwójna ślepa synteza, grill z
  zapisanymi odrzuceniami, dyscyplina zakresu, myślenie o licencji przed mieleniem.
- **Zalecenia o najwyższym stosunku wartości do kosztu:** walidator z manifestem,
  próba sekcji Manim CE w godzinę, szablon wpisu idiomu z parą scen łamiącą i przechodzącą,
  sprawdzenia mechaniczne przed `visual-judge`, akceptacja jako flaga czytana przez skrypt.

## Słabe strony

- **Niesprawdzalne odnośniki.** Większość „see informant-video” prowadzi do prywatnego
  repozytorium. Dla osoby z zewnątrz dokument jest w połowie nieczytelny; to też blokada
  upublicznienia (`TODO.md`, task/01).
- **Walidacja z zewnątrz, której nie widzimy.** „Reguły działają jako lint w
  informant-video” to najmocniejszy argument za korpusem i jednocześnie nieweryfikowalny.
- **Import procesu zamiast problemu.** `gates.toml`, generowanie `.claude/` i `.codex/`
  z jednego źródła, graf lekcji z wykrywaniem oscylacji — sensowne przy 20 skillach i
  dwóch harnessach, przedwczesne przy zerze skilli.
- **Niespójność wewnętrzna.** Porównanie chwali testy bez pytest (runner czyta kody
  wyjścia), przegląd zaleca „test runner”. Przegląd chce CI „dziś”, a porównanie pokazuje,
  że CI recenzenta w nagłówku przyznaje, czego nigdy nie uruchomiono.
- **Duże nakładanie się dokumentów** (~60% treści). Porównanie wystarczyłoby jako
  uzasadnienie, przegląd jako lista.
- **Tor narracyjny prawie pominięty.** Stwierdza, że żaden film nie przeszedł przez czat,
  ale nie proponuje, jak analizować wideo. To dziś największa luka merytoryczna projektu
  (patrz dwa nowe pomysły w `research/`).

## Zalecenia: przyjąć / odłożyć / odrzucić

| zalecenie | decyzja | gdzie / dlaczego |
|---|---|---|
| hook licencyjny, `LICENSE` | przyjęte | w budowie, `task/02-fundamenty-repozytorium` |
| `pyproject.toml`, ruff, mypy, testy | przyjęte | jw., lokalne `tooling/check.py` |
| CI na GitHub Actions | **odłożone** | spec fundamentów: najpierw lokalny kontrakt, CI podpina się bez zmian |
| walidator korpusu, naprawa YAML, unikalne id, taksonomia | przyjęte | w budowie |
| manifest przebiegu (model, effort, hash promptu, rewizja klonu) | przyjęte | w budowie; stary korpus jako `legacy-unverified` |
| `TimeoutExpired` w minerze | przyjęte | w budowie |
| `confidence` bez informacji, `falsifiable` zawsze `true` | **do decyzji** | walidator sprawdza tylko wartości; czy pole zostaje, rozstrzyga kurator |
| próbka 30 dowodów `file:line` | przyjąć | tanie, przed kuracją; brak zadania |
| rozjazdy dokumentacji (9.2, 9.3, 13, status speca) | przyjąć | tanie; brak zadania |
| szablon wpisu idiomu z parą scen | przyjąć, **priorytet spotkania** | to jedyny styk torów A i B |
| próba mechanizmu sekcji na Manim CE | przyjąć | przed task/13 |
| jeden blok toru B end-to-end przed kuracją | **do decyzji** | agenda, pkt 4.4 |
| sprawdzenia mechaniczne przed `visual-judge` | przyjąć | `docs/pipeline-komponenty.md` |
| tiery modeli zamiast nazw | przyjąć | przy task/11 |
| trzy kody wyjścia hooków | przyjąć | hook licencyjny już tak działa |
| Codex vs D2 | przyjąć | wpis do `decision-log.md` |
| kolejka lekcji od razu | odłożyć | zapis ustaleń grilla do speca tak; maszyneria lekcji w etapie 3 |
| `gates.toml`, generowany control plane | odrzucić na teraz | brak bramek i drugiego harnessu |
| pomiar kodu autora | przyjąć jako pomysł | naturalnie łączy się z analizą wielopoziomową |
| decyzja językowa | przyjąć | do `decision-log.md` |

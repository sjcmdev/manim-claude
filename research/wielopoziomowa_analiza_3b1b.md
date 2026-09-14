# Wielopoziomowa analiza filmów 3Blue1Brown

**Status:** pomysł, 2026-09-14. Nie wiąże.

## Pomysł

Dziś korpus ma dwa rozłączne źródła: kod (`file:line`) i planowaną analizę wideo
(znaczniki czasu). Nikt nie łączy jednego z drugim. Tymczasem 3b1b jest jedynym
materiałem, gdzie mamy jednocześnie film i kod, który go wyprodukował. Analiza
wielopoziomowa bierze jeden film i opisuje go na pięciu poziomach, a obserwacje
z różnych poziomów wiąże wspólnym fragmentem czasu i kodu.

## Poziomy

| poziom | pytanie | wejście | dowód |
|---|---|---|---|
| **1. narracja** | jak zbudowane jest wyjaśnienie: pytanie, intuicja, rozróżnienie, formalizm, przykład, sprawdzenie | transkrypcja | `t_start–t_end` |
| **2. narracja wspomagana wizualnie** | co widz widzi, gdy pada dane zdanie; czy obraz wyprzedza, towarzyszy, czy podsumowuje słowo | transkrypcja + klatki | para: zdanie ↔ stan kadru |
| **3. układ sceny** | podział kadru, co trwa, co znika, kolory jako kodowanie pojęć, hierarchia | klatki kluczowe | klatka + opis układu |
| **4. wygląd animacji** | rodzaj ruchu, czas trwania, przejścia, co jest animowane, a co podmieniane | ujęcia + różnice klatek | `t_start–t_end` |
| **5. kod ↔ animacja** | która klasa `Scene` i które linie produkują dany fragment; jakim idiomem kodu uzyskano efekt z poziomu 4 | kod `3b1b/videos` + film | `file:line` ↔ `t_start–t_end` |

Poziom 1 kontynuuje `pedagogy_epistemic_style_analysis.md`. Poziomy 3–4 zasilają
`observations/animation`. Poziom 5 jest nowy i to on daje wartość całości: reguła
animacyjna z dowodem w kodzie i w obrazie jednocześnie jest dużo mocniejsza niż każda
z osobna, i od razu wskazuje, jak ją zakodować w `scene-coder`.

## Dopasowanie kodu do filmu (poziom 5)

Kod 3b1b nie ma znaczników czasu. Kandydaci na kotwice:

- napisy i wzory: literały `Tex`/`Text` w kodzie ↔ OCR klatek;
- kolejność klas w pliku ↔ kolejność ujęć;
- nazwy klas i sekcji ↔ tematy w transkrypcji;
- charakterystyczne liczby (zakresy osi, liczba obiektów) ↔ to, co widać.

Renderu kodu 3b1b nie przechowujemy ani nie publikujemy; jeśli potrzebny do dopasowania,
wyłącznie w katalogu roboczym.

## Wynik

Jeden rekord na fragment filmu z polami dla każdego poziomu i wspólnym kluczem
(`video`, `t_start`, `t_end`, `scene_class`, `file`, `line_start`, `line_end`).
Walidowany kontraktem korpusu, z manifestem. Z rekordów wyprowadzane są zwykłe obserwacje
per poziom, więc kurator nie musi znać nowego formatu.

## Licencja

Kod i filmy 3b1b są objęte CC BY-NC-SA. Obowiązuje ta sama zasada co przy minerze kodu:
materiał wyłącznie poza repozytorium, do korpusu trafia opis własnymi słowami i odwołania,
bez cytowania kodu i bez klatek. Hook `no_3b1b_code.py` pilnuje zapisu.

## Pytania na spotkanie

1. Pilot: który film? Warunek: kod w `3b1b/videos` istnieje i jest kompletny
   (seria 2023+).
2. Czy poziomy 1–4 robimy tym samym lokalnym pipeline'em GPU co analizę
   dobrze poprowadzonych filmów (`analiza_konstrukcji_filmow_gpu.md`)? Rekomendacja: tak,
   3b1b jako pierwszy przypadek, poziom 5 jako dodatek dostępny tylko tu.
3. Ile ręcznej weryfikacji dopasowania kod ↔ film akceptujemy w pilocie?
4. Czy to zastępuje task/06 (analiza narracji przez zewnętrzny czat)?

## Ryzyka

- Dopasowanie kod ↔ film może być niejednoznaczne (kod zmieniany po nagraniu, sceny
  wycięte w montażu). Pilot ma zmierzyć odsetek fragmentów z pewną kotwicą.
- Pięć poziomów to dużo — pilot na jednym filmie i trzech poziomach (1, 2, 5)
  pokaże, czy reszta jest warta kosztu.

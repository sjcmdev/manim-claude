# Porównanie dwóch niezależnych syntez idiomów konstrukcji scen w Manimie

Notacja **T / S** oznacza liczbę źródeł podaną odpowiednio przez syntezę Terra i Sol. Gdy jedna synteza rozbiła temat na kilka reguł, zachowano wszystkie jej liczby zamiast tworzyć pozornie wspólną sumę.

## 1. Zgodne

To reguły rozpoznane niezależnie przez obie syntezy. Różnice liczebności nie są tu wygładzone; trafiają również do sekcji „Rozbieżności”.

### Granice scen i ponowne użycie

1. **Wydzielaj niezależny beat narracyjno-wizualny do osobnej klasy sceny**, jeśli ma własny stan wejścia i wyjścia albo powinien być osobno renderowany i montowany. Źródła: **13 / 12**. Dowód: `_2016/eola/chapter0.py:64`.

2. **Długi `construct()` dziel na nazwane metody fazowe, a sam `construct()` zostaw jako orkiestrator**, gdy fazy współdzielą stan i nie są naturalnymi punktami cięcia. Źródła: **6 / 5**. Dowód: `_2016/eola/chapter8.py:113`.

3. **Rodzinę podobnych scen buduj przez klasę bazową oraz parametry lub wąskie haki**, zamiast kopiować `construct()`. Źródła: **19 / 18**. Dowód: `_2016/eola/chapter3.py:240`.

4. **Powtarzalne konstrukcje przenoś do parametryzowanych helperów, fabryk, komponentów, klas bazowych lub modułów współdzielonych.** Terra rozdziela ten wzorzec na współdzielone komponenty (**14**) i parametryzowane fabryki (**17**); Sol scala go w regułę obejmującą **21** źródeł. Dowód: `_2019/diffyq/part1/shared_constructs.py:19`.

5. **Projektuj złożony motyw z nazwanymi częściami lub metadanymi domenowymi i odwołuj się do nich po znaczeniu, nie przez kruche indeksy.** Terra: fabryki z nazwanymi częściami (**17**) oraz jawna reguła metadanych (**6**); Sol: komponenty z nazwanymi częściami (**14**) oraz odwołania semantyczne (**10**). Dowód: `_2022/convolutions/discrete.py:386`.

### Stan, zależności i cykl życia

6. **Obiekty współdzielone przez wiele faz trzymaj w nazwanych atrybutach sceny, a jednorazowe lokalnie.** Źródła: **10 / 8**. Dowód: `_2017/eoc/chapter1.py:80`.

7. **Jeden wspólny parametr liczbowy ciągłej zmiany trzymaj w jednym `ValueTrackerze` i wyprowadzaj z niego zależne reprezentacje.** Źródła: **16 / 15**. Dowód: `_2019/diffyq/part1/pendulum.py:1023`.

8. **Animuj obiekt sterujący lub tracker, a trwałe zależności geometrii, tekstu i stylu utrzymuj updaterami albo `always_redraw`.** Obie syntezy: **20** źródeł. Terra dopowiada, by kroki narracyjne wykonywać jawnymi animacjami. Dowód: `_2024/holograms/diffraction.py:420`.

9. **Przy ręcznej zmianie roli lub reprezentacji obiektu jawnie zatrzymuj, czyść, odpinaj i w razie potrzeby ponownie podłączaj updatery.** Źródła: **12 / 15**. Dowód: `_2023/clt/main.py:1280`.

10. **Przed czasową, odwracalną reorganizacją zapisuj stan albo przygotuj target, a potem przywracaj go zamiast ręcznie odtwarzać układ.** Źródła: **6 / 8**. Dowód: `_2017/eoc/chapter7.py:195`.

11. **Odłącz updater od kopii, która ma stać się nieruchomym śladem, snapshotem lub źródłem niezależnej transformacji.** Źródła: **3 / 3**. Dowód: `_2022/puzzles/subsets.py:838`.

12. **Autonomiczną symulację zamykaj w komponencie posiadającym własny stan lub czas oraz jawne metody zatrzymania i wznowienia.** Źródła: **4 / 4**. Dowód: `_2025/laplace/shm.py:46`.

### Kompozycja, kamera i ciągłość

13. **Buduj układ relacyjnie względem kotwic i sąsiadów, a współrzędne bezwzględne rezerwuj dla świadomych kotwic danych, kamery lub całego kadru.** Źródła: **21 / 21**. Dowód: `_2016/eola/chapter0.py:70`.

14. **Grupuj geometrię, etykiety, ramki i prowadnice należące do jednego konceptu przed ich wspólną transformacją.** Źródła: **16 / 14**. Dowód: `_2016/eola/chapter9.py:331`.

15. **Pozycje wynikające z danych mapuj przez jeden układ współrzędnych, zamiast powielać stałe kadru i ręczne przeliczenia.** Źródła: **5 / 5**, ale z innym składem źródeł. Dowód: `_2024/antp/main.py:389`.

16. **Narracyjne napisy, panele i HUD przypinaj do kadru podczas ruchu kamery 3D.** Źródła: **6 / 6**. Dowód: `_2023/gauss_int/integral.py:482`.

17. **Duże regularne diagramy generuj algorytmicznie z centralnych parametrów układu, a następnie skaluj i pozycjonuj gotową grupę.** Źródła: **2 / 3**. Dowód: `_2026/cross_entropy/transformer_render.py:38`.

18. **Ruch kamery zapisuj jako jawną sekwencję etapów lub wydziel do helpera**, gdy kamera jest częścią objaśnienia. Źródła: **2 / 2**. Dowód: `_2024/holograms/diffraction.py:451`.

### Dane, obliczenia i koszt renderowania

19. **Oddzielaj model lub dane źródłowe od ich projekcji na mobjecty i zasilaj wszystkie reprezentacje jednym źródłem prawdy.** Źródła: **17 / 21**. Sol dodatkowo wydziela węższą wersję „jedna funkcja modelu dla wszystkich wykresów, pól i obliczeń” (**4**). Dowód: `_2018/div_curl.py:1144`.

20. **Statyczne dane obliczaj przed budową geometrii, a dane rzeczywiście zależne od animowanego stanu aktualizuj w updaterze, `always_redraw` lub jawnej pętli klatkowej.** Terra ujmuje oba przypadki jedną regułą (**12**); Sol rozdziela dane statyczne (**8**) i dynamiczne (**12**). Dowód: `_2022/quintic/polynomial_baisics.py:853`.

21. **Ciężkie dane, modele i przygotowane assety trzymaj poza kodem choreografii sceny; scena ma je wczytywać i materializować.** Źródła: **6 / 4**. Dowód: `_2025/colliding_blocks_v2/supplements.py:922`.

22. **Kosztowne wyniki modeli i próbkowań przygotowuj lub cache’uj poza wielokrotnie wywoływanym callbackiem i pętlą renderu.** Źródła: **3 / 4**. Dowód: `_2026/cross_entropy/next_char.py:244`.

23. **Gęstość próbkowania, rozdzielczość, horyzont obliczeń i poziom jakości wystawiaj jako parametry**, aby rozdzielić render roboczy od produkcyjnego. Źródła: **3 / 2**. Dowód: `_2018/div_curl.py:399`.

24. **Ustalaj seed albo przekazuj generator losowy jawnie, gdy losowość wpływa na finalny obraz.** Źródła: **3 / 3**. Dowód: `_2024/puzzles/added_dimension.py:1320`.

### Tempo i synchronizacja

25. **Parametryzuj tempo powtarzalnej choreografii lokalną stałą, argumentem helpera albo atrybutem wariantu**, zamiast rozrzucać magiczne czasy. Źródła: **21 / 20**. Dowód: `_2017/eoc/chapter2.py:12`.

26. **Wyprowadzaj czas sekwencji z liczby elementów, długości ścieżki, rozmiaru przewijanej treści lub czasu modelu.** Terra ujmuje te przypadki razem (**8**); Sol osobno liczy skalę treści (**6**) i powiązanie `run_time` z czasem modelu (**5**). Dowód: `_2023/clt/galton_board.py:378`.

27. **Rozdzielaj całkowity czas ujęcia od lokalnych przedziałów `time_span` animacji równoległych.** Źródła: **2 / 2**. Dowód: `_2026/print_gallery/exponential.py:177`.

## 2. Tylko w jednej

### Tylko Terra

**Brak samodzielnych reguł bez odpowiednika w Sol.** Wszystkie 28 reguł głównych Terry są obecne w Sol, choć Sol czasem scala dwie reguły Terry w jedną, czasem rozbija jedną regułę Terry na kilka, a czasem przesuwa jej wyjątek do sekcji sprzeczności. Jedyny charakterystyczny dla Terry akcent — jawne animacje dla kroków narracyjnych zamiast updaterów — zachowano w regule zgodnej nr 8 jako doprecyzowanie pochodzące z Terry.

### Tylko Sol

Poniższych reguł nie ma w Terrze jako zaakceptowanych, samodzielnych idiomów. Nie są tu rangowane jakościowo.

1. **Przenoś wspólną geometrię, dane i konfigurację kamery do `setup()` klasy bazowej, a `construct()` zostaw dla choreografii ujęcia.** Źródła: **9**. Dowód: `_2023/convolutions2/continuous.py:1043`.

2. **Trzymaj suplementy, plansze przejściowe i reakcje w osobnym module od głównego przebiegu filmu.** Źródła: **6**. Dowód: `_2022/convolutions/supplements.py:1`.

3. **Oddzielaj moduły scen tematycznych, moduły konstrukcji współdzielonych i manifest kolejności renderowania.** Źródła: **3**. Dowód: `_2019/diffyq/all_part1_scenes.py:1`.

4. **Dobieraj klasę bazową sceny do rodzaju ujęcia** — np. dialogu, zwykłej planszy lub osadzonego wideo. Źródła: **1**. Dowód: `_2022/puzzles/subsets.py:209`.

5. **Przy wielodziedziczeniu inicjalizuj jawnie każdego rodzica dostarczającego niezależny stan**, jeśli `setup()` nie tworzy kooperacyjnego łańcucha. Źródła: **1**. Dowód: `_2018/div_curl.py:2909`.

6. **Enkapsuluj powtarzalny efekt czasowy w parametryzowanej klasie `Animation`.** Źródła: **1**. Dowód: `_2024/puzzles/max_rand.py:4`.

7. **Kopiuj już zainicjalizowany kosztowny obiekt wraz z jego stanem renderującym**, zamiast odtwarzać inicjalizację. Źródła: **1**. Dowód: `_2024/holograms/diffraction.py:745`.

8. **Przełączaj kierunek dwustronnej zależności jawnymi metodami, usuwając poprzednie wiązanie przed włączeniem nowego.** Źródła: **2**. Dowód: `_2022/quintic/roots_and_coefs.py:457`.

9. **Rozdzielaj rzeczywiście niezależne wymiary stanu na osobne trackery.** Źródła: **2**. Dowód: `_2025/colliding_blocks_v2/blocks.py:118`.

10. **Synchronizuj wewnętrzne zegary reprezentacji przed crossfadem lub zmianą widoku.** Źródła: **1**. Dowód: `_2023/optics_puzzles/driven_harmonic_oscillator.py:628`.

11. **Usuwaj z dynamicznego kontenera elementy, które trwale opuściły kadr.** Źródła: **1**. Dowód: `_2024/antp/main.py:53`.

12. **Przenoś informację między reprezentacjami przez kopię widocznego obiektu lub jego semantycznej części.** Źródła: **3**. Dowód: `_2025/grover/clarification.py:328`.

13. **Transformuj równania poprzez rozpoznawalne podwyrażenia, zamiast zastępować cały zapis nowym obiektem.** Źródła: **1**. Dowód: `_2023/clt_proof/main.py:139`.

14. **Pozostawiaj źródłowe podobiekty na scenie do zakończenia wszystkich transformacji, które ich używają.** Źródła: **1**. Dowód: `_2023/clt_proof/main.py:136`.

15. **Oddzielaj algorytm animacji od źródła danych przez wymienialne metody lub funkcje dostarczające osie, próbki i przykłady.** Źródła: **3**. Dowód: `_2023/convolutions2/continuous.py:375`.

16. **Dopasowuj wielowartościowe wyniki numeryczne do poprzednich pozycji, zamiast ufać niestabilnej kolejności indeksów.** Źródła: **1**. Dowód: `_2022/quintic/roots_and_coefs.py:62`.

17. **Przekazuj wynik poprzedniej iteracji jako dane wejściowe następnej.** Źródła: **1**. Dowód: `_2023/convolutions2/continuous.py:1896`.

18. **Przenoś obliczenia per-piksel do shadera, pozostawiając CPU dla geometrii pomocniczej.** Źródła: **1**. Dowód: `_2024/holograms/diffraction.wgsl:52`.

19. **Zwiększaj liczbę aktywnych danych stopniowo zamiast od razu renderować pełny ogromny zbiór.** Źródła: **1**. Dowód: `_2024/holograms/diffraction.py:3496`.

20. **Zewnętrzne źródło wideo otwieraj w `setup()`, zamykaj w `tear_down()`, a ekstrakcję klatek wydzielaj do metody.** Źródła: **1**. Dowód: `_2024/holograms/model.py:16`.

21. **Przycinaj przemapowaną geometrię do docelowego obszaru przed animacją.** Źródła: **1**. Dowód: `_2026/print_gallery/exponential.py:3191`.

22. **Nie uruchamiaj kosztownego eksperymentu ani interaktywnego wykresu podczas importu modułu scen.** Źródła: **1**. Dowód: `_2024/transformers/almost_orthogonal.py:22`.

23. **Po pokazaniu kilku wolnych przykładów przechodź do masowej fazy z uproszczonym odświeżaniem stanu.** Źródła: **2**. Dowód: `_2023/clt/main.py:3266`.

24. **Wyznaczaj czas zdarzenia z modelu analitycznego i używaj go do wspólnej synchronizacji obrazu oraz dźwięku.** Źródła: **1**. Dowód: `_2025/colliding_blocks_v2/blocks.py:69`.

25. **Oznaczaj pauzy odpowiadające konkretnym punktom komentarza narracyjnego nazwanym argumentem.** Źródła: **1**. Dowód: `_2022/puzzles/subsets.py:893`.

## 3. Rozbieżności

### Te same decyzje, inne wersje

| Temat | Terra | Sol |
|---|---|---|
| **Granica sceny** | Osobna klasa dla niezależnego beatu: **13** źródeł; długi rozdział stanowy w jednej klasie jest kontrprzykładem bez mierzalnego progu decyzji. | Osobna klasa: **12** źródeł; dodatkowo jawne kryterium z `_2022/puzzles/subsets.py:872`: wspólny stan przemawia za fazami jednej sceny, niezależne cięcie za osobną klasą. |
| **Źródło prawdy o stanie** | Jeden tracker: **16** źródeł; alternatywą jest stan zapisany w pozycjach obiektów w `_2022/quintic/roots_and_coefs.py:445`. | Jeden `ValueTracker`: **15** źródeł; obok stanu w pozycjach wskazuje trzeci wariant — osobne trackery dla niezależnych wymiarów czasu, fizyki i prezentacji. |
| **Mechanizm ciągłej zależności** | Updatery lub `always_redraw` są wzorcem większości źródeł; `_2016/eola/chapter10.py:1081` używa jawnej pętli klatkowej. | Tracker z updaterem lub `always_redraw`: **15** źródeł; ten sam kontrprzykład EOLA. Obie syntezy zaznaczają, że nie wiadomo, czy różnica wynika z projektu, czy z epoki API. |
| **Miejsce obliczeń** | Jedna warunkowa reguła: statyczne dane przed geometrią, dynamiczne w updaterze; **12** źródeł. | Dwie osobne reguły: statyczne przed geometrią (**8**) i dynamiczne w updaterze/`always_redraw`/pętli (**12**), plus cache jako trzeci przypadek. Sol umieszcza temat również w „Sprzecznościach”. |
| **Układ relacyjny a kalibracja absolutna** | Układ relacyjny: **21** źródeł; wyjątek to jawne pozycje i rozmiary warstw rastrowych w `_2026/print_gallery/exponential.py:155`. Brak progu przejścia w tryb pikselowy. | Układ relacyjny: **21** źródeł; wyjątek staje się osobną pozytywną regułą (**2**) i obejmuje też punkty adnotacji fotografii z `_2024/holograms/supplements.py:87`. |
| **Gotowy asset a generowanie proceduralne** | Generowanie z modelu ilustruje `_2019/diffyq/part2/fourier_series.py:240`, gotową planszę `_2022/puzzles/subsets.py:2232`; brak rozstrzygnięcia kosztu utrzymania i jakości. | Gotową planszę ilustruje ten sam plik puzzles, generowanie funkcji `_2025/laplace/integration.py:35`; także nie podaje globalnego zwycięzcy. |
| **Własność parametrów tempa** | Lokalna stała, argument helpera i atrybut wariantu są jedną regułą obecną we wszystkich **21** źródłach. | Centralizacja powtarzalnego przebiegu dotyczy **20** źródeł, wszystkich poza EOLA; lokalny czas konkretnego beatu w `_2016/eola/chapter1.py:78` jest przedstawiony jako przeciwna praktyka. |
| **Metadane przy obiekcie a równoległe kolekcje** | Preferuje nazwy lub metadane domenowe na obiekcie zamiast kruchych indeksów; **6** źródeł. | Pokazuje również uzasadnioną alternatywę: niezależne trackery w kolekcji indeksowanej tak samo jak grupa obiektów, `_2023/optics_puzzles/slowing_waves.py:39`. |
| **Ścieżki absolutne** | „Nie zaszywaj absolutnej ścieżki autora” zostaje świadomie odsiane jako ogólna jakość repozytorium, nie idiom Manima. | Ta sama zasada trafia do katalogu głównego jako reguła scenowa z **9** źródłami; dowód: `_2022/puzzles/subsets.py:4480`. |

### Niezgodne liczby źródeł

Poza tematami z tabeli liczby różnią się także dla wielu reguł zgodnych. Najważniejsze pary **T / S** to: fazowanie `construct()` **6 / 5**, warianty scen **19 / 18**, atrybuty sceny **10 / 8**, zarządzanie updaterami **12 / 15**, zapis stanu/targetu **6 / 8**, grupowanie semantyczne **16 / 14**, generowanie regularnych układów **2 / 3**, jedno źródło danych **17 / 21**, ciężkie dane poza choreografią **6 / 4**, cache **3 / 4**, parametry jakości **3 / 2** i czas zależny od skali danych **8 / 6**. Przy mapowaniu pozycji obie syntezy podają **5**, lecz Terra wlicza `_2023-gauss_int`, a Sol `_2018-div_curl`.

Te różnice nie powinny być automatycznie interpretowane jako różnica siły dowodu. Najpierw trzeba zunifikować definicję „źródła”, zakres reguły oraz sposób liczenia projektu, modułu i pojedynczej obserwacji.

## 4. Różnice w podejściu

### Charakter opracowań

- **Terra — 101 linii.** Kompresuje materiał do 28 szerokich reguł głównych, mocniej oddziela idiomy konstrukcji scen od ogólnej higieny Pythona i repozytorium, a sprzeczności opisuje jako pięć dużych osi decyzyjnych. Ostrzej pokazuje warunki obowiązywania reguł i ryzyko fałszywej uniwersalizacji. Gubi część mechaniki szczegółowej: cykl życia wideo, shadery, stabilizowanie wyników numerycznych, synchronizację zegarów i dźwięku, manifesty renderowania oraz wyspecjalizowane typy scen.

- **Sol — 385 linii.** Rozbija materiał na 59 reguł głównych i zachowuje wiele idiomów operacyjnych opartych nawet na jednym źródle. Ostrzej widzi cykl życia zasobów, wydajność, szczegóły numeryczne, ciągłość transformacji, stan wielowymiarowy i synchronizację. Gubi część granicy między idiomem Manima a ogólną jakością kodu; przykładem są ścieżki absolutne i zachowanie przy imporcie. Szersza granularność zwiększa też liczbę pozycji, które są raczej hipotezami specjalistycznymi niż regułami ogólnymi.

### Filtr „odsiane jako banał”

Terra odrzuca **44 z 324 obserwacji**, Sol **39 surowych obserwacji**. W obu odrzucane są puste sceny/`pass`, kod po bezwarunkowym `return`, mutowalne wartości domyślne, stare kopie lub TODO i podobna higiena. Pełny ślad przykładów z obu syntez:

- samo stwierdzenie, że `VGroup` grupuje elementy, bez semantycznego cyklu życia;
- przekazywanie identycznego słownika `run_time` do kilku animacji;
- kod po bezwarunkowym `return`;
- `pass`, TODO i puste sceny w kodzie produkcyjnym;
- mutowalna lista jako wartość domyślna;
- absolutne ścieżki autora — Terra odrzuca, Sol awansuje do reguły, co odnotowano wyżej;
- nieużywane obiekty lub parametry;
- cykliczne zależności modułów;
- stare kopie, zakomentowane alternatywy i przestarzałe mechanizmy;
- ponowne wykonywanie identycznej operacji układu.

### Ograniczenia materiału, których nie wolno zgubić przy awansie

Obie syntezy wskazują brak danych o intencji i kryteriach narracyjnych, jakości finalnego ruchu i czytelności kadru, dostępności, profilach wydajności, wersjach Manima i środowisku odtwarzania, walidacji lub regresji wizualnej oraz prawach i pochodzeniu assetów. Z kodu nie wynika więc, że częsty wzorzec był dobry ani że nadal jest aktualny.

Terra dodatkowo akcentuje brak budżetów pamięci i czasu, procedury QA assetów, alternatyw tekstowych oraz reprodukowalności danych zewnętrznych. Sol dopowiada brak powiązania z lektorem, wiedzy o odrzuconych alternatywach, wyników dydaktycznych i retencji, opisu docelowej widowni, oceny poprawności matematycznej, interpretacji elementów roboczych, informacji o dźwięku i montażu końcowym oraz dowodu przenośności poza styl i pipeline 3Blue1Brown.

## 5. Rekomendacja kolejności przeglądu

1. **Najpierw przeczytać reguły zgodne 1–27**, zaczynając od tych z co najmniej 10 źródłami w obu syntezach: granice scen, ponowne użycie, tracker/updatery, układ relacyjny, grupowanie semantyczne, jedno źródło danych i parametryzacja tempa.

2. **Następnie rozstrzygnąć dziewięć rozbieżności tematycznych.** Dla biblioteki najlepiej zapisać je jako reguły warunkowe lub drzewka decyzji: wspólny stan kontra niezależne cięcie, jeden tracker kontra niezależne wymiary, layout relacyjny kontra kalibracja rastrowa, statyczne kontra dynamiczne obliczenia, asset kontra generowanie.

3. **Przed użyciem liczby źródeł jako rankingu ujednolicić liczenie.** Różnice **13/12**, **16/15**, **17/21** czy **21/20** pokazują, że obie syntezy miały inne granice kategorii.

4. **Potem przejrzeć reguły tylko-Sol z co najmniej trzema źródłami:** `setup()` klasy bazowej, moduły suplementów, manifest renderowania, ciągłość przez kopię widocznego obiektu i wymienialne źródła danych. To najszybszy sposób poszerzenia rdzenia bez zaczynania od przypadków jednostkowych.

5. **Na końcu przejrzeć reguły tylko-Sol z jednym lub dwoma źródłami** jako kandydatów specjalistycznych: shadery, wideo, stabilizacja wyników numerycznych, clipping, synchronizacja zegarów i dźwięku, własna klasa `Animation` oraz masowa faza prezentacji.

6. **Oddzielnie zdecydować o zasadach higieny repozytorium.** Jeśli mają zostać zachowane, powinny trafić do standardu inżynierskiego obok biblioteki idiomów Manima, z jawną decyzją, czy wyjątkiem są ścieżki absolutne i kosztowne działania przy imporcie.

7. **Przed ostatecznym awansem zweryfikować kandydatów w kodzie i renderach.** Priorytetem są zgodność z aktualną wersją API, wizualna regresja, profil renderu, poprawność matematyczna, dostępność, synchronizacja z lektorem oraz licencje i reprodukowalność assetów.

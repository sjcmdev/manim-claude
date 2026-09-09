# Źródło prawdy i czas w updaterach

- **Wyliczaj stan zależny z bieżącej geometrii lub trackera i nie używaj do tego `dt`.**
  - **Źródła (23):** _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, mf_tools, uwezi.
  - **Dowód:** `part2/heat_equation.py:102`.
  - **Kiedy:** Gdy bieżący stan źródła jednoznacznie wyznacza położenie, wartość lub geometrię obiektu zależnego.

- **Używaj `dt` wyłącznie do całkowania czasu, prędkości lub innego przyrostowego stanu.**
  - **Źródła (14):** _2018-div_curl, _2022-convolutions, _2022-puzzles, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, uwezi.
  - **Dowód:** `objects.py:181`.
  - **Kiedy:** Gdy wynik zależy od upływu czasu i nie można go odtworzyć wyłącznie z aktualnego trackera.

- **Odtwarzaj złożoną geometrię z aktualnych danych przez `always_redraw`, `become` lub funkcję budującą, zamiast kumulować deformacje.**
  - **Źródła (18):** _2018-div_curl, _2019-diffyq, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, mf_tools, uwezi.
  - **Dowód:** `continuous.py:165`.
  - **Kiedy:** Gdy zmiana obejmuje punkty, liczbę części albo cały kształt i pełna rekonstrukcja jest prostsza niż mutacja fragmentów.

- **Przechowuj stan między klatkami tylko wtedy, gdy proces rzeczywiście zależy od historii.**
  - **Źródła (15):** _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-puzzles, _2022-quintic, _2023-gauss_int, _2023-optics_puzzles, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-grover, _2025-laplace, _2026-cross_entropy, abul4fia.
  - **Dowód:** `polynomial_baisics.py:1439`.
  - **Kiedy:** Gdy powstaje ślad, całkowana trajektoria, stan dyskretny, przekroczenie progu albo ciągłość gałęzi funkcji.

- **Rozdzielaj updater źródła lub stanu od updaterów jego wizualizacji.**
  - **Źródła (6):** _2019-diffyq, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-transformers, uwezi.
  - **Dowód:** `ml_basics.py:2213`.
  - **Kiedy:** Gdy jedna wartość napędza kilka reprezentacji albo poszczególne właściwości mają odmienne zależności.

- **W updaterach tworzonych w pętli wiąż indeks i inne wartości iteracji w argumentach domyślnych domknięcia.**
  - **Źródła (2):** _2026-cross_entropy, _2026-print_gallery.
  - **Dowód:** `language_tree.py:417`.
  - **Kiedy:** Gdy każdy z wielu updaterów ma zapamiętać inny indeks, obiekt albo parametr.

- **Dziel duże `dt` na mniejsze kroki przed numerycznym całkowaniem dynamiki.**
  - **Źródła (1):** _2023-optics_puzzles.
  - **Dowód:** `driven_harmonic_oscillator.py:37`.
  - **Kiedy:** Gdy updater rozwiązuje równanie ruchu, a stabilność integracji zależy od długości kroku.

- **Wykonaj updater natychmiast po podpięciu, jeśli stan początkowy musi być poprawny przed pierwszą klatką.**
  - **Źródła (1):** uwezi.
  - **Dowód:** `20230605_zoomed.py:33`.
  - **Kiedy:** Gdy domyślna geometria lub tekst nie odpowiada początkowej wartości źródła.

# Struktura i cykl życia updaterów

- **Zawieszaj, czyść i wznawiaj updatery jawnie na granicach ręcznych transformacji i zmian roli obiektu.**
  - **Źródła (17):** _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-quintic, _2023-clt, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia.
  - **Dowód:** `embedding.py:2898`.
  - **Kiedy:** Gdy updater konkurowałby z `Transform`, statyczną kopią, usunięciem kotwicy albo ponownym użyciem obiektu.

- **Używaj nazwanej funkcji do wieloetapowej aktualizacji, a lambdy tylko do pojedynczego, lokalnego powiązania.**
  - **Źródła (12):** _2018-div_curl, _2019-diffyq, _2022-quintic, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2024-antp, _2024-holograms, _2024-puzzles, _2025-colliding_blocks_v2, _2025-laplace, uwezi.
  - **Dowód:** `integral.py:248`.
  - **Kiedy:** Gdy trzeba dobrać formę updatera do liczby operacji, liczby części i możliwości ponownego użycia.

- **Używaj `UpdateFromFunc` lub `UpdateFromAlphaFunc` zamiast trwałego updatera dla zależności obowiązującej tylko podczas jednego przejścia.**
  - **Źródła (4):** _2016-eola, _2023-clt, _2023-optics_puzzles, _2025-laplace.
  - **Dowód:** `dice_sims.py:181`.
  - **Kiedy:** Gdy po zakończeniu konkretnego `play` zależność nie powinna już działać.

- **Ustalaj kolejność updaterów zgodnie z przepływem danych: najpierw producent, potem konsument.**
  - **Źródła (2):** _2022-quintic, _2023-optics_puzzles.
  - **Dowód:** `adding_waves.py:808`.
  - **Kiedy:** Gdy wynik jednego updatera jest wejściem drugiego albo ponowne dodawanie obiektów zmienia kolejność aktualizacji.

- **Modeluj krótkotrwały efekt zdarzeniowy jako samousuwający się updater z czasem rozpoczęcia.**
  - **Źródła (1):** _2025-colliding_blocks_v2.
  - **Dowód:** `blocks.py:1102`.
  - **Kiedy:** Gdy błysk lub reakcja jest uruchamiana przez zdarzenie wykrywane poza liniowym przebiegiem `play`.

- **Usuwaj element strumienia po opuszczeniu kadru i natychmiast przerywaj jego dalszą aktualizację.**
  - **Źródła (1):** _2024-antp.
  - **Dowód:** `main.py:53`.
  - **Kiedy:** Gdy updater obsługuje potencjalnie długi strumień przewijanych obiektów.

# Wybór abstrakcji animacji

- **Składaj gotowe animacje zamiast tworzyć podklasę `Animation`, jeśli efekt nie wnosi własnego algorytmu klatkowego.**
  - **Źródła (14):** _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-puzzles, _2025-laplace.
  - **Dowód:** `subsets.py:60`.
  - **Kiedy:** Gdy ruch jest kombinacją transformacji, wejść, wyjść, updaterów lub zmian trackerów.

- **Twórz własną klasę `Animation` dla nowej logiki wykonywanej w każdej klatce, zwłaszcza dyskretnej, losowej albo wieloparametrowej.**
  - **Źródła (6):** _2016-eola, _2024-puzzles, _2025-colliding_blocks_v2, _2025-grover, mf_tools, uwezi.
  - **Dowód:** `max_rand.py:4`.
  - **Kiedy:** Gdy stan pośredni nie daje się opisać zwykłą transformacją celu ani lokalnym callbackiem.

- **Ograniczaj własną klasę do `__init__` i `interpolate_mobject`, jeśli standardowy początek, koniec i sprzątanie wystarczają.**
  - **Źródła (5):** _2016-eola, _2024-puzzles, _2024-transformers, mf_tools, uwezi.
  - **Dowód:** `helpers.py:630`.
  - **Kiedy:** Gdy cała nowość animacji mieści się w obliczeniu stanu dla danego `alpha`.

- **Przywracaj `starting_mobject` lub niezależną kopię bazową przed transformacjami zależnymi od `alpha`.**
  - **Źródła (2):** mf_tools, uwezi.
  - **Dowód:** `animations.py:26`.
  - **Kiedy:** Gdy kolejne klatki stosują skalowanie, obrót lub przesunięcie i nie mogą dziedziczyć deformacji z poprzedniej klatki.

- **Przyjmuj parametry własnej animacji jawnie i przekazuj niezużyte `kwargs` do konstruktora bazowego.**
  - **Źródła (3):** _2016-eola, _2024-puzzles, _2025-colliding_blocks_v2.
  - **Dowód:** `max_rand.py:5`.
  - **Kiedy:** Gdy animacja ma własne dane wejściowe, lecz nadal powinna respektować standardowe ustawienia `run_time`, `rate_func` i cyklu życia.

- **Steruj postępem istniejącej animacji przez jawne `begin()` i `interpolate_mobject`, jeśli kontrolę nad `alpha` ma przejąć tracker.**
  - **Źródła (1):** _2026-cross_entropy.
  - **Dowód:** `robot.py:7916`.
  - **Kiedy:** Gdy postęp transformacji ma być odłączony od czasu pojedynczego `play`.

# Choreografia i tempo

- **Grupuj równoległe ruchy opisujące jedno zdarzenie, a kolejne kroki narracyjne rozdzielaj na osobne fazy.**
  - **Źródła (24):** _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, mf_tools, uwezi.
  - **Dowód:** `main.py:242`.
  - **Kiedy:** Gdy synchronizacja ma wyrażać wspólny sens, a nie tylko techniczną możliwość równoległego wykonania.

- **Wprowadzaj powtarzalne elementy falą, dobierając `lag_ratio` lub okna czasowe do kolejności czytania.**
  - **Źródła (16):** _2016-eola, _2017-eoc, _2019-diffyq, _2022-convolutions, _2022-quintic, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery.
  - **Dowód:** `integral.py:104`.
  - **Kiedy:** Gdy kolejność elementów niesie informację albo jednoczesne wejście tworzyłoby nieczytelny blok.

- **Dobieraj `rate_func` do znaczenia ruchu: `linear` do czasu i skanowania, a `there_and_back` lub `wiggle` do chwilowego akcentu.**
  - **Źródła (23):** _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, mf_tools, uwezi.
  - **Dowód:** `integral.py:521`.
  - **Kiedy:** Gdy tempo ma komunikować charakter zjawiska, a nie być wyłącznie ozdobnym easingiem.

- **Przygotuj kompletny `target` przed `MoveToTarget`, gdy grupa zmienia naraz układ, skalę, położenie i styl.**
  - **Źródła (4):** _2023-clt_proof, _2023-convolutions2, _2024-antp, _2026-print_gallery.
  - **Dowód:** `dice.py:322`.
  - **Kiedy:** Gdy wiele współzależnych właściwości powinno dotrzeć do spójnego stanu końcowego.

- **Mapuj semantycznie odpowiadające sobie fragmenty wzorów, a elementy bez pary wprowadzaj lub usuwaj osobno.**
  - **Źródła (9):** _2022-quintic, _2023-clt_proof, _2023-gauss_int, _2024-antp, _2026-cross_entropy, _2026-print_gallery, abul4fia, mf_tools, uwezi.
  - **Dowód:** `transform_matching_slices.py:18`.
  - **Kiedy:** Gdy obie reprezentacje mają częściowo wspólną strukturę i automatyczne dopasowanie nie wystarcza.

# Wejście i kierowanie uwagą

- **Przekształcaj obiekt w semantycznego następcę zamiast wygaszać go i niezależnie tworzyć nowy.**
  - **Źródła (24):** _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, mf_tools, uwezi.
  - **Dowód:** `subsets.py:3703`.
  - **Kiedy:** Gdy widz powinien odczytać kolejną formę jako rozwinięcie, wynik lub zmianę reprezentacji poprzedniej.

- **Wprowadzaj główną geometrię i adnotacje odmiennymi gestami oraz w osobnych momentach.**
  - **Źródła (23):** _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, uwezi.
  - **Dowód:** `chapter1.py:78`.
  - **Kiedy:** Gdy obiekt merytoryczny ma najpierw ustanowić zjawisko, a tekst, rama lub strzałka dopiero je nazwać.

- **Wyprowadzaj adnotację lub wynik z punktu, kierunku albo kopii obiektu, do którego się odnosi.**
  - **Źródła (19):** _2017-eoc, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, mf_tools, uwezi.
  - **Dowód:** `diagonal_slices.py:189`.
  - **Kiedy:** Gdy przestrzenne pochodzenie nowego elementu pomaga wyjaśnić jego związek ze źródłem.

- **Przygaszaj nadal potrzebny kontekst zamiast usuwać go ze sceny.**
  - **Źródła (17):** _2016-eola, _2017-eoc, _2018-div_curl, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery.
  - **Dowód:** `integral.py:79`.
  - **Kiedy:** Gdy poprzednia konstrukcja pozostaje punktem odniesienia, ale nie powinna konkurować z aktualnym tematem.

- **Zostawiaj półprzezroczyste kopie poprzednich stanów, jeśli historia zmiany jest częścią argumentu.**
  - **Źródła (5):** _2023-gauss_int, _2024-puzzles, _2024-transformers, _2025-laplace, _2026-print_gallery.
  - **Dowód:** `supplements.py:1093`.
  - **Kiedy:** Gdy odbiorca powinien porównywać trajektorię, położenie lub kolejne warianty, a nie tylko stan bieżący.

- **Wyróżnij fragment przed jego zastąpieniem lub odrzuceniem.**
  - **Źródła (2):** _2023-clt_proof, _2024-antp.
  - **Dowód:** `main.py:1007`.
  - **Kiedy:** Gdy widz musi najpierw zidentyfikować element, którego dotyczy następna operacja.

# Sprzątanie i przekazywanie stanu

- **Sprzątaj powiązane obiekty tymczasowe jako jedną fazę i jednocześnie przygotowuj trwały stan następnego kroku.**
  - **Źródła (19):** _2016-eola, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt_proof, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, mf_tools, uwezi.
  - **Dowód:** `integral.py:824`.
  - **Kiedy:** Gdy ramki, etykiety, linie i kopie tracą funkcję razem, a scena ma od razu osiągnąć kolejny stan roboczy.

- **Po transformacji przez kopię usuń obiekt przejściowy i ustanów kanoniczny obiekt docelowy jako nowy korzeń sceny.**
  - **Źródła (5):** _2016-eola, _2022-puzzles, _2023-clt, _2024-transformers, mf_tools.
  - **Dowód:** `chapter11.py:306`.
  - **Kiedy:** Gdy następne kroki mają działać na stabilnej hierarchii, a nie na submobjectach pozostałych po transformacji.

- **Używaj samoczyszczącego cyklu tworzenia i zaniku dla markerów, śladów i diagnostycznych podświetleń.**
  - **Źródła (6):** _2018-div_curl, _2019-diffyq, _2022-convolutions, _2023-clt_proof, _2025-grover, mf_tools.
  - **Dowód:** `discrete.py:439`.
  - **Kiedy:** Gdy obiekt ma istnieć tylko przez czas jednego akcentu i nie może pozostać w hierarchii sceny.

- **Przenieś czas, wartość albo wynik do trwałego następcy przed usunięciem obiektu dynamicznego.**
  - **Źródła (2):** _2023-clt, _2023-optics_puzzles.
  - **Dowód:** `bending_waves.py:397`.
  - **Kiedy:** Gdy nowy obiekt reprezentuje dalszy ciąg tego samego procesu i powinien rozpocząć od identycznego stanu.

# Projektowanie API własnych mobjectów

- **Parametryzuj geometrię, styl i zachowanie w konstruktorze lub konfiguracji, zamiast kodować osobne warianty.**
  - **Źródła (24):** _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, mf_tools, uwezi.
  - **Dowód:** `part1/pendulum.py:6`.
  - **Kiedy:** Gdy obiekt ma być używany ponownie w innych rozmiarach, kolorach, orientacjach lub konfiguracjach modelu.

- **Eksponuj semantyczne części jako stabilne dzieci, nazwane atrybuty albo jawne akcesory.**
  - **Źródła (22):** _2016-eola, _2017-eoc, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, mf_tools, uwezi.
  - **Dowód:** `robot.py:21`.
  - **Kiedy:** Gdy scena będzie niezależnie animować, stylować, aktualizować lub odpytywać części kompozytu.

- **Rozdziel kontrakty metod: fabryka tworzy nowy obiekt, mutator zmienia istniejący, akcesor zwraca dane lub widok, a metoda czynności zwraca animację.**
  - **Źródła (16):** _2016-eola, _2019-diffyq, _2022-convolutions, _2022-quintic, _2023-clt, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2026-cross_entropy, _2026-print_gallery, mf_tools, uwezi.
  - **Dowód:** `distribution.py:52`.
  - **Kiedy:** Gdy klasa udostępnia jednocześnie konstrukcję geometrii, zmianę stanu i własny język ruchów.

- **Używaj parametryzowanej fabryki zwracającej `Group` lub `VGroup`, jeśli obiekt jest wyłącznie kompozycją istniejących mobjectów.**
  - **Źródła (9):** _2018-div_curl, _2022-puzzles, _2022-quintic, _2023-clt_proof, _2024-antp, _2024-holograms, _2024-puzzles, _2025-colliding_blocks_v2, _2026-print_gallery.
  - **Dowód:** `subsets.py:6`.
  - **Kiedy:** Gdy kompozycja nie potrzebuje własnego cyklu życia, stanu ani zachowania uzasadniającego nową klasę.

- **Zwracaj `self` z setterów i mutatorów przeznaczonych do łańcuchowania lub `.animate`.**
  - **Źródła (10):** _2019-diffyq, _2023-clt, _2023-gauss_int, _2023-optics_puzzles, _2024-holograms, _2024-transformers, _2025-laplace, _2026-cross_entropy, mf_tools, uwezi.
  - **Dowód:** `objects.py:478`.
  - **Kiedy:** Gdy operacja zmienia istniejący obiekt i ma być składana z innymi zmianami.

- **Aktualizuj stabilne dzieci w miejscu przy zmianie danych, a twórz nowy obiekt dopiero przy zmianie struktury lub znaczenia.**
  - **Źródła (6):** _2019-diffyq, _2023-clt, _2023-gauss_int, _2025-grover, _2026-print_gallery, uwezi.
  - **Dowód:** `main.py:59`.
  - **Kiedy:** Gdy trzeba zachować tożsamość i updatery istniejących części, ale nie kosztem ukrywania rzeczywistej zmiany strukturalnej.

- **Buduj punkty prawdziwego własnego `VMobject` w konstruktorze lub `init_points` i wystawiaj charakterystyczne punkty przez akcesory.**
  - **Źródła (5):** _2016-eola, _2017-eoc, abul4fia, mf_tools, uwezi.
  - **Dowód:** `chapter6.py:152`.
  - **Kiedy:** Gdy podstawową reprezentacją obiektu jest własna krzywa lub zbiór punktów, a nie kompozycja gotowych mobjectów.

- **Umieszczaj autonomiczną dynamikę wewnątrz obiektu i wystawiaj scenie jawne sterowanie jej cyklem życia.**
  - **Źródła (8):** _2018-div_curl, _2019-diffyq, _2023-optics_puzzles, _2024-holograms, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, uwezi.
  - **Dowód:** `shm.py:46`.
  - **Kiedy:** Gdy updater jest częścią modelu obiektu, a nie jednorazową zależnością konkretnej sceny.

- **Dołączaj dekorację jako dziecko właściciela, jeśli ma dzielić z nim transformacje i cykl życia.**
  - **Źródła (3):** _2024-antp, _2025-grover, _2025-laplace.
  - **Dowód:** `main.py:636`.
  - **Kiedy:** Gdy obrys, etykieta lub wrapper powinny zawsze poruszać się i znikać razem z obiektem bazowym.

- **Oddziel punkty nośne od parametrów renderera i synchronizuj zmienną geometrię z jego buforem danych.**
  - **Źródła (1):** _2024-holograms.
  - **Dowód:** `diffraction.py:43`.
  - **Kiedy:** Gdy wygląd jest liczony przez shader lub renderer z wielu źródeł, a geometria mobjectu służy tylko jako nośnik.

- **Utrzymuj mapę kluczy do submobjectów jako źródło prawdy i synchronizuj ją z hierarchią grupy.**
  - **Źródła (1):** mf_tools.
  - **Dowód:** `dual_compatibility.py:37`.
  - **Kiedy:** Gdy elementy są dodawane i usuwane według kluczy, a indeksy dzieci nie są stabilnym API.

# Sprzeczności

- **Gdzie przechowywać stan historyczny updatera**
  - **Na mobjectcie:** _2018-div_curl (`div_curl.py:368`), _2019-diffyq (`part1/pendulum.py:333`), _2023-optics_puzzles (`objects.py:434`), _2026-cross_entropy (`language_tree.py:754`).
  - **Poza mobjectem, w domknięciu lub modelu:** _2023-gauss_int (`supplements.py:917`), _2024-transformers (`mlp.py:2483`).
  - Jedna strona wiąże historię z wizualnym obiektem, druga utrzymuje stan obliczeniowy niezależnie od niego.

- **Ile updaterów powinno obsługiwać współzależną strukturę**
  - **Rozdzielaj niezależne właściwości:** _2023-convolutions2 (`continuous.py:1102`), _2023-gauss_int (`integral.py:440`), _2024-transformers (`ml_basics.py:2213`).
  - **Przeliczaj całą grupę w jednym updaterze:** _2022-puzzles (`subsets.py:650`), _2022-quintic (`roots_and_coefs.py:465`), _2025-laplace (`exponentials.py:1173`).

- **Czy updater ma działać podczas animowania tego samego obiektu**
  - **Zawieszaj go na czas ręcznej animacji:** m.in. _2024-transformers (`embedding.py:2898`) i _2025-colliding_blocks_v2 (`blocks.py:1706`).
  - **Pozostaw go aktywnym przez `suspend_mobject_updating=False`:** _2023-optics_puzzles (`e_field.py:386`) i _2024-holograms (`diffraction.py:1833`).

- **Kto ma być właścicielem choreografii**
  - **Scena ma budować animacje, a fabryka obiektu tylko geometrię:** _2023-clt_proof (`main.py:497`), _2023-optics_puzzles (`cylinder.py:199`), _2024-puzzles (`added_dimension.py:1486`).
  - **Mobject ma wystawiać gotowe animacje lub sam wykonywać ruch:** _2022-quintic (`roots_and_coefs.py:600`), _2024-transformers (`helpers.py:713`), _2026-cross_entropy (`robot.py:39`).

- **Czy tworzyć własną klasę `Animation`**
  - **Składaj gotowe animacje:** 14 źródeł; reprezentatywnie _2023-convolutions2 (`continuous.py:1919`).
  - **Twórz klasę dla własnej logiki klatkowej:** 6 źródeł; reprezentatywnie _2024-puzzles (`max_rand.py:4`).
  - Granica między „kombinacją efektów” a „nowym algorytmem klatkowym” nie jest w zbiorze zdefiniowana testowalnym kryterium.

- **Czy jawnie dobierać `rate_func`**
  - **Dobieraj ją do semantyki ruchu:** 23 źródła; reprezentatywnie _2023-gauss_int (`integral.py:521`).
  - **Steruj rytmem przez `run_time`, `lag_ratio` i `path_arc`, pozostawiając `rate_func` domyślną:** _2023-clt_proof (`main.py:856`).

# Odsiane jako banał

**6 reguł.**

Przykłady: „Uruchamiaj niezależne ruchy równolegle w jednym `play`” (_2022-quintic), „Składaj równoległe i sekwencyjne ruchy przez `AnimationGroup` oraz `LaggedStart`” (_2026-print_gallery), „Buduj własną klasę `AnimationGroup` przez zebranie animacji składowych” (uwezi) oraz „grupuj równoległe transformacje w `AnimationGroup`” (_2023-clt_proof). Reguły te opisują bezpośrednio kontrakt funkcji, nie decyzję projektową ani jej warunki.

# Czego brakuje

- **Intencji narracyjnej:** z kodu nie wiadomo, jaki błąd rozumowania widza ma usuwać ruch ani dlaczego dana ciągłość, pauza lub akcent są dydaktycznie skuteczne.
- **Powiązania z narracją głosową:** brak danych o synchronizacji z lektorem, długości pauz, rytmie zdań i momentach wymagających czasu na samodzielne odczytanie obrazu.
- **Oceny odbiorców:** nie ma testów z widzami, pomiarów zrozumienia ani informacji, które animacje okazały się mylące mimo poprawnego kodu.
- **Kryteriów czytelności:** brak minimalnych rozmiarów tekstu, kontrastu, bezpiecznych kolorów, zasad dla daltonizmu, napisów i urządzeń o różnych rozdzielczościach.
- **Budżetów wydajnościowych:** kod pokazuje techniki, ale nie określa progów, przy których `always_redraw`, `become`, shadery lub duże hierarchie stają się za wolne albo pamięciożerne.
- **Walidacji skrajnych parametrów:** brak kontraktów dla pustych grup, zerowych długości, nieciągłości, zmian liczby dzieci, ekstremalnego `dt` i błędnych danych wejściowych.
- **Testowania i regresji wizualnej:** zbiór nie mówi o renderach referencyjnych, deterministyczności, testach kluczowych klatek ani wykrywaniu artefaktów między klatkami.
- **Zachowania przy przerwaniu cyklu:** brak reguł dotyczących wyjątków, pominięcia animacji, przewijania, przerwanego renderu i gwarantowanego sprzątania updaterów.
- **Warstwowania i kompozycji:** niewiele jest o `z_index`, kolejności renderowania, przezroczystości, maskowaniu, clippingu, antyaliasingu i nakładaniu obiektów 2D/3D.
- **Kompatybilności wersji:** materiał miesza generacje `manimlib` i różne style API, lecz nie określa, które idiomy są przenośne między wersjami i rendererami.
- **Reprodukowalności:** sporadyczne ziarna losowe nie tworzą polityki deterministycznych symulacji, losowych animacji i porównywalnych renderów.
- **Granicy scena–mobject–model:** kod pokazuje wszystkie trzy warianty własności stanu i choreografii, lecz nie dostarcza danych o kosztach utrzymania ani kryterium wyboru.
- **Względnej wagi czterech obszarów:** niemal równy rozkład 128/118/122/123 wynika najpewniej ze schematu ekstrakcji, więc nie pozwala ocenić, które obszary rzeczywiście dominują w praktyce.
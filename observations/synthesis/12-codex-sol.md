# Granice scen i organizacja materiału

- **Wydzielaj każdy niezależny beat narracyjny lub wstawkę do osobnej klasy sceny.**
  - **Źródła (12):** `_2016-eola`, `_2022-puzzles`, `_2023-clt_proof`, `_2023-gauss_int`, `_2024-antp`, `_2024-holograms`, `_2024-puzzles`, `_2025-colliding_blocks_v2`, `_2025-grover`, `_2025-laplace`, `_2026-cross_entropy`, `_2026-print_gallery`.
  - **Dowód:** `_2016/eola/chapter0.py:64`.
  - **Kiedy:** Gdy fragment ma własny stan początkowy i końcowy albo będzie osobno renderowany i montowany.

- **Przenoś wspólną geometrię, dane i konfigurację kamery do `setup()` klasy bazowej, a `construct()` zostaw dla choreografii konkretnego ujęcia.**
  - **Źródła (9):** `_2017-eoc`, `_2023-clt`, `_2023-convolutions2`, `_2023-gauss_int`, `_2024-holograms`, `_2024-puzzles`, `_2024-transformers`, `_2025-colliding_blocks_v2`, `_2026-print_gallery`.
  - **Dowód:** `_2023/convolutions2/continuous.py:1043`.
  - **Kiedy:** Gdy kilka faz lub podklas korzysta z tych samych osi, trackerów, danych albo ustawień kamery.

- **Trzymaj krótkie suplementy, plansze przejściowe i reakcje w osobnym module od głównego przebiegu filmu.**
  - **Źródła (6):** `_2022-convolutions`, `_2023-gauss_int`, `_2024-holograms`, `_2024-puzzles`, `_2026-cross_entropy`, `_2026-print_gallery`.
  - **Dowód:** `_2022/convolutions/supplements.py:1`.
  - **Kiedy:** Gdy ujęcia pomocnicze są niezależne od stanu głównej konstrukcji i mają osobny cykl montażowy.

- **Rozbijaj długi `construct()` na nazwane metody fazowe wywoływane w kolejności narracji.**
  - **Źródła (5):** `_2016-eola`, `_2017-eoc`, `_2018-div_curl`, `_2019-diffyq`, `_2022-puzzles`.
  - **Dowód:** `_2016/eola/chapter8.py:113`.
  - **Kiedy:** Gdy kolejne etapy współdzielą obiekty i dlatego nie powinny stać się osobnymi scenami.

- **Oddzielaj moduły scen tematycznych, moduły konstrukcji współdzielonych i manifest kolejności renderowania.**
  - **Źródła (3):** `_2017-eoc`, `_2019-diffyq`, `_2024-transformers`.
  - **Dowód:** `_2019/diffyq/all_part1_scenes.py:1`.
  - **Kiedy:** Gdy film ma wiele rozdziałów lub kilka plików składających się na jedną kolejność montażową.

- **Dobieraj klasę bazową sceny do rodzaju ujęcia.**
  - **Źródła (1):** `_2022-puzzles`.
  - **Dowód:** `_2022/puzzles/subsets.py:209`.
  - **Kiedy:** Gdy dialog, zwykła animowana plansza i osadzony materiał wideo mają różne wymagania wykonawcze.

- **Przy wielodziedziczeniu inicjalizuj jawnie każdego rodzica dostarczającego niezależny stan.**
  - **Źródła (1):** `_2018-div_curl`.
  - **Dowód:** `_2018/div_curl.py:2909`.
  - **Kiedy:** Gdy scena składa zachowania kilku bazowych typów, których `setup()` nie tworzy jednego kooperacyjnego łańcucha.

# Warianty i ponowne użycie

- **Wydzielaj każdą powtarzalną konstrukcję do parametryzowanego helpera, komponentu, klasy bazowej lub modułu współdzielonego.**
  - **Źródła (21):** `_2016-eola`, `_2017-eoc`, `_2018-div_curl`, `_2019-diffyq`, `_2022-convolutions`, `_2022-puzzles`, `_2022-quintic`, `_2023-clt`, `_2023-clt_proof`, `_2023-convolutions2`, `_2023-gauss_int`, `_2023-optics_puzzles`, `_2024-antp`, `_2024-holograms`, `_2024-puzzles`, `_2024-transformers`, `_2025-colliding_blocks_v2`, `_2025-grover`, `_2025-laplace`, `_2026-cross_entropy`, `_2026-print_gallery`.
  - **Dowód:** `_2019/diffyq/part1/shared_constructs.py:19`.
  - **Kiedy:** Gdy ten sam motyw, układ lub algorytm budowy występuje w co najmniej dwóch scenach albo wariantach.

- **Buduj rodzinę podobnych scen przez dziedziczenie i nadpisywanie parametrów lub wąskich haków zamiast kopiowania `construct()`.**
  - **Źródła (18):** `_2016-eola`, `_2017-eoc`, `_2018-div_curl`, `_2019-diffyq`, `_2022-convolutions`, `_2022-puzzles`, `_2022-quintic`, `_2023-clt`, `_2023-convolutions2`, `_2023-gauss_int`, `_2023-optics_puzzles`, `_2024-antp`, `_2024-puzzles`, `_2024-transformers`, `_2025-colliding_blocks_v2`, `_2025-grover`, `_2026-cross_entropy`, `_2026-print_gallery`.
  - **Dowód:** `_2016/eola/chapter3.py:240`.
  - **Kiedy:** Gdy warianty zachowują przebieg, a różnią się danymi, tempem, stylem lub jednym etapem.

- **Projektuj złożony motyw jako komponent z nazwanymi częściami, metadanymi i metodami zmiany stanu.**
  - **Źródła (14):** `_2016-eola`, `_2017-eoc`, `_2022-convolutions`, `_2022-puzzles`, `_2023-clt_proof`, `_2023-convolutions2`, `_2023-optics_puzzles`, `_2024-antp`, `_2024-holograms`, `_2024-transformers`, `_2025-grover`, `_2025-laplace`, `_2026-cross_entropy`, `_2026-print_gallery`.
  - **Dowód:** `_2023/convolutions2/dice.py:33`.
  - **Kiedy:** Gdy geometria, etykiety i stan mają wspólny cykl życia, ale czasem wymagają osobnego sterowania.

- **Odwołuj się do części komponentu po znaczeniu, nie przez kruche indeksy podobiektów.**
  - **Źródła (10):** `_2016-eola`, `_2022-convolutions`, `_2022-puzzles`, `_2022-quintic`, `_2023-clt`, `_2023-convolutions2`, `_2023-optics_puzzles`, `_2024-antp`, `_2024-transformers`, `_2026-cross_entropy`.
  - **Dowód:** `_2022/puzzles/subsets.py:28`.
  - **Kiedy:** Gdy zawartość TeX-u, kolejność elementów lub liczba części może zmienić się między wariantami.

- **Modeluj wielokrotnie używany układ dynamiczny jako obiekt z własnym stanem oraz metodami jego ustawiania i odczytu.**
  - **Źródła (4):** `_2023-optics_puzzles`, `_2024-holograms`, `_2025-laplace`, `_2026-cross_entropy`.
  - **Dowód:** `_2025/laplace/shm.py:11`.
  - **Kiedy:** Gdy ten sam model fizyczny lub interaktywny występuje w wielu scenach z innymi parametrami.

- **Enkapsuluj powtarzalny efekt czasowy w parametryzowanej klasie `Animation`.**
  - **Źródła (1):** `_2024-puzzles`.
  - **Dowód:** `_2024/puzzles/max_rand.py:4`.
  - **Kiedy:** Gdy identyczna dynamika, a nie tylko identyczna geometria, pojawia się w kilku ujęciach.

- **Kopiuj już zainicjalizowany kosztowny obiekt i przenoś jego stan renderujący zamiast odtwarzać inicjalizację.**
  - **Źródła (1):** `_2024-holograms`.
  - **Dowód:** `_2024/holograms/diffraction.py:745`.
  - **Kiedy:** Gdy warianty współdzielą siatkę punktów, shadery lub uniformy, a różnią się tylko wybranymi parametrami.

# Stan, zależności i updatery

- **Animuj obiekt sterujący lub tracker, a trwałe zależności geometrii, tekstu i stylu utrzymuj updaterami.**
  - **Źródła (20):** wszystkie poza `_2016-eola`.
  - **Dowód:** `_2024/holograms/diffraction.py:420`.
  - **Kiedy:** Gdy kilka elementów musi stale reagować na jedną zmieniającą się wartość lub pozycję.

- **Trzymaj wspólny parametr liczbowy w jednym `ValueTrackerze` i wyprowadzaj z niego wszystkie zależne reprezentacje.**
  - **Źródła (15):** `_2019-diffyq`, `_2022-convolutions`, `_2022-puzzles`, `_2022-quintic`, `_2023-clt`, `_2023-clt_proof`, `_2023-convolutions2`, `_2023-gauss_int`, `_2023-optics_puzzles`, `_2024-puzzles`, `_2024-transformers`, `_2025-grover`, `_2025-laplace`, `_2026-cross_entropy`, `_2026-print_gallery`.
  - **Dowód:** `_2019/diffyq/part1/pendulum.py:1023`.
  - **Kiedy:** Gdy jedna wielkość steruje jednocześnie wykresem, etykietą, kolorem lub położeniem.

- **Jawnie zatrzymuj, czyść, odpinaj i ponownie podłączaj updatery przy zmianie roli lub reprezentacji obiektu.**
  - **Źródła (15):** `_2018-div_curl`, `_2019-diffyq`, `_2022-convolutions`, `_2022-puzzles`, `_2022-quintic`, `_2023-clt`, `_2023-convolutions2`, `_2023-gauss_int`, `_2023-optics_puzzles`, `_2024-holograms`, `_2024-puzzles`, `_2025-colliding_blocks_v2`, `_2025-grover`, `_2025-laplace`, `_2026-print_gallery`.
  - **Dowód:** `_2023/clt/main.py:1280`.
  - **Kiedy:** Gdy jawna animacja lub snapshot mógłby walczyć z aktywną zależnością o ten sam obiekt.

- **Zapisuj obiekty współdzielone przez fazy w nazwanych atrybutach sceny, a elementy jednorazowe pozostawiaj lokalne.**
  - **Źródła (8):** `_2016-eola`, `_2017-eoc`, `_2018-div_curl`, `_2019-diffyq`, `_2022-quintic`, `_2023-clt`, `_2023-convolutions2`, `_2024-transformers`.
  - **Dowód:** `_2016/eola/chapter8.py:129`.
  - **Kiedy:** Gdy późniejsza metoda musi zmodyfikować, wygasić lub przywrócić obiekt utworzony wcześniej.

- **Zapisuj stan albo przygotowuj target przed czasową reorganizacją i przywracaj go zamiast ręcznie odtwarzać układ.**
  - **Źródła (8):** `_2016-eola`, `_2017-eoc`, `_2022-convolutions`, `_2022-puzzles`, `_2023-gauss_int`, `_2024-antp`, `_2024-transformers`, `_2025-grover`.
  - **Dowód:** `_2017/eoc/chapter7.py:195`.
  - **Kiedy:** Gdy obiekt po epizodzie objaśniającym ma wrócić do wcześniejszej kompozycji.

- **Trzymaj stan autonomicznej symulacji wewnątrz jej komponentu i udostępniaj jawne zatrzymanie oraz wznowienie.**
  - **Źródła (4):** `_2019-diffyq`, `_2023-optics_puzzles`, `_2024-holograms`, `_2025-laplace`.
  - **Dowód:** `_2023/optics_puzzles/objects.py:178`.
  - **Kiedy:** Gdy scena przełącza się między ciągłym ruchem a zatrzymanym diagramem lub ręcznie reżyserowaną fazą.

- **Odłączaj updater od kopii, która ma stać się nieruchomym snapshotem.**
  - **Źródła (3):** `_2022-puzzles`, `_2023-convolutions2`, `_2023-gauss_int`.
  - **Dowód:** `_2022/puzzles/subsets.py:838`.
  - **Kiedy:** Gdy kopia dynamicznego obiektu ma zachować wcześniejszy stan lub uczestniczyć w niezależnej transformacji.

- **Przełączaj kierunek dwustronnej zależności jawnymi metodami, usuwając poprzednie wiązanie przed włączeniem nowego.**
  - **Źródła (2):** `_2019-diffyq`, `_2022-quintic`.
  - **Dowód:** `_2022/quintic/roots_and_coefs.py:457`.
  - **Kiedy:** Gdy raz obraz steruje modelem, a innym razem model ma sterować obrazem.

- **Rozdzielaj rzeczywiście niezależne wymiary stanu na osobne trackery.**
  - **Źródła (2):** `_2023-optics_puzzles`, `_2025-colliding_blocks_v2`.
  - **Dowód:** `_2025/colliding_blocks_v2/blocks.py:118`.
  - **Kiedy:** Gdy czas symulacji, stan fizyczny, prezentacja lub fazy wielu warstw muszą zmieniać się niezależnie.

- **Synchronizuj wewnętrzne zegary reprezentacji przed crossfadem lub zmianą widoku.**
  - **Źródła (1):** `_2023-optics_puzzles`.
  - **Dowód:** `_2023/optics_puzzles/driven_harmonic_oscillator.py:628`.
  - **Kiedy:** Gdy dwa obiekty pokazują ten sam proces i mają być zamienione bez skoku fazy.

- **Usuwaj z dynamicznego kontenera elementy, które trwale opuściły kadr.**
  - **Źródła (1):** `_2024-antp`.
  - **Dowód:** `_2024/antp/main.py:53`.
  - **Kiedy:** Gdy długie przewijanie lub generator adnotacji mógłby bez końca powiększać liczbę aktywnych mobjectów.

# Kompozycja, kamera i ciągłość wizualna

- **Buduj układ relacyjnie, a współrzędne bezwzględne rezerwuj dla świadomych kotwic danych, kamery lub całego kadru.**
  - **Źródła (21):** `_2016-eola`, `_2017-eoc`, `_2018-div_curl`, `_2019-diffyq`, `_2022-convolutions`, `_2022-puzzles`, `_2022-quintic`, `_2023-clt`, `_2023-clt_proof`, `_2023-convolutions2`, `_2023-gauss_int`, `_2023-optics_puzzles`, `_2024-antp`, `_2024-holograms`, `_2024-puzzles`, `_2024-transformers`, `_2025-colliding_blocks_v2`, `_2025-grover`, `_2025-laplace`, `_2026-cross_entropy`, `_2026-print_gallery`.
  - **Dowód:** `_2016/eola/chapter0.py:70`.
  - **Kiedy:** Gdy pozycja elementu wynika z sąsiedztwa, wyrównania lub rozmiaru innego elementu.

- **Grupuj geometrię, etykiety i adnotacje należące do jednego konceptu przed ich wspólną transformacją.**
  - **Źródła (14):** `_2016-eola`, `_2017-eoc`, `_2022-convolutions`, `_2022-puzzles`, `_2023-clt_proof`, `_2023-convolutions2`, `_2023-optics_puzzles`, `_2024-antp`, `_2024-holograms`, `_2024-transformers`, `_2025-grover`, `_2025-laplace`, `_2026-cross_entropy`, `_2026-print_gallery`.
  - **Dowód:** `_2016/eola/chapter9.py:331`.
  - **Kiedy:** Gdy kilka mobjectów powinno razem zmieniać położenie, skalę, styl, widoczność lub cykl życia.

- **Przypinaj narracyjne napisy i panele do kadru podczas ruchu kamery 3D.**
  - **Źródła (6):** `_2023-gauss_int`, `_2023-optics_puzzles`, `_2024-puzzles`, `_2025-colliding_blocks_v2`, `_2025-grover`, `_2025-laplace`.
  - **Dowód:** `_2023/gauss_int/integral.py:482`.
  - **Kiedy:** Gdy geometria należy do świata 3D, lecz tekst ma pozostać stabilny i czytelny.

- **Mapuj dane na położenia przez jeden układ współrzędnych zamiast powielać ręczne przeliczenia.**
  - **Źródła (5):** `_2018-div_curl`, `_2023-clt`, `_2023-clt_proof`, `_2024-antp`, `_2026-print_gallery`.
  - **Dowód:** `_2024/antp/main.py:389`.
  - **Kiedy:** Gdy punkty, etykiety, odcinki i wykresy muszą pozostać wzajemnie wyrównane po zmianie osi.

- **Generuj duże regularne układy algorytmicznie, a następnie ograniczaj rozmiar i pozycjonuj gotową grupę.**
  - **Źródła (3):** `_2022-puzzles`, `_2026-cross_entropy`, `_2026-print_gallery`.
  - **Dowód:** `_2026/cross_entropy/transformer_render.py:38`.
  - **Kiedy:** Gdy liczba wierszy, kolumn, warstw, paneli lub elementów zależy od danych.

- **Przenoś informację między reprezentacjami przez kopię widocznego obiektu lub jego semantycznej części.**
  - **Źródła (3):** `_2023-clt_proof`, `_2024-antp`, `_2025-grover`.
  - **Dowód:** `_2025/grover/clarification.py:328`.
  - **Kiedy:** Gdy widz powinien dostrzec ciągłość między symbolem, geometrią, etykietą i nowym układem.

- **Planuj ruch kamery jako jawną sekwencję perspektyw lub jako helper uruchamiany równolegle z treścią.**
  - **Źródła (2):** `_2024-antp`, `_2024-holograms`.
  - **Dowód:** `_2024/holograms/diffraction.py:451`.
  - **Kiedy:** Gdy kamera prowadzi widza przez długą planszę albo kilka widoków tej samej geometrii.

- **Dla adnotacji fotografii i pikselowo nakładanych warstw przechowuj jawne punkty, rozmiary i pozycje kalibracyjne.**
  - **Źródła (2):** `_2024-holograms`, `_2026-print_gallery`.
  - **Dowód:** `_2024/holograms/supplements.py:87`.
  - **Kiedy:** Gdy układ wynika z niezmiennej treści rastrowej, a przesunięcie o kilka pikseli niszczy dopasowanie.

- **Transformuj równania poprzez rozpoznawalne podwyrażenia zamiast zastępować cały zapis nowym obiektem.**
  - **Źródła (1):** `_2023-clt_proof`.
  - **Dowód:** `_2023/clt_proof/main.py:139`.
  - **Kiedy:** Gdy kolejne równania zachowują wspólne termy, których ciągłość ma być czytelna dla widza.

- **Pozostawiaj źródłowe podobiekty na scenie do zakończenia wszystkich transformacji, które ich używają.**
  - **Źródła (1):** `_2023-clt_proof`.
  - **Dowód:** `_2023/clt_proof/main.py:136`.
  - **Kiedy:** Gdy późniejsza animacja korzysta z fragmentu grupy utworzonej we wcześniejszym kroku.

# Dane, obliczenia i koszt renderowania

- **Oddzielaj model lub dane źródłowe od ich projekcji na mobjecty i zasilaj wszystkie reprezentacje tym samym źródłem.**
  - **Źródła (21):** `_2016-eola`, `_2017-eoc`, `_2018-div_curl`, `_2019-diffyq`, `_2022-convolutions`, `_2022-puzzles`, `_2022-quintic`, `_2023-clt`, `_2023-clt_proof`, `_2023-convolutions2`, `_2023-gauss_int`, `_2023-optics_puzzles`, `_2024-antp`, `_2024-holograms`, `_2024-puzzles`, `_2024-transformers`, `_2025-colliding_blocks_v2`, `_2025-grover`, `_2025-laplace`, `_2026-cross_entropy`, `_2026-print_gallery`.
  - **Dowód:** `_2024/antp/main.py:360`.
  - **Kiedy:** Gdy te same wartości są pokazywane jako geometria, liczby, etykiety, wykresy lub efekty.

- **Przeliczaj dane zależne od animowanego stanu w updaterze, `always_redraw` albo jawnej pętli klatkowej.**
  - **Źródła (12):** `_2016-eola`, `_2018-div_curl`, `_2019-diffyq`, `_2022-quintic`, `_2023-clt_proof`, `_2023-optics_puzzles`, `_2024-holograms`, `_2024-puzzles`, `_2024-transformers`, `_2025-grover`, `_2026-cross_entropy`, `_2026-print_gallery`.
  - **Dowód:** `_2022/quintic/polynomial_baisics.py:853`.
  - **Kiedy:** Gdy wynik rzeczywiście zmienia się podczas animacji i wcześniejsze obliczenie dałoby nieaktualną geometrię.

- **Obliczaj statyczne dane przed budową geometrii i dopiero potem mapuj je na obiekty wizualne.**
  - **Źródła (8):** `_2016-eola`, `_2017-eoc`, `_2022-convolutions`, `_2022-puzzles`, `_2023-clt_proof`, `_2023-convolutions2`, `_2023-gauss_int`, `_2024-antp`.
  - **Dowód:** `_2023/clt_proof/main.py:157`.
  - **Kiedy:** Gdy wartości nie zmieniają się w trakcie ujęcia albo mogą być przygotowane jako jedna tablica próbek.

- **Nie uzależniaj scen od absolutnych ścieżek autora; rozwiązuj zasoby i eksporty względem projektu lub konfiguracji.**
  - **Źródła (9):** `_2022-puzzles`, `_2023-convolutions2`, `_2023-gauss_int`, `_2023-optics_puzzles`, `_2024-transformers`, `_2025-grover`, `_2025-laplace`, `_2026-cross_entropy`, `_2026-print_gallery`.
  - **Dowód:** `_2022/puzzles/subsets.py:4480`.
  - **Kiedy:** Gdy render wymaga obrazów, modeli, danych, wideo albo zapisuje artefakty pomocnicze.

- **Przekazuj jedną funkcję modelu do wszystkich wykresów, pól i obliczeń pochodnych.**
  - **Źródła (4):** `_2018-div_curl`, `_2019-diffyq`, `_2022-quintic`, `_2023-optics_puzzles`.
  - **Dowód:** `_2018/div_curl.py:1144`.
  - **Kiedy:** Gdy kilka warstw obrazu ma przedstawiać dokładnie ten sam model matematyczny.

- **Cache’uj lub przygotowuj kosztowne dane przed wielokrotnym próbkowaniem.**
  - **Źródła (4):** `_2017-eoc`, `_2024-transformers`, `_2025-colliding_blocks_v2`, `_2026-cross_entropy`.
  - **Dowód:** `_2026/cross_entropy/next_char.py:244`.
  - **Kiedy:** Gdy callback wykresu, model ML albo kilka scen wielokrotnie żąda tych samych wyników.

- **Trzymaj obszerne dane wejściowe i przygotowane assety poza przebiegiem sceny, a w scenie tylko je wczytuj i materializuj.**
  - **Źródła (4):** `_2022-puzzles`, `_2025-colliding_blocks_v2`, `_2026-cross_entropy`, `_2026-print_gallery`.
  - **Dowód:** `_2025/colliding_blocks_v2/supplements.py:922`.
  - **Kiedy:** Gdy dane są długie, ręcznie opracowane, często wymieniane albo powstały w innym narzędziu.

- **Oddzielaj algorytm animacji od źródła danych przez wymienialne metody lub funkcje dostarczające osie, próbki i przykłady.**
  - **Źródła (3):** `_2023-convolutions2`, `_2024-transformers`, `_2026-cross_entropy`.
  - **Dowód:** `_2023/convolutions2/continuous.py:375`.
  - **Kiedy:** Gdy identyczna choreografia ma obsługiwać różne funkcje, rozkłady, obrazy lub teksty.

- **Ustalaj seed, gdy losowość wpływa na finalny kadr.**
  - **Źródła (3):** `_2023-clt`, `_2024-puzzles`, `_2025-laplace`.
  - **Dowód:** `_2024/puzzles/added_dimension.py:1320`.
  - **Kiedy:** Gdy rerender, poprawka montażowa lub test porównawczy powinny odtworzyć ten sam układ.

- **Wystawiaj jako parametry poziom jakości, gęstość próbkowania i horyzont obliczeń.**
  - **Źródła (2):** `_2018-div_curl`, `_2025-laplace`.
  - **Dowód:** `_2018/div_curl.py:399`.
  - **Kiedy:** Gdy potrzebny jest szybki render roboczy i droższy wariant produkcyjny.

- **Dopasowuj wielowartościowe wyniki numeryczne do poprzednich pozycji, zamiast ufać niestabilnej kolejności indeksów.**
  - **Źródła (1):** `_2022-quintic`.
  - **Dowód:** `_2022/quintic/roots_and_coefs.py:62`.
  - **Kiedy:** Gdy kolejność pierwiastków lub innych wyników może zmienić się mimo ciągłej zmiany parametrów.

- **Przekazuj wynik poprzedniej iteracji jako dane wejściowe następnej.**
  - **Źródła (1):** `_2023-convolutions2`.
  - **Dowód:** `_2023/convolutions2/continuous.py:1896`.
  - **Kiedy:** Gdy scena pokazuje kolejne zastosowania tej samej operacji numerycznej.

- **Przenoś obliczenia per-piksel do shadera, pozostawiając CPU dla pomocniczej geometrii.**
  - **Źródła (1):** `_2024-holograms`.
  - **Dowód:** `_2024/holograms/diffraction.wgsl:52`.
  - **Kiedy:** Gdy pełny obraz jest zbyt kosztowny do obliczania na CPU, ale wykresy i pola nadal potrzebują odpowiednika modelu.

- **Zwiększaj liczbę aktywnych danych stopniowo zamiast od razu renderować pełny ogromny zbiór.**
  - **Źródła (1):** `_2024-holograms`.
  - **Dowód:** `_2024/holograms/diffraction.py:3496`.
  - **Kiedy:** Gdy pełny dataset pogarsza wydajność lub utrudnia pedagogiczne pokazanie narastania efektu.

- **Otwieraj zewnętrzne źródło wideo w `setup()`, zamykaj je w `tear_down()`, a ekstrakcję klatek wydzielaj do metody.**
  - **Źródła (1):** `_2024-holograms`.
  - **Dowód:** `_2024/holograms/model.py:16`.
  - **Kiedy:** Gdy scena korzysta z zasobu wymagającego jawnego cyklu życia poza pojedynczym wywołaniem `construct()`.

- **Przycinaj przemapowaną geometrię do docelowego obszaru przed animacją.**
  - **Źródła (1):** `_2026-print_gallery`.
  - **Dowód:** `_2026/print_gallery/exponential.py:3191`.
  - **Kiedy:** Gdy transformacja siatki, tekstury lub kafelków może wyprowadzić elementy poza użyteczny zakres.

- **Nie uruchamiaj kosztownego eksperymentu ani interaktywnego wykresu podczas importu modułu scen.**
  - **Źródła (1):** `_2024-transformers`.
  - **Dowód:** `_2024/transformers/almost_orthogonal.py:22`.
  - **Kiedy:** Gdy moduł jest importowany tylko po to, aby renderer odnalazł klasy scen.

# Tempo, symulacja i synchronizacja

- **Parametryzuj tempo powtarzalnej sekwencji w metodzie, helperze albo atrybucie wariantu zamiast rozrzucać magiczne czasy.**
  - **Źródła (20):** wszystkie poza `_2016-eola`.
  - **Dowód:** `_2017/eoc/chapter2.py:12`.
  - **Kiedy:** Gdy jeden przebieg ma wersje wolną, szybką lub zależną od konfiguracji.

- **Wyprowadzaj czas animacji z długości ścieżki, liczby elementów albo rozmiaru przewijanej treści.**
  - **Źródła (6):** `_2022-puzzles`, `_2022-quintic`, `_2023-clt`, `_2023-gauss_int`, `_2023-optics_puzzles`, `_2024-antp`.
  - **Dowód:** `_2023/clt/galton_board.py:378`.
  - **Kiedy:** Gdy warianty różnią się skalą danych, ale powinny zachować porównywalną prędkość percepcyjną.

- **Wiąż `run_time` z czasem modelu i steruj pauzą lub spowolnieniem przez osobny parametr czasu.**
  - **Źródła (5):** `_2019-diffyq`, `_2023-optics_puzzles`, `_2024-holograms`, `_2025-colliding_blocks_v2`, `_2025-laplace`.
  - **Dowód:** `_2025/colliding_blocks_v2/blocks.py:165`.
  - **Kiedy:** Gdy ekran ma odtwarzać symulację w czasie rzeczywistym albo przechodzić do slow motion.

- **Określaj lokalne `time_span` poszczególnych animacji wewnątrz jednego czasu całego ujęcia.**
  - **Źródła (2):** `_2024-holograms`, `_2026-print_gallery`.
  - **Dowód:** `_2026/print_gallery/exponential.py:177`.
  - **Kiedy:** Gdy elementy jednej kompozycji mają wejść i wyjść w różnych chwilach, ale pozostają częścią wspólnego beatu.

- **Po pokazaniu kilku wolnych przykładów przechodź do masowej fazy z uproszczonym odświeżaniem stanu.**
  - **Źródła (2):** `_2023-clt`, `_2023-gauss_int`.
  - **Dowód:** `_2023/clt/main.py:3266`.
  - **Kiedy:** Gdy widz zna już mechanizm, a scena ma pokazać jego statystyczny lub zbiorczy efekt.

- **Wyznaczaj czas zdarzenia z modelu analitycznego i używaj go do wspólnej synchronizacji obrazu oraz dźwięku.**
  - **Źródła (1):** `_2025-colliding_blocks_v2`.
  - **Dowód:** `_2025/colliding_blocks_v2/blocks.py:69`.
  - **Kiedy:** Gdy zderzenie lub inny impuls może wypaść między klatkami renderu.

- **Oznaczaj pauzy odpowiadające konkretnym punktom komentarza narracyjnego nazwanym argumentem.**
  - **Źródła (1):** `_2022-puzzles`.
  - **Dowód:** `_2022/puzzles/subsets.py:893`.
  - **Kiedy:** Gdy pauza jest punktem montażowym związanym z konkretną kwestią, a nie tylko technicznym `wait()`.

# Sprzeczności

1. **Granularność sceny**

   - **Osobna klasa na niezależny beat:** 12 źródeł; dowód: `_2016/eola/chapter0.py:64`.
   - **Jeden ciągły, stanowy rozdział w jednej klasie, dzielony komentarzami:** `_2026-print_gallery`; dowód: `_2026/print_gallery/exponential.py:429`.
   - `_2022-puzzles` pokazuje warunkową granicę: wspólny stan przemawia za fazami jednej sceny, a niezależne cięcie za osobną klasą (`_2022/puzzles/subsets.py:872`).

2. **Źródło prawdy dla zmiennego stanu**

   - **Jeden `ValueTracker`:** 15 źródeł; dowód: `_2019/diffyq/part1/pendulum.py:1023`.
   - **Stan odczytywany bezpośrednio z położeń obiektów, bez drugiej kopii:** `_2022-quintic`; dowód: `_2022/quintic/roots_and_coefs.py:445`.
   - **Oddzielne trackery dla czasu, fizyki i prezentacji:** `_2025-colliding_blocks_v2`; dowód: `_2025/colliding_blocks_v2/blocks.py:118`.

3. **Mechanizm ciągłej zależności**

   - **Jawna pętla klatkowa przeliczająca całą geometrię:** `_2016-eola`; dowód: `_2016/eola/chapter10.py:1081`.
   - **`ValueTracker` z updaterem lub `always_redraw`:** 15 źródeł; dowód: `_2019/diffyq/part1/pendulum.py:1023`.
   - Korpus nie pozwala ustalić, czy różnica jest wyborem projektowym, czy skutkiem zmiany API Manima między epokami.

4. **Miejsce obliczeń**

   - **Oblicz statyczne dane przed utworzeniem geometrii:** 8 źródeł; dowód: `_2023/clt_proof/main.py:157`.
   - **Obliczaj dane zależne od stanu wewnątrz updatera:** 12 źródeł; dowód: `_2022/quintic/polynomial_baisics.py:853`.
   - **Usuń drogie obliczenia z wielokrotnie próbkowanego callbacku i użyj cache:** `_2017-eoc`; dowód: `_2017/eoc/chapter8.py:1396`.

5. **Gotowy asset kontra generowanie proceduralne**

   - **Wczytaj przygotowaną, złożoną planszę jako asset:** `_2022-puzzles`; dowód: `_2022/puzzles/subsets.py:2232`.
   - **Generuj wykresy, powierzchnie i ścieżki z funkcji podczas renderu:** `_2025-laplace`; dowód: `_2025/laplace/integration.py:35`.

6. **Własność parametrów tempa**

   - **Ustalaj czas lokalnie przy konkretnym beacie zamiast przez jedną globalną stałą:** `_2016-eola`; dowód: `_2016/eola/chapter1.py:78`.
   - **Centralizuj czas powtarzalnego przebiegu w helperze lub atrybucie klasy:** 20 źródeł; dowód: `_2017/eoc/chapter2.py:12`.

7. **Układ relacyjny kontra kalibracja absolutna**

   - **Pozycjonuj elementy względem kotwic i sąsiadów:** 21 źródeł; dowód: `_2016/eola/chapter0.py:70`.
   - **Zachowuj jawne rozmiary i pozycje pikselowo nakładanych warstw:** `_2026-print_gallery`; dowód: `_2026/print_gallery/exponential.py:155`.
   - **Zapisuj jawne punkty kotwiczące adnotacje na fotografii:** `_2024-holograms`; dowód: `_2024/holograms/supplements.py:87`.

8. **Stan przy obiekcie kontra równoległe kolekcje**

   - **Zapisuj metadane na obiektach zamiast w równoległych mapach indeksów:** `_2022-convolutions`; dowód: `_2022/convolutions/discrete.py:386`.
   - **Trzymaj niezależne trackery w kolekcji indeksowanej tak samo jak grupa obiektów:** `_2023-optics_puzzles`; dowód: `_2023/optics_puzzles/slowing_waves.py:39`.

# Odsiane jako banał

**39 surowych obserwacji.**

Przykłady:

- „Nie zostawiaj pustej sceny z `pass`” — `_2023/clt_proof/main.py:102`.
- „Usuń kod po bezwarunkowym `return`” — `_2026/cross_entropy/robot.py:7669`.
- „Usuń nieużywane obiekty lub parametry” — `_2023/clt_proof/main.py:531`, `_2022/convolutions/discrete.py:1573`.
- „Nie używaj mutowalnej listy jako argumentu domyślnego” — `_2024/transformers/generation.py:244`.
- „Utrzymuj zależności modułów acykliczne” — `_2025/grover/qc_supplements.py:2`.
- „Usuń stare kopie, TODO i zakomentowane alternatywy” — `_2017/eoc/old_chapter1.py:4`, `_2023/clt/dice_sims.py:88`.
- „Nie wywołuj drugi raz identycznej operacji układu” — `_2023/clt_proof/main.py:1296`.
- „Nie używaj mechanizmu oznaczonego jako przestarzały” — `_2018/div_curl.py:20`.

# Czego brakuje

- **Intencji narracyjnej:** kod nie wyjaśnia, dlaczego dana reprezentacja, kolejność ani granica sceny była pedagogicznie właściwa.
- **Powiązania z lektorem:** nie wiadomo, do jakich słów odnoszą się `wait()`, `run_time`, pauzy i cięcia ani czy finalny montaż zachował te czasy.
- **Oceny finalnego ruchu:** ze statycznego kodu nie da się wiarygodnie ocenić czytelności, migotania, zasłaniania elementów, płynności transformacji ani dezorientujących ruchów kamery.
- **Odrzuconych alternatyw i przyczyn decyzji:** nie wiadomo, które rozwiązania wypróbowano, dlaczego je porzucono i czy zachowany kod jest wzorcem, kompromisem czy jednorazowym obejściem.
- **Wyników i skuteczności:** samo wystąpienie wzorca nie dowodzi, że był dobry; brakuje porównań renderów, opinii widzów, retencji i wyników testów dydaktycznych.
- **Docelowej widowni:** brak informacji o prerekwizytach, oczekiwanym tempie rozumowania i dopuszczalnym obciążeniu poznawczym.
- **Pomiarów wydajności:** są pokrętła jakości, cache i shadery, ale nie ma czasów renderu, zużycia pamięci, profili ani progów uzasadniających wybór.
- **Środowiska odtwarzania:** brakuje wersji Manima, Pythona, fontów, TeX-u, shaderów, modeli i sterowników potrzebnych do wiernego rerenderu.
- **Regresji wizualnej i poprawności matematycznej:** kod nie pokazuje, jak sprawdzano zgodność kolejnych renderów, błędy numeryczne ani zgodność wzorów z narracją.
- **Znaczenia elementów roboczych:** nie wiadomo, czy `TODO`, puste sceny i stare metody są śmieciem, świadomymi punktami montażowymi czy prywatnym systemem notatek autora.
- **Dostępności:** zbiór milczy o napisach, kontraście, daltonizmie, wielkości tekstu, bezpiecznych obszarach kadru, lokalizacji i wersjach bez dźwięku.
- **Dźwięku i montażu końcowego:** poza pojedynczą synchronizacją zdarzeń nie widać muzyki, miksu, efektów, kolejności wybranych take’ów ani przejść między plikami.
- **Pochodzenia zasobów:** brak licencji, autorstwa, procedury aktualizacji oraz informacji, czy asset może być legalnie i technicznie przeniesiony do biblioteki idiomów.
- **Zakresu obowiązywania historycznego:** materiał obejmuje lata 2016–2026, lecz nie oznacza, które idiomy są nadal zalecane, a które wynikają z dawnego API.
- **Przenośności poza stylem 3Blue1Brown:** wszystkie źródła pochodzą z jednego repozytorium i jednej tradycji produkcyjnej, więc korpus nie ujawnia, które reguły są uniwersalne, a które charakterystyczne dla tego autora i pipeline’u.
## Granice scen i ponowne użycie

- **Wydzielaj niezależny beat narracyjno-wizualny do osobnej klasy sceny.** Źródła: **13** — 2016/eola, 2022/convolutions, 2022/puzzles, 2023/clt_proof, 2023/gauss_int, 2024/antp, 2024/holograms, 2024/puzzles, 2025/colliding_blocks_v2, 2025/grover, 2025/laplace, 2026/cross_entropy, 2026/print_gallery. Dowód: `_2016/eola/chapter0.py:64`. Obowiązuje, gdy ujęcie ma własny stan początkowy i końcowy albo powinno dać się renderować i montować osobno.

- **Rozbijaj długą scenę stanową na nazwane metody fazowe, a `construct` zostaw jako orkiestrator kolejności.** Źródła: **6** — 2016/eola, 2017/eoc, 2018/div_curl, 2019/diffyq, 2022/puzzles, 2026/print_gallery. Dowód: `_2016/eola/chapter8.py:113`. Obowiązuje, gdy kolejne etapy współdzielą obiekty i nie są sensownymi punktami cięcia filmu.

- **Buduj warianty scen przez klasę bazową oraz parametry lub małe nadpisania, zamiast kopiować `construct`.** Źródła: **19** — 2016/eola, 2017/eoc, 2018/div_curl, 2019/diffyq, 2022/convolutions, 2022/puzzles, 2022/quintic, 2023/clt, 2023/convolutions2, 2023/gauss_int, 2023/optics_puzzles, 2024/antp, 2024/holograms, 2024/puzzles, 2024/transformers, 2025/colliding_blocks_v2, 2025/grover, 2026/cross_entropy, 2026/print_gallery. Dowód: `_2016/eola/chapter3.py:240`. Obowiązuje, gdy różnią się dane, tempo, styl albo pojedyncza faza, lecz dramaturgia i hierarchia obiektów zostają te same.

- **Wydzielaj współdzielone komponenty scen do modułu, helpera albo klasy bazowej i importuj je zamiast odtwarzać lokalnie.** Źródła: **14** — 2016/eola, 2017/eoc, 2019/diffyq, 2022/quintic, 2023/clt, 2023/convolutions2, 2023/gauss_int, 2023/optics_puzzles, 2024/antp, 2024/transformers, 2024/holograms, 2025/laplace, 2026/cross_entropy, 2026/print_gallery. Dowód: `_2017/eoc/chapter1.py:2`. Obowiązuje, gdy geometria, model danych lub ruch występuje w więcej niż jednym module scen.

- **Zamykaj powtarzalne motywy wizualne w parametryzowanych fabrykach, zachowując ich nazwane części.** Źródła: **17** — 2018/div_curl, 2019/diffyq, 2022/convolutions, 2022/puzzles, 2022/quintic, 2023/clt, 2023/convolutions2, 2023/gauss_int, 2024/antp, 2024/holograms, 2024/puzzles, 2024/transformers, 2025/colliding_blocks_v2, 2025/grover, 2025/laplace, 2026/cross_entropy, 2026/print_gallery. Dowód: `_2018/div_curl.py:120`. Obowiązuje, gdy ten sam diagram, etykieta, kafelek lub układ powstaje wielokrotnie z innymi danymi albo stylem.

## Stan, zależności i cykl życia animacji

- **Przechowuj obiekty używane przez wiele faz jako nazwane atrybuty sceny, a jednorazowe pozostawiaj lokalnie.** Źródła: **10** — 2016/eola, 2017/eoc, 2018/div_curl, 2019/diffyq, 2022/quintic, 2023/clt, 2023/convolutions2, 2024/transformers, 2024/puzzles, 2026/print_gallery. Dowód: `_2017/eoc/chapter1.py:80`. Obowiązuje, gdy późniejsza faza ma przekształcić, przywrócić albo wygasić wcześniej utworzony obiekt.

- **Trzymaj jeden wspólny parametr ciągłej zmiany w trackerze i wyprowadzaj z niego wszystkie obiekty pochodne.** Źródła: **16** — 2019/diffyq, 2022/convolutions, 2022/puzzles, 2022/quintic, 2023/clt, 2023/clt_proof, 2023/convolutions2, 2023/gauss_int, 2023/optics_puzzles, 2024/transformers, 2024/puzzles, 2025/colliding_blocks_v2, 2025/grover, 2025/laplace, 2026/cross_entropy, 2026/print_gallery. Dowód: `_2022/puzzles/subsets.py:643`. Obowiązuje, gdy jedna liczba steruje jednocześnie geometrią, liczbami, etykietami, kolorem lub śladem.

- **Używaj updaterów albo `always_redraw` wyłącznie do trwałych zależności, a kroki narracyjne wykonuj jawnymi animacjami.** Źródła: **20** — 2017/eoc, 2018/div_curl, 2019/diffyq, 2022/convolutions, 2022/puzzles, 2022/quintic, 2023/clt, 2023/clt_proof, 2023/convolutions2, 2023/gauss_int, 2023/optics_puzzles, 2024/antp, 2024/holograms, 2024/puzzles, 2024/transformers, 2025/colliding_blocks_v2, 2025/grover, 2025/laplace, 2026/cross_entropy, 2026/print_gallery. Dowód: `_2022/convolutions/discrete.py:1233`. Obowiązuje, gdy zależność ma przetrwać ruch kamery lub wiele animacji, a nie tylko jedną transformację.

- **Jawnie zawieszaj, wznawiaj lub usuwaj updatery przed ręczną zmianą reprezentacji obiektu.** Źródła: **12** — 2018/div_curl, 2022/puzzles, 2022/quintic, 2023/clt, 2023/convolutions2, 2023/gauss_int, 2024/holograms, 2024/puzzles, 2025/colliding_blocks_v2, 2025/grover, 2025/laplace, 2026/print_gallery. Dowód: `_2024/holograms/diffraction.py:1005`. Obowiązuje, gdy updater i jawna animacja mogłyby jednocześnie modyfikować ten sam mobject.

- **Zapisuj stan lub przygotowuj target przed odwracalną reorganizacją układu.** Źródła: **6** — 2016/eola, 2017/eoc, 2022/convolutions, 2023/gauss_int, 2024/transformers, 2025/grover. Dowód: `_2017/eoc/chapter7.py:195`. Obowiązuje, gdy obiekt po epizodzie wyjaśniającym ma wrócić do poprzedniego położenia, skali albo stylu.

- **Odłączaj updater od kopii, która ma zostać nieruchomym śladem lub źródłem niezależnej transformacji.** Źródła: **3** — 2022/puzzles, 2023/convolutions2, 2023/gauss_int. Dowód: `_2023/gauss_int/integral.py:736`. Obowiązuje, gdy kopiowany obiekt dynamiczny ma przestać reagować na bieżący parametr.

- **Modeluj autonomiczną symulację jako obiekt posiadający własny czas i jawne metody zatrzymania oraz wznowienia.** Źródła: **4** — 2019/diffyq, 2023/optics_puzzles, 2024/holograms, 2025/laplace. Dowód: `_2025/laplace/shm.py:46`. Obowiązuje, gdy scena przełącza się między biegiem fizycznej symulacji a reżyserowanym zatrzymaniem.

## Kompozycja i przestrzeń kadru

- **Układaj elementy względem kotwic i sąsiadów, a ręczne współrzędne rezerwuj dla globalnej kompozycji lub danych geometrycznych.** Źródła: **21** — wszystkie badane źródła. Dowód: `_2016/eola/chapter0.py:70`. Obowiązuje dla etykiet, paneli, wzorów i grup o zmiennej zawartości lub rozmiarze.

- **Grupuj element główny z jego etykietami, ramką i prowadnicami jako jedną semantyczną jednostkę ruchu.** Źródła: **16** — 2016/eola, 2017/eoc, 2018/div_curl, 2022/convolutions, 2022/puzzles, 2022/quintic, 2023/clt_proof, 2023/convolutions2, 2023/optics_puzzles, 2024/antp, 2024/holograms, 2024/transformers, 2025/grover, 2025/laplace, 2026/cross_entropy, 2026/print_gallery. Dowód: `_2017/eoc/chapter2.py:995`. Obowiązuje, gdy elementy mają wspólnie przesuwać się, skalować, kopiować albo znikać.

- **Nadaj częściom złożonego mobjectu nazwy lub metadane domenowe zamiast sterować nimi przez kruche indeksy submobjectów.** Źródła: **6** — 2022/convolutions, 2022/puzzles, 2022/quintic, 2023/convolutions2, 2024/transformers, 2026/cross_entropy. Dowód: `_2022/convolutions/discrete.py:386`. Obowiązuje, gdy diagram lub napis będzie przebudowywany, filtrowany albo animowany po znaczeniu.

- **Mapuj pozycje pochodzące z danych przez jeden układ współrzędnych, nie przez stałe kadru.** Źródła: **5** — 2023/clt, 2023/clt_proof, 2023/gauss_int, 2024/antp, 2026/print_gallery. Dowód: `_2024/antp/main.py:389`. Obowiązuje dla punktów, wykresów, siatek i adnotacji, które muszą pozostać wyrównane po zmianie osi lub geometrii.

- **Przypinaj tekst narracyjny i HUD do ekranu, gdy kamera porusza się w świecie 3D.** Źródła: **6** — 2023/gauss_int, 2023/optics_puzzles, 2024/puzzles, 2025/colliding_blocks_v2, 2025/grover, 2025/laplace. Dowód: `_2023/gauss_int/integral.py:482`. Obowiązuje, gdy tekst ma pozostać czytelny mimo obrotu, zoomu lub przesunięcia kamery.

- **Generuj duże regularne diagramy procedurą opartą na centralnych stałych układu.** Źródła: **2** — 2026/cross_entropy, 2026/print_gallery. Dowód: `_2026/cross_entropy/transformer_render.py:38`. Obowiązuje dla diagramów z wieloma warstwami, wierszami, kolumnami albo kafelkami.

## Dane, obliczenia i koszt renderu

- **Utrzymuj jedno źródło modelu danych i przekształcaj jego wynik w geometrię oraz etykiety dopiero przy budowie sceny.** Źródła: **17** — 2016/eola, 2017/eoc, 2018/div_curl, 2019/diffyq, 2022/convolutions, 2022/puzzles, 2022/quintic, 2023/clt, 2023/clt_proof, 2023/convolutions2, 2023/gauss_int, 2023/optics_puzzles, 2024/antp, 2024/transformers, 2025/laplace, 2026/cross_entropy, 2026/print_gallery. Dowód: `_2018/div_curl.py:1144`. Obowiązuje, gdy ta sama funkcja, tablica lub model zasila kilka warstw wizualizacji.

- **Obliczaj statyczne dane przed budową geometrii, a dane zależne od animowanego stanu przeliczaj w updaterze.** Źródła: **12** — 2016/eola, 2019/diffyq, 2022/convolutions, 2022/puzzles, 2022/quintic, 2023/clt_proof, 2023/convolutions2, 2023/gauss_int, 2024/antp, 2024/puzzles, 2025/laplace, 2026/cross_entropy. Dowód: `_2022/convolutions/discrete.py:1101`. Obowiązuje, gdy trzeba odróżnić koszt jednorazowego przygotowania od kosztu ponoszonego w każdej klatce.

- **Oddzielaj ciężkie dane, modele i ręcznie przygotowane layouty od kodu choreografii sceny.** Źródła: **6** — 2022/puzzles, 2024/holograms, 2025/colliding_blocks_v2, 2025/laplace, 2026/cross_entropy, 2026/print_gallery. Dowód: `_2026/cross_entropy/language_models.py:16`. Obowiązuje, gdy dane są duże, kosztowne, ręcznie opracowane albo zmieniają się niezależnie od animacji.

- **Cache’uj wyniki kosztownych modeli i numerycznych próbkowań poza pętlą renderu.** Źródła: **3** — 2017/eoc, 2024/transformers, 2026/cross_entropy. Dowód: `_2026/cross_entropy/next_char.py:244`. Obowiązuje, gdy renderer wielokrotnie pyta o te same dane albo kilka scen używa tego samego modelu.

- **Wystawiaj gęstość próbkowania, rozdzielczość i poziom jakości jako parametry sceny.** Źródła: **3** — 2018/div_curl, 2024/holograms, 2025/laplace. Dowód: `_2018/div_curl.py:399`. Obowiązuje, gdy potrzebne są zarówno szybkie rendery robocze, jak i kosztowne rendery produkcyjne.

- **Ustalaj seed albo przekazuj generator losowy jawnie, gdy losowość wpływa na finalny obraz.** Źródła: **3** — 2023/clt, 2024/puzzles, 2025/laplace. Dowód: `_2024/puzzles/added_dimension.py:1320`. Obowiązuje, gdy rerender ma odtworzyć tę samą kompozycję lub przebieg.

## Czas, rytm i kamera

- **Parametryzuj tempo powtarzalnej choreografii lokalną stałą, argumentem helpera albo atrybutem wariantu.** Źródła: **21** — wszystkie badane źródła. Dowód: `_2017/eoc/chapter2.py:12`. Obowiązuje, gdy kilka kroków należy przyspieszać lub zwalniać razem bez kopiowania przebiegu.

- **Wyprowadzaj czas sekwencji z liczby elementów, długości ścieżki albo czasu symulacji.** Źródła: **8** — 2022/puzzles, 2022/quintic, 2023/clt, 2023/gauss_int, 2023/optics_puzzles, 2024/antp, 2025/colliding_blocks_v2, 2025/laplace. Dowód: `_2023/clt/galton_board.py:378`. Obowiązuje, gdy warianty różnią się liczbą elementów, gęstością danych lub odległością ruchu.

- **Rozdzielaj czas całego ujęcia od przedziałów czasowych równoległych animacji.** Źródła: **2** — 2024/holograms, 2026/print_gallery. Dowód: `_2026/print_gallery/exponential.py:177`. Obowiązuje, gdy elementy mają wejść lub wyjść w różnych momentach jednego przebiegu.

- **Zapisuj ruch kamery jako jawne etapy lub wydziel go do helpera.** Źródła: **2** — 2024/antp, 2024/holograms. Dowód: `_2024/holograms/diffraction.py:451`. Obowiązuje, gdy kamera jest częścią objaśnienia, a nie tylko technicznym kadrowaniem.

## Sprzeczności

- **Granica sceny:** 13 źródeł zaleca osobną klasę dla niezależnego ujęcia, np. `_2025/grover/qc_supplements.py:152`; 2026/print_gallery zaleca utrzymać długi, stanowy rozdział w jednej klasie, `_2026/print_gallery/exponential.py:429`. Korpus nie podaje mierzalnego progu, kiedy współdzielony stan przestaje uzasadniać jedną klasę.

- **Źródło prawdy o stanie:** 16 źródeł preferuje `ValueTracker`, np. `_2023/gauss_int/integral.py:371`; 2022/quintic zaleca przechowywać stan modelu w pozycjach obiektów, `_2022/quintic/roots_and_coefs.py:445`. To dwa odmienne modele własności stanu.

- **Mechanizm ciągłej zmiany:** większość źródeł zaleca updatery lub `always_redraw`, np. `_2026/cross_entropy/robot.py:8021`; 2016/eola zaleca jawną pętlę po klatkach, `_2016/eola/chapter10.py:1081`. To może wynikać z różnic wersji Manima, ale korpus nie ustala tej granicy.

- **Układ relacyjny kontra pikselowa kalibracja:** wszystkie źródła preferują układ relacyjny dla zwykłych elementów, np. `_2017/eoc/chapter10.py:80`; 2026/print_gallery wymaga jawnych pozycji i rozmiarów warstw rastrowych, `_2026/print_gallery/exponential.py:155`. Materiał nie daje reguły wykrywania, że kompozycja weszła już w tryb pikselowego nakładania.

- **Generowanie kontra gotowy asset:** źródła matematyczne zalecają wyprowadzać obraz z modelu, np. `_2019/diffyq/part2/fourier_series.py:240`; 2022/puzzles zaleca załadować gotową złożoną planszę, `_2022/puzzles/subsets.py:2232`. Korpus nie rozstrzyga kosztu utrzymania ani jakości obu podejść.

## Odsiane jako banał

**44 z 324 obserwacji** odrzucono jako opis oczywistej funkcji API, ogólną higienę Pythona lub problem jakości kodu, a nie decyzję projektową specyficzną dla konstrukcji scen.

Przykłady:

- „`VGroup` grupuje elementy” bez wskazania wspólnego cyklu życia lub semantycznych części.
- Przekazywanie identycznego słownika `run_time` do kilku animacji.
- Usuwanie kodu po bezwarunkowym `return`.
- Niepozostawianie `pass`, TODO i pustych scen w katalogu produkcyjnym.
- Niestosowanie mutowalnej listy jako wartości domyślnej argumentu.
- Niezaszywanie absolutnej ścieżki autora w kodzie.

Ostatnie trzy są ważnymi zasadami jakości repozytorium, ale nie powinny trafić do biblioteki idiomów Manima.

## Czego brakuje

- Kryteriów narracyjnych: kod nie mówi, czy widz rozumie kolejność ujawniania informacji, czy pauza jest wystarczająca ani gdzie potrzebne jest powtórzenie.
- Oceny wizualnej: nie da się wyczytać z kodu czy tekst jest czytelny, kontrast wystarczający, kadr przeładowany albo ruch kamery dezorientuje.
- Dostępności: brak zasad dla palet bezpiecznych dla osób z zaburzeniami rozpoznawania barw, napisów, tempa odbioru i alternatyw tekstowych.
- Empirycznych danych o wydajności: obserwacje wskazują potencjalnie drogie miejsca, lecz nie zawierają profili renderu, limitów czasu ani budżetów pamięci.
- Kontraktu wersji i API: materiał obejmuje lata 2016–2026, ale nie oznacza wersji Manima, kompatybilności idiomów ani zamienników dla API przestarzałych.
- Procesu walidacji: brak renderów referencyjnych, testów wizualnej regresji, zasad QA oraz procedury sprawdzania assetów.
- Praw i pochodzenia zasobów: kod ujawnia użycie obrazów, SVG, tekstur i wideo, lecz nie mówi nic o licencjach, źródłach i reprodukowalności danych zewnętrznych.
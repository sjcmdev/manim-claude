## Updatery i stan

- **Wyprowadzaj mobject zależny z bieżącej wartości lub geometrii źródła, a nie z `dt`.**  
  Źródła: 24 — _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, mf_tools, uwezi.  
  Dowód: `_2016/eola/chapter2.py:332`.  
  Obowiązuje, gdy aktualny stan źródła jednoznacznie wyznacza wynik.

- **Przyjmuj `dt` wyłącznie wtedy, gdy updater całkuje czas, prędkość lub historię stanu.**  
  Źródła: 16 — _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, uwezi.  
  Dowód: `_2018/div_curl/div_curl.py:368`.  
  Obowiązuje dla fizyki, zegarów i śladów; nie dla projekcji wartości trackera.

- **Odbudowuj geometrię pochodną z aktualnych danych przez `become`, `always_redraw` lub fabrykę, zamiast kumulować przesunięcia.**  
  Źródła: 18 — _2018-div_curl, _2019-diffyq, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, mf_tools, uwezi.  
  Dowód: `_2018/div_curl/div_curl.py:1302`.  
  Obowiązuje, gdy zmienia się kształt, liczba punktów albo układ części.

- **Przechowuj stan wymagany między klatkami jawnie na właścicielu albo w wydzielonym modelu i aktualizuj go przed geometrią.**  
  Źródła: 15 — _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-quintic, _2023-optics_puzzles, _2024-holograms, _2024-transformers, _2025-colliding_blocks_v2, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, mf_tools, uwezi.  
  Dowód: `_2016/eola/chapter2.py:245`.  
  Obowiązuje dla zależności historycznych, a nie dla czystej geometrii od trackera.

- **Rozdziel updater źródła, updater geometrii i updater interakcji oraz pilnuj kolejności ich zależności.**  
  Źródła: 10 — _2018-div_curl, _2022-convolutions, _2022-quintic, _2023-clt, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-transformers, _2025-colliding_blocks_v2, uwezi.  
  Dowód: `_2023/optics_puzzles/adding_waves.py:808`.  
  Obowiązuje, gdy jeden ruch zasila więcej niż jeden poziom wizualizacji.

- **Zapisuj referencję do updatera i jawnie go czyść, zawieszaj lub wznawiaj przy transformacji, zmianie trybu albo robieniu statycznej kopii.**  
  Źródła: 16 — _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-quintic, _2023-clt, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery.  
  Dowód: `_2018/div_curl/div_curl.py:1819`.  
  Obowiązuje, chyba że updater ma celowo współbiec z animacją.

- **Wymuś pierwsze przeliczenie zaraz po podpięciu updatera.**  
  Źródła: 4 — _2022-convolutions, _2023-clt, mf_tools, uwezi.  
  Dowód: `20230605_zoomed.py:33` (uwezi).  
  Obowiązuje, gdy obiekt ma być poprawny jeszcze przed pierwszą klatką.

## Kompozycja i własne klasy `Animation`

- **Składaj zwykłą choreografię z gotowych animacji, `AnimationGroup`, `LaggedStart`, `Succession` i wspólnego `play`, a własną klasę twórz dopiero przy rzeczywistej logice klatkowej.**  
  Źródła: 24 — _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, mf_tools, uwezi.  
  Dowód: `_2018/div_curl/div_curl.py:161`.  
  Obowiązuje dla kompozycji gotowych ruchów bez własnej interpolacji.

- **Twórz własną klasę `Animation`, gdy każda klatka wymaga własnej geometrii, dyskretnego wyboru albo stanu zależnego od `alpha`.**  
  Źródła: 8 — _2016-eola, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2026-cross_entropy, mf_tools, uwezi.  
  Dowód: `_2016/eola/chapter11.py:847`.  
  Obowiązuje, gdy callback ani gotowa kompozycja nie opisują przebiegu.

- **Ogranicz uzasadnioną własną klasę do parametrów, kopii roboczej i `interpolate_mobject`, jeśli bazowe `begin` i `finish` wystarczają.**  
  Źródła: 6 — _2016-eola, _2017-eoc, _2024-puzzles, _2024-transformers, _2026-cross_entropy, uwezi.  
  Dowód: `_2016/eola/chapter11.py:854`.  
  Obowiązuje dla pojedynczej interpolacji bez własnego cyklu życia sceny.

- **Animuj parametr lub `ValueTracker`, a geometrię pozostaw updaterowi, gdy z jednego parametru wynika wiele skutków wizualnych.**  
  Źródła: 13 — _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-optics_puzzles, _2024-holograms, _2024-transformers, _2025-grover, _2025-laplace, _2026-cross_entropy.  
  Dowód: `_2023/optics_puzzles/cylinder.py:133`.  
  Obowiązuje, gdy tracker jest jednym źródłem prawdy dla kilku mobjectów.

- **Dobieraj `rate_func` do znaczenia ruchu: `linear` dla czasu i przepływu, `there_and_back` lub `wiggle` dla akcentu, a lag i okna dla rytmu.**  
  Źródła: 23 — _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, mf_tools, uwezi.  
  Dowód: `_2024/transformers/auto_regression.py:221`.  
  Obowiązuje, gdy tempo jest nośnikiem znaczenia, a nie tylko domyślną krzywą.

- **Modeluj równoległość jako grupę animacji, a kolejność jako sukcesję albo okna czasowe.**  
  Źródła: 21 — _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-holograms, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, uwezi.  
  Dowód: `_2024/transformers/network_flow.py:373`.  
  Obowiązuje dla ruchu wieloczęściowego lub wielofazowego.

## Wejście, przejście i sprzątanie sceny

- **Wprowadzaj geometrię główną rysowaniem, wzrostem lub transformacją, a etykiety i adnotacje osobnym, późniejszym gestem.**  
  Źródła: 23 — _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, uwezi.  
  Dowód: `_2016/eola/chapter1.py:78`.  
  Obowiązuje, gdy obraz i objaśnienie pełnią różne funkcje poznawcze.

- **Ujawniaj serię lub złożoną ilustrację warstwami i w rytmie, zamiast pokazywać wszystkie elementy naraz.**  
  Źródła: 20 — _2016-eola, _2017-eoc, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2026-cross_entropy, _2026-print_gallery, mf_tools, uwezi.  
  Dowód: `_2016/eola/chapter5.py:30`.  
  Obowiązuje dla detali, serii lub etapów budowy, które widz ma odczytać kolejno.

- **Wyprowadzaj element wynikowy z jego znaczącego źródła przez kierunek, kopię, punkt kotwiczący albo łuk.**  
  Źródła: 16 — _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-gauss_int, _2024-antp, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, uwezi.  
  Dowód: `_2024/transformers/auto_regression.py:238`.  
  Obowiązuje, gdy wejście ma komunikować pochodzenie, przepływ lub relację.

- **Transformuj obiekt w następną reprezentację, jeśli zachowuje on ciągłość pojęciową albo wspólne części.**  
  Źródła: 24 — _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, mf_tools, uwezi.  
  Dowód: `_2016/eola/chapter1.py:242`.  
  Nie obowiązuje dla naprawdę nowego, niezwiązanego konceptu.

- **Przygaszaj kontekst potrzebny później, zamiast go usuwać.**  
  Źródła: 18 — _2016-eola, _2017-eoc, _2018-div_curl, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2024-holograms, _2024-puzzles, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, mf_tools.  
  Dowód: `_2016/eola/chapter2.py:565`.  
  Obowiązuje, gdy wcześniejsza konstrukcja pomaga zachować orientację.

- **Czyść efemeryczne kopie, markery, nakładki i adnotacje w skoordynowanej fazie, a po handoffie ustanawiaj kanoniczny obiekt następny.**  
  Źródła: 22 — _2016-eola, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, mf_tools, uwezi.  
  Dowód: `_2016/eola/chapter11.py:306`.  
  Obowiązuje bezpośrednio przed kolejnym etapem, gdy element nie ma już funkcji semantycznej.

## Projektowanie własnych mobjectów

- **Przyjmuj parametry konstrukcji i wyglądu w `__init__` albo konfiguracji, zapisuj je jako stan i buduj kompletny obiekt gotowy do animacji.**  
  Źródła: 24 — _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, mf_tools, uwezi.  
  Dowód: `_2016/eola/chapter5.py:5`.  
  Obowiązuje dla reużywalnego mobjectu; sytuacyjne stany należą zwykle do sceny.

- **Wystawiaj semantycznie istotne części jako nazwane atrybuty w stabilnej hierarchii grup.**  
  Źródła: 24 — _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-grover, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, mf_tools, uwezi.  
  Dowód: `_2016/eola/chapter5.py:33`.  
  Obowiązuje, gdy scena, updater lub metoda klasy ma później sterować częścią niezależnie.

- **Buduj geometrię w klasie albo fabryce, a choreografię pozostaw scenie lub metodzie zwracającej animację.**  
  Źródła: 22 — _2016-eola, _2017-eoc, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt, _2023-clt_proof, _2023-convolutions2, _2023-gauss_int, _2023-optics_puzzles, _2024-holograms, _2024-puzzles, _2024-transformers, _2025-colliding_blocks_v2, _2025-laplace, _2026-cross_entropy, _2026-print_gallery, abul4fia, mf_tools, uwezi.  
  Dowód: `_2016/eola/chapter6.py:152`.  
  Obowiązuje, gdy obiekt ma być używany w wielu scenach.

- **Dla prostego kompozytu używaj parametryzowanej fabryki `Group` lub `VGroup`, a klasę twórz dopiero dla własnego stanu, zachowania albo API.**  
  Źródła: 14 — _2017-eoc, _2022-puzzles, _2022-quintic, _2023-clt_proof, _2023-convolutions2, _2024-antp, _2024-holograms, _2024-puzzles, _2025-colliding_blocks_v2, _2025-grover, _2026-print_gallery, abul4fia, mf_tools, uwezi.  
  Dowód: `_2022/puzzles/subsets.py:6`.  
  Obowiązuje jako decyzja o głębokości abstrakcji, nie jako nakaz używania grupy zawsze.

- **Rozdzielaj kontrakty metod: accessor zwraca dane, fabryka nowy mobject, mutator zmienia i zwraca `self`, a metoda czynności zwraca `Animation`.**  
  Źródła: 12 — _2016-eola, _2019-diffyq, _2022-convolutions, _2023-clt, _2023-gauss_int, _2023-optics_puzzles, _2024-holograms, _2024-transformers, _2025-laplace, _2026-cross_entropy, mf_tools, uwezi.  
  Dowód: `_2026/cross_entropy/distribution.py:52`.  
  Obowiązuje, gdy publiczne API klasy ma służyć i konstrukcji, i animacji bez ukrytej mutacji.

- **Parametryzuj warianty oraz powtarzalne dzieci danymi lub konfiguracją zamiast kopiować konstrukcję.**  
  Źródła: 14 — _2016-eola, _2018-div_curl, _2019-diffyq, _2022-convolutions, _2022-puzzles, _2022-quintic, _2023-clt_proof, _2023-optics_puzzles, _2024-antp, _2024-holograms, _2024-transformers, _2025-colliding_blocks_v2, _2026-print_gallery, uwezi.  
  Dowód: `_2023/optics_puzzles/objects.py:723`.  
  Obowiązuje, gdy algorytm geometrii jest wspólny, a różnią się dane, styl lub orientacja.

- **Przy zmianie danych odtwarzaj zmienny podzespół, zachowując tożsamość kontenera zewnętrznego.**  
  Źródła: 8 — _2018-div_curl, _2023-clt, _2023-gauss_int, _2023-optics_puzzles, _2024-transformers, _2026-cross_entropy, mf_tools, uwezi.  
  Dowód: `20250210_superbarchart.py:46` (uwezi).  
  Obowiązuje, gdy istniejące referencje sceny muszą nadal wskazywać ten sam mobject.

## Sprzeczności

- **Cykl życia updatera:** zawieszaj lub czyść updater przed ręczną transformacją (`_2024/transformers/embedding.py:2898`, `_2023/optics_puzzles/bending_waves.py:354`) kontra wymuszaj `suspend_mobject_updating=False`, gdy animacja ma współdziałać z tym updaterem (`_2023/optics_puzzles/e_field.py:386`, `_2024/holograms/diffraction.py:1833`).

- **Granica własnej klasy `Animation`:** składaj ruch z gotowych animacji zamiast podklasy (`_2018/div_curl/div_curl.py:161`) kontra twórz własną klasę dla logiki wykonywanej w każdej klatce (`_2024/puzzles/max_rand.py:4`, `_2016/eola/chapter11.py:847`).

- **Źródło prawdy animacji:** animuj tracker, a geometrię licz updaterem (`_2023/optics_puzzles/cylinder.py:133`) kontra trzymaj historię ruchu w instancji `Animation` (`_2024/puzzles/max_rand.py:11`).

- **Kontekst po fazie:** przygaszaj element, który ma nadal objaśniać scenę (`_2016/eola/chapter2.py:565`) kontra sprzątaj obiekty pomocnicze przed następną warstwą (`_2023/optics_puzzles/ior_annotations.py:117`, `_2026/cross_entropy/entropy.py:588`).

- **Głębokość abstrakcji mobjectu:** używaj fabryki `VGroup` dla zwykłej kompozycji (`_2022/puzzles/subsets.py:6`) kontra twórz klasę posiadającą stan i updater (`_2023/optics_puzzles/objects.py:144`, `20260128_meterclass.py:4` z uwezi).

## Odsiane jako banał

**34 z 491 obserwacji** odrzucono jako opis API bez decyzji projektowej.

Przykłady: „`VGroup` grupuje elementy”, „`AnimationGroup` uruchamia kilka animacji”, „`LaggedStart` opóźnia elementy”, „`FadeIn` i `FadeOut` przyjmują przesunięcie”, „`always_redraw` odtwarza obiekt”. Zostawały tylko przypadki, w których obserwacja wyjaśniała, kiedy mechanizm wybrać i po co.

## Czego brakuje

- Kryteriów percepcyjnych: tempa czytelnego dla widza, czasu na odczyt wzoru, obciążenia poznawczego i testów z odbiorcami.
- Zasad typografii, kontrastu, palety, dostępności, kompozycji kadru, ruchu kamery oraz synchronizacji z narracją i dźwiękiem.
- Danych o niezawodności: deterministyczności losowości, różnicach wersji Manima i rendererów, testach renderów oraz regresjach wizualnych.
- Kosztów wydajnościowych: kiedy `always_redraw`, kopiowanie, `Transform` albo mnożenie updaterów stają się zbyt drogie.
- Kontraktów dla przyszłej biblioteki idiomów: kompatybilności Community/OpenGL/Cairo, obsługi błędów wejścia, przykładów granicznych i stabilności publicznego API.
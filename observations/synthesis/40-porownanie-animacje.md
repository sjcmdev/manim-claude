# Porównanie syntez reguł animacji w Manimie

## 1. Zgodne

### 1.1. Updatery i stan

- **Wyliczaj stan zależny z bieżącej geometrii albo trackera, bez używania `dt`.** Stosuj, gdy aktualny stan źródła jednoznacznie wyznacza wynik. Źródła: **Terra 24, Sol 23**. Dowód: `_2016/eola/chapter2.py:332`.
- **Używaj `dt` tylko do całkowania czasu, prędkości lub innego stanu zależnego od historii.** Dotyczy fizyki, zegarów, śladów i innych procesów przyrostowych, których nie da się odtworzyć z bieżącej wartości trackera. Źródła: **Terra 16, Sol 14**. Dowód: `_2018/div_curl/div_curl.py:368`.
- **Odtwarzaj złożoną geometrię z aktualnych danych przez `become`, `always_redraw` albo funkcję budującą, zamiast kumulować przesunięcia i deformacje.** Stosuj zwłaszcza przy zmianie kształtu, punktów lub liczby części. Źródła: **Terra 18, Sol 18**. Dowód: `_2018/div_curl/div_curl.py:1302`.
- **Przechowuj stan między klatkami jawnie i tylko wtedy, gdy proces naprawdę zależy od historii.** Może należeć do właściciela albo wydzielonego modelu; aktualizuj go przed geometrią. Dotyczy m.in. śladów, całkowanych trajektorii, stanów dyskretnych, progów i ciągłości gałęzi funkcji. Źródła: **Terra 15, Sol 15**. Dowód: `_2016/eola/chapter2.py:245`.
- **Rozdzielaj producenta stanu od jego wizualizacji i pilnuj kolejności producent–konsument.** Terra łączy separację źródła, geometrii i interakcji w jedną regułę; Sol rozdziela ją na dwie. Źródła: **Terra 10; Sol 6 dla separacji i 2 dla kolejności**. Dowód: `_2023/optics_puzzles/adding_waves.py:808`.
- **Jawnie zarządzaj cyklem życia updatera na granicach ręcznych transformacji, zmiany trybu, kopiowania i usuwania kotwicy.** Zachowaj referencję; zawieszaj, czyść albo wznawiaj updater, chyba że ma celowo współdziałać z animacją. Źródła: **Terra 16, Sol 17**. Dowód: `_2024/transformers/embedding.py:2898`.
- **Wykonaj updater natychmiast po podpięciu, jeśli stan początkowy ma być poprawny przed pierwszą klatką.** Źródła: **Terra 4, Sol 1**. Dowód: `20230605_zoomed.py:33` (uwezi).

### 1.2. Własne klasy `Animation` i choreografia

- **Składaj efekt z gotowych animacji, `AnimationGroup`, `LaggedStart`, `Succession`, updaterów i wspólnego `play`, jeśli nie wnosi własnego algorytmu klatkowego.** Źródła: **Terra 24, Sol 14**. Dowód: `_2018/div_curl/div_curl.py:161`.
- **Twórz własną klasę `Animation`, gdy każda klatka wymaga nowej logiki zależnej od `alpha`, szczególnie dyskretnej, losowej, geometrycznej albo wieloparametrowej.** Źródła: **Terra 8, Sol 6**. Dowód: `_2024/puzzles/max_rand.py:4`.
- **Jeśli standardowy cykl życia wystarcza, ogranicz własną klasę do jawnych parametrów, kopii roboczej i `interpolate_mobject`.** Nie nadpisuj `begin` i `finish` bez potrzeby. Źródła: **Terra 6, Sol 5**. Dowód: `_2016/eola/chapter11.py:854`.
- **Dobieraj `rate_func` do znaczenia ruchu.** `linear` służy czasowi, przepływowi i skanowaniu, `there_and_back` lub `wiggle` — chwilowemu akcentowi, a lag i okna czasowe — rytmowi. Źródła: **Terra 23, Sol 23**. Dowód: `_2024/transformers/auto_regression.py:221`.
- **Grupuj równoległe ruchy opisujące jedno zdarzenie, a kolejne kroki modeluj sukcesją, oknami czasowymi albo osobnymi fazami.** Źródła: **Terra 21, Sol 24**. Dowód: `_2024/transformers/network_flow.py:373`.

### 1.3. Wejście obiektu, przejście i sprzątanie

- **Wprowadzaj główną geometrię i adnotacje odmiennymi gestami oraz w osobnych momentach.** Najpierw ustanów zjawisko rysowaniem, wzrostem lub transformacją, potem je nazwij etykietą, ramą albo strzałką. Źródła: **Terra 23, Sol 23**. Dowód: `_2016/eola/chapter1.py:78`.
- **Ujawniaj serię lub złożoną ilustrację warstwami i w rytmie czytania.** Dla powtarzalnych elementów używaj fali, `lag_ratio` lub okien czasowych zamiast jednoczesnego wejścia całego bloku. Źródła: **Terra 20, Sol 16**. Dowód: `_2016/eola/chapter5.py:30`.
- **Wyprowadzaj wynik albo adnotację z jego znaczącego źródła przez kierunek, kopię, punkt kotwiczący lub łuk.** Stosuj, gdy wejście ma komunikować pochodzenie, przepływ albo relację. Źródła: **Terra 16, Sol 19**. Dowód: `_2024/transformers/auto_regression.py:238`.
- **Transformuj obiekt w semantycznego następcę, gdy zachowuje ciągłość pojęciową lub wspólne części.** Nie stosuj tego do naprawdę nowego, niezwiązanego konceptu. Źródła: **Terra 24, Sol 24**. Dowód: `_2016/eola/chapter1.py:242`.
- **Przygaszaj kontekst nadal potrzebny jako punkt odniesienia, zamiast go usuwać.** Źródła: **Terra 18, Sol 17**. Dowód: `_2016/eola/chapter2.py:565`.
- **Sprzątaj powiązane obiekty tymczasowe jako jedną fazę i równocześnie ustanawiaj trwały, kanoniczny stan następnego kroku.** Po transformacji przez kopię usuń obiekt przejściowy i pozostaw stabilny korzeń sceny. Źródła: **Terra 22; Sol 19 dla sprzątania i 5 dla kanonicznego następcy**. Dowód: `_2016/eola/chapter11.py:306`.

### 1.4. Projektowanie własnych mobjectów

- **Parametryzuj geometrię, wygląd i zachowanie w `__init__` albo konfiguracji oraz buduj kompletny obiekt gotowy do animacji.** Stan sytuacyjny konkretnej sceny zwykle nie należy do reużywalnego mobjectu. Źródła: **Terra 24, Sol 24**. Dowód: `_2016/eola/chapter5.py:5`.
- **Eksponuj semantycznie ważne części jako stabilne dzieci, nazwane atrybuty albo jawne akcesory.** Jest to potrzebne, gdy scena, updater lub metoda klasy ma sterować częścią niezależnie. Źródła: **Terra 24, Sol 22**. Dowód: `_2016/eola/chapter5.py:33`.
- **Dla prostego kompozytu używaj parametryzowanej fabryki zwracającej `Group` lub `VGroup`; klasę twórz dopiero dla własnego stanu, zachowania, cyklu życia albo API.** Źródła: **Terra 14, Sol 9**. Dowód: `_2022/puzzles/subsets.py:6`.
- **Rozdzielaj kontrakty metod.** Akcesor zwraca dane lub widok, fabryka tworzy nowy mobject, mutator zmienia istniejący i zwraca `self`, a metoda czynności zwraca `Animation`. Źródła: **Terra 12; Sol 16 dla całego podziału i 10 dla `return self`**. Dowód: `_2026/cross_entropy/distribution.py:52`.
- **Parametryzuj warianty i powtarzalne dzieci danymi lub konfiguracją zamiast kopiować konstrukcję.** Stosuj, gdy wspólny jest algorytm geometrii, a różnią się dane, styl lub orientacja. Źródła: **Terra 14, Sol 24** (Sol ujmuje tę zasadę szerzej jako parametryzację wariantów). Dowód: `_2023/optics_puzzles/objects.py:723`.
- **Przy zmianie danych zachowuj tożsamość stabilnego kontenera i istniejących referencji.** Aktualizuj stabilne dzieci w miejscu; jeśli zmienia się struktura podzespołu, odtwórz ten podzespół, nie cały zewnętrzny obiekt. Źródła: **Terra 8, Sol 6**. Dowód: `20250210_superbarchart.py:46` (uwezi).

## 2. Tylko w jednej

### 2.1. Tylko Terra

#### Updatery i własne klasy `Animation`

- **Animuj parametr lub `ValueTracker`, a geometrię pozostaw updaterowi, gdy jeden parametr napędza wiele skutków wizualnych.** Źródła: **13**. Dowód: `_2023/optics_puzzles/cylinder.py:133`. Pochodzenie: **Terra**.

#### Projektowanie własnych mobjectów

- **Buduj geometrię w klasie albo fabryce, a choreografię pozostaw scenie lub metodzie zwracającej animację.** Dotyczy obiektów używanych w wielu scenach. Źródła: **22**. Dowód: `_2016/eola/chapter6.py:152`. Pochodzenie: **Terra**.

### 2.2. Tylko Sol

#### Updatery i stan

- **W updaterach tworzonych w pętli wiąż indeks i inne wartości iteracji w argumentach domyślnych domknięcia.** Źródła: **2**. Dowód: `language_tree.py:417` (_2026-cross_entropy). Pochodzenie: **Sol**.
- **Dziel duże `dt` na mniejsze kroki przed numerycznym całkowaniem dynamiki.** Źródła: **1**. Dowód: `driven_harmonic_oscillator.py:37` (_2023-optics_puzzles). Pochodzenie: **Sol**.
- **Używaj nazwanej funkcji do wieloetapowej aktualizacji, a lambdy tylko do pojedynczego, lokalnego powiązania.** Źródła: **12**. Dowód: `integral.py:248` (_2023-gauss_int). Pochodzenie: **Sol**.
- **Używaj `UpdateFromFunc` albo `UpdateFromAlphaFunc` zamiast trwałego updatera dla zależności obowiązującej tylko podczas jednego przejścia.** Źródła: **4**. Dowód: `dice_sims.py:181` (_2023-clt). Pochodzenie: **Sol**.
- **Modeluj krótkotrwały efekt zdarzeniowy jako samousuwający się updater z czasem rozpoczęcia.** Źródła: **1**. Dowód: `blocks.py:1102` (_2025-colliding_blocks_v2). Pochodzenie: **Sol**.
- **Usuwaj element strumienia po opuszczeniu kadru i natychmiast przerywaj jego dalszą aktualizację.** Źródła: **1**. Dowód: `main.py:53` (_2024-antp). Pochodzenie: **Sol**.

#### Własne klasy `Animation` i choreografia

- **Przywracaj `starting_mobject` albo niezależną kopię bazową przed transformacjami zależnymi od `alpha`.** Zapobiega to dziedziczeniu deformacji z poprzedniej klatki. Źródła: **2**. Dowód: `animations.py:26` (mf_tools/uwezi). Pochodzenie: **Sol**.
- **Przyjmuj własne parametry animacji jawnie i przekazuj niezużyte `kwargs` do konstruktora bazowego.** Zachowuje to standardową obsługę `run_time`, `rate_func` i cyklu życia. Źródła: **3**. Dowód: `max_rand.py:5` (_2024-puzzles). Pochodzenie: **Sol**.
- **Steruj postępem istniejącej animacji przez jawne `begin()` i `interpolate_mobject`, jeśli kontrolę nad `alpha` ma przejąć tracker.** Źródła: **1**. Dowód: `robot.py:7916` (_2026-cross_entropy). Pochodzenie: **Sol**.
- **Przygotuj kompletny `target` przed `MoveToTarget`, gdy grupa zmienia jednocześnie układ, skalę, położenie i styl.** Źródła: **4**. Dowód: `dice.py:322` (_2023-clt_proof). Pochodzenie: **Sol**.
- **Mapuj semantycznie odpowiadające sobie fragmenty wzorów, a elementy bez pary wprowadzaj lub usuwaj osobno.** Źródła: **9**. Dowód: `transform_matching_slices.py:18`. Pochodzenie: **Sol**.

#### Wejście i sprzątanie

- **Zostawiaj półprzezroczyste kopie poprzednich stanów, jeśli historia zmiany jest częścią argumentu.** Źródła: **5**. Dowód: `supplements.py:1093` (_2023-gauss_int). Pochodzenie: **Sol**.
- **Wyróżnij fragment przed jego zastąpieniem lub odrzuceniem.** Źródła: **2**. Dowód: `main.py:1007` (_2024-antp). Pochodzenie: **Sol**.
- **Używaj samoczyszczącego cyklu tworzenia i zaniku dla markerów, śladów i diagnostycznych podświetleń.** Źródła: **6**. Dowód: `discrete.py:439` (_2018-div_curl). Pochodzenie: **Sol**.
- **Przenieś czas, wartość albo wynik do trwałego następcy przed usunięciem obiektu dynamicznego.** Źródła: **2**. Dowód: `bending_waves.py:397` (_2023-optics_puzzles). Pochodzenie: **Sol**.

#### Projektowanie własnych mobjectów

- **Buduj punkty prawdziwego własnego `VMobject` w konstruktorze albo `init_points` i wystawiaj charakterystyczne punkty przez akcesory.** Źródła: **5**. Dowód: `chapter6.py:152` (_2016-eola). Pochodzenie: **Sol**.
- **Umieszczaj autonomiczną dynamikę wewnątrz obiektu i wystawiaj scenie jawne sterowanie jej cyklem życia.** Źródła: **8**. Dowód: `shm.py:46` (_2023-optics_puzzles). Pochodzenie: **Sol**.
- **Dołączaj dekorację jako dziecko właściciela, jeśli ma dzielić z nim transformacje i cykl życia.** Źródła: **3**. Dowód: `main.py:636` (_2024-antp). Pochodzenie: **Sol**.
- **Oddziel punkty nośne od parametrów renderera i synchronizuj zmienną geometrię z jego buforem danych.** Źródła: **1**. Dowód: `diffraction.py:43` (_2024-holograms). Pochodzenie: **Sol**.
- **Utrzymuj mapę kluczy do submobjectów jako źródło prawdy i synchronizuj ją z hierarchią grupy.** Źródła: **1**. Dowód: `dual_compatibility.py:37` (mf_tools). Pochodzenie: **Sol**.

## 3. Sprzeczności

Poniższe pary pozostają nierozstrzygnięte. Część z nich może być poprawna po obu stronach przy różnych warunkach, ale materiał nie daje wspólnego, testowalnego kryterium wyboru.

### 3.1. Czy updater ma działać podczas ręcznej animacji tego samego obiektu?

- **Zawieszaj albo czyść updater**, aby nie konkurował z `Transform`: `_2024/transformers/embedding.py:2898`, `_2023/optics_puzzles/bending_waves.py:354`, `_2025/colliding_blocks_v2/blocks.py:1706`.
- **Pozostaw updater aktywny przez `suspend_mobject_updating=False`**, jeśli ma współtworzyć ruch: `_2023/optics_puzzles/e_field.py:386`, `_2024/holograms/diffraction.py:1833`.

### 3.2. Gdzie ma mieszkać stan historyczny?

- **Na mobjectcie:** `div_curl.py:368` (_2018-div_curl), `part1/pendulum.py:333` (_2019-diffyq), `objects.py:434` (_2023-optics_puzzles), `language_tree.py:754` (_2026-cross_entropy).
- **Poza mobjectem, w domknięciu albo modelu:** `supplements.py:917` (_2023-gauss_int), `mlp.py:2483` (_2024-transformers).

Terra dopuszcza obie lokalizacje w jednej regule; Sol zapisuje je jako alternatywne praktyki bez kryterium wyboru.

### 3.3. Ile updaterów powinno obsługiwać współzależną strukturę?

- **Rozdzielaj źródło oraz niezależne właściwości na osobne updatery:** `continuous.py:1102` (_2023-convolutions2), `integral.py:440` (_2023-gauss_int), `ml_basics.py:2213` (_2024-transformers).
- **Przeliczaj całą grupę atomowo w jednym updaterze:** `subsets.py:650` (_2022-puzzles), `roots_and_coefs.py:465` (_2022-quintic), `exponentials.py:1173` (_2025-laplace).

### 3.4. Gotowa kompozycja czy własna klasa `Animation`?

- **Składaj gotowe animacje:** Terra podaje 24 źródła, Sol 14; dowody reprezentatywne: `_2018/div_curl/div_curl.py:161`, `continuous.py:1919` (_2023-convolutions2).
- **Twórz klasę dla własnej logiki klatkowej:** Terra podaje 8 źródeł, Sol 6; dowody: `_2024/puzzles/max_rand.py:4`, `_2016/eola/chapter11.py:847`.

Obie syntezy opisują warunek słownie, ale żadna nie daje testowalnej granicy między „kombinacją efektów” a „nowym algorytmem klatkowym”.

### 3.5. Tracker czy instancja `Animation` jako źródło prawdy przebiegu?

- **Animuj tracker, a geometrię obliczaj updaterem:** `_2023/optics_puzzles/cylinder.py:133`.
- **Przechowuj historię ruchu w instancji `Animation`:** `_2024/puzzles/max_rand.py:11`.

### 3.6. Kto ma być właścicielem choreografii?

- **Scena buduje animacje, a obiekt lub fabryka dostarcza geometrię:** `main.py:497` (_2023-clt_proof), `cylinder.py:199` (_2023-optics_puzzles), `added_dimension.py:1486` (_2024-puzzles).
- **Mobject wystawia gotowe animacje albo sam wykonuje ruch:** `roots_and_coefs.py:600` (_2022-quintic), `helpers.py:713` (_2024-transformers), `robot.py:39` (_2026-cross_entropy).

Terra formułuje kompromis „scena albo metoda zwracająca animację”; Sol pozostawia obie praktyki naprzeciw siebie.

### 3.7. Czy `rate_func` dobierać jawnie?

- **Dobieraj `rate_func` do semantyki ruchu:** 23 źródła w obu syntezach; `integral.py:521` (_2023-gauss_int).
- **Steruj rytmem przez `run_time`, `lag_ratio` i `path_arc`, pozostawiając domyślną `rate_func`:** `main.py:856` (_2023-clt_proof).

### 3.8. Przygaszać czy usuwać kontekst po fazie?

- **Przygaszaj element, który nadal objaśnia scenę:** `_2016/eola/chapter2.py:565`, `integral.py:79` (_2023-gauss_int).
- **Sprzątaj obiekty pomocnicze przed następną warstwą:** `_2023/optics_puzzles/ior_annotations.py:117`, `_2026/cross_entropy/entropy.py:588`.

### 3.9. Fabryka `VGroup` czy własna klasa mobjectu?

- **Używaj fabryki dla zwykłej kompozycji:** `_2022/puzzles/subsets.py:6`.
- **Twórz klasę posiadającą stan, updater lub autonomiczne API:** `_2023/optics_puzzles/objects.py:144`, `20260128_meterclass.py:4` (uwezi), `shm.py:46` (_2023-optics_puzzles).

### 3.10. Rekonstruować czy mutować geometrię?

- **Odtwarzaj zmienną geometrię lub podzespół z aktualnych danych:** `_2018/div_curl/div_curl.py:1302`, `20250210_superbarchart.py:46` (uwezi).
- **Aktualizuj stabilne dzieci w miejscu, a nowy obiekt twórz dopiero przy zmianie struktury lub znaczenia:** `main.py:59` (_2024-antp).

To napięcie dotyczy także granicy tożsamości: Terra akcentuje zachowanie kontenera zewnętrznego przy odbudowie podzespołu, Sol — zachowanie dzieci i ich updaterów przy mutacji in-place.

## 4. Różnice w podejściu

### 4.1. Granularność i organizacja

- **Terra** kondensuje materiał do **26 reguł** w czterech działach odpowiadających obszarom zbioru. Częściej scala kilka decyzji w jedną regułę, np. separację updaterów z ich kolejnością oraz sprzątanie z ustanowieniem kanonicznego następcy.
- **Sol** wyodrębnia **46 reguł** w ośmiu działach. Zachowuje więcej technicznych przypadków brzegowych: domknięcia w pętli, podział dużego `dt`, `starting_mobject`, ręczne sterowanie `alpha`, shadery, mapy kluczy i samousuwające się updatery.
- Skutek dla biblioteki idiomów: Terra lepiej nadaje się do wyboru zasad nadrzędnych, Sol do dopisywania warunków, wyjątków i wariantów implementacyjnych.

### 4.2. Liczenie źródeł

Przy wielu regułach o tym samym sensie liczebności są różne: bez-`dt` **24/23**, `dt` **16/14**, natychmiastowa inicjalizacja **4/1**, gotowe animacje **24/14**, własna `Animation` **8/6**, fabryka grup **14/9** (Terra/Sol). Nawet przy deklarowanym **18/18** dla rekonstrukcji geometrii listy różnią się pojedynczym źródłem. Liczb nie należy więc sumować ani traktować jako wspólnej miary siły dowodu bez ponownego uzgodnienia sposobu grupowania obserwacji.

### 4.3. Traktowanie sprzeczności

- **Terra** częściej zamienia konflikt w warunkową regułę nadrzędną („czyść updater, chyba że ma współbiec”; „fabryka dla kompozytu, klasa dla stanu/API”). Jednocześnie wskazuje pięć par sprzecznych praktyk.
- **Sol** częściej zachowuje warianty jako osobne, konkretne zalecenia i wskazuje pięć konfliktów, w tym właściciela historii, liczbę updaterów, właściciela choreografii i politykę `rate_func`.
- Po połączeniu obu ujęć pozostaje dziesięć osobnych osi decyzji opisanych w sekcji 3; część jest konfliktem bezpośrednim, część brakiem kryterium wyboru między poprawnymi wariantami warunkowymi.

### 4.4. Co obie syntezy odsiały jako banał

- **Terra** podaje **34 z 491 obserwacji** odrzuconych jako opis API bez decyzji projektowej. Przykłady: „`VGroup` grupuje elementy”, „`AnimationGroup` uruchamia kilka animacji”, „`LaggedStart` opóźnia elementy”, „`FadeIn` i `FadeOut` przyjmują przesunięcie”, „`always_redraw` odtwarza obiekt”.
- **Sol** podaje **6 reguł** odrzuconych z tego samego powodu. Przykłady: uruchamianie niezależnych ruchów równolegle w jednym `play`, składanie ruchów przez `AnimationGroup` i `LaggedStart`, budowanie własnej klasy `AnimationGroup` z animacji składowych oraz grupowanie równoległych transformacji w `AnimationGroup`.
- Różna jednostka raportowania („obserwacje” kontra „reguły”) nie pozwala bezpośrednio porównać liczb 34 i 6.

### 4.5. Zidentyfikowane braki materiału

- **Narracja, percepcja i odbiorcy:** Terra wskazuje brak kryteriów tempa, czasu na odczyt wzoru, obciążenia poznawczego i testów z odbiorcami; Sol dodaje intencję narracyjną, błąd rozumowania widza, synchronizację z lektorem, rytm zdań i pomiary zrozumienia.
- **Czytelność i kompozycja:** Terra wymienia typografię, kontrast, paletę, dostępność, kadr, kamerę oraz synchronizację z narracją i dźwiękiem; Sol dodaje minimalne rozmiary, daltonizm, napisy, rozdzielczości, `z_index`, kolejność renderowania, maskowanie, clipping, antyaliasing i nakładanie 2D/3D.
- **Wydajność:** obie syntezy nie znajdują progów kosztu `always_redraw`, `become`, kopiowania, `Transform`, shaderów, wielu updaterów i dużych hierarchii.
- **Niezawodność i testy:** Terra wskazuje brak danych o deterministyczności, rendererach, testach renderów i regresji wizualnej; Sol dodaje kluczowe klatki, artefakty między klatkami, ekstremalne `dt`, puste grupy, zera, nieciągłości, zmianę liczby dzieci, błędne wejścia oraz zachowanie po wyjątku, pominięciu animacji, przewijaniu i przerwanym renderze.
- **Reprodukowalność:** Sol osobno zaznacza brak polityki ziaren losowych i porównywalnych renderów.
- **Kompatybilność i kontrakty biblioteki:** Terra wymienia Community/OpenGL/Cairo, obsługę błędów, przypadki graniczne i stabilność publicznego API; Sol podkreśla mieszanie generacji `manimlib`, wersji API i rendererów.
- **Granice modelu:** Sol wskazuje brak kryterium własności stanu i choreografii między sceną, mobjectem i modelem oraz brak danych o kosztach utrzymania tych wariantów.
- **Waga obszarów:** Sol ostrzega, że niemal równy rozkład obserwacji 128/118/122/123 może wynikać ze schematu ekstrakcji, a nie z praktycznej ważności czterech obszarów.

## 5. Rekomendacja kolejności przeglądu

1. **Najpierw sekcja 3 — sprzeczności.** Ustal polityki biblioteki dla: aktywności updatera podczas animacji, właściciela historii, liczby updaterów, progu własnej `Animation`, źródła prawdy przebiegu, właściciela choreografii, `rate_func`, przygaszania kontra sprzątania, fabryki kontra klasy oraz rekonstrukcji kontra mutacji.
2. **Potem zgodne reguły z najmocniejszą zbieżnością.** Zacznij od tych z równymi lub niemal równymi liczebnościami: rekonstrukcja geometrii, semantyczny `rate_func`, rozdzielenie geometrii od adnotacji, semantyczny następca i parametryzacja mobjectu.
3. **Następnie zgodne reguły z dużą rozbieżnością liczby źródeł.** Przed awansem sprawdź ponownie próbki dla natychmiastowej inicjalizacji updatera, kompozycji gotowych animacji, własnej `Animation` i fabryki `Group`/`VGroup`.
4. **Dopiero potem reguły znalezione przez jedną syntezę.** Najpierw rozważ wieloźródłowe idiomy Sol i dwa szerokie idiomy Terra, a przypadki jednoźródłowe traktuj jako kandydatów wymagających dodatkowej walidacji, nie jako reguły ogólne.
5. **Na końcu nałóż wymagania biblioteczne spoza korpusu.** Przed publikacją ustal kompatybilność wersji i rendererów, budżety wydajności, deterministyczność, testy regresji wizualnej, obsługę parametrów skrajnych, przerwania cyklu oraz kryteria dostępności i czytelności.

# Grill autorski — runda 1: anty-wzorce

Zapis ustaleń z sesji wydobywania technik manimowych od autora. Trzecie źródło
obserwacji, obok mielenia kodu 3b1b (task/04) i analizy wideo (task/06).

Data sesji: 2026-09-08/09. Metoda: wywiad, pytania pojedynczo, przy każdym
rekomendacja prowadzącego. Plan: dwa pełne przebiegi — runda 1 od anty-wzorców,
runda 2 systematycznie po kategoriach.

Status: **runda 1 w toku.** Reguły poniżej nie mają jeszcze przykładów, więc żadna
nie jest gotowa do awansu.

## Ustalenia o samym procesie

**Dowodem dla reguły autorskiej jest para własnych przykładów, nie cytat z cudzego
materiału.** Minimalna scena łamiąca regułę plus minimalna przechodząca. Grill idzie
bez dowodów dla szybkości, przykłady dorabiamy po nim. Uzasadnienie: falsyfikowalność
wychodzi z konstrukcji, kod jest własny, więc ShareAlike nie dotyczy, a `TODO.md:189`
(task/20) i tak wymaga dokładnie takiej pary do lintu.

**`idioms/` przyjmuje praktykę autora tam, gdzie nie rozjeżdża się z tym, co model
generuje poprawnie.** Nie dodajemy pola `audience` do każdej reguły; oznaczamy tylko
te, przy których rozjazd faktycznie wystąpił. Na razie dwie: relacje wielkości oraz
przekazywanie parametrów.

## Reguły wydobyte

### Kompozycja i pozycjonowanie

**Kadr ma jedną kotwicę; pozycje wiążą się w łańcuch do niej, a nie stoją niezależnie.**
Kotwicą bywa obiekt centralny albo funkcja generująca powtarzalny zestaw — to zależy
od sceny i nie da się rozstrzygnąć z góry. Falsyfikowalne zostaje samo istnienie
łańcucha.

**Używaj `next_to` i `move_to` zamiast `shift`.** Potwierdzone przez autora jako
praktyka, ale sam wskazuje, że to nie tu leży trudność. Niska nowość — ta reguła
jest już przykładem wzorcowym w `design-spec.md`.

**Wyrównuj przez `aligned_edge` w `next_to` oraz przez metodę `align_to`, zamiast
korygować pozycję po fakcie.**

**Dobieranie `buff` w relacji do skali i wymiarów obiektów pochłania dużo czasu.**
Ból nazwany, reguła jeszcze nie zbudowana. Kandydat: `buff` wyrażony względem wymiaru
obiektu, nie jako liczba bezwzględna.

**Relacje wielkości (`scale`, `font_size`, `stretch_to_fit_*`) to najtrudniejszy
element na starcie.** Autor przyznaje, że nie ma tu systemu — u niego to zawsze
fine-tuning. Reguła będzie więc *przepisana dla agenta*, nie wydobyta z praktyki:
jeden obiekt referencyjny, reszta wyprowadzona względem niego. Autor uznaje to za
sensowne zwłaszcza w kontekście pracy modelu.

### Modularność i parametry

**Buduj najpierw bezpośrednio w scenie, wyciągaj do funkcji dopiero wtedy, gdy
parametry są znane.** Autor odrzucił nazwanie cyklu „wywołanie → sygnatura → ciało"
anty-wzorcem: to jest cena modularności, nie błąd. Regułą jest kolejność — przedwczesna
faktoryzacja jest przyczyną, skakanie po kodzie tylko objawem.

**Parametry zestawu obiektów przekazuj strukturą, nie rosnącą listą argumentów.**
Praktyka autora: lista specyfikacji w miejscu wywołania, funkcja tylko po niej iteruje.
Wariant dla modelu: dataclass z dostępem jak do słownika (`item["foo"]`). Rozjazd
odnotowany.

### Czas i tempo

**Scena wystawia mały zestaw nazwanych pokręteł czasowych; każdy pozostały czas jest
z nich wyprowadzony proporcją.** Sama kolejność zdarzeń nie wystarcza — potrzebna jest
możliwość rozciągnięcia i ściśnięcia całości bez ruszania wielu miejsc.

**Pokrętło dostaje czas związany z czymś spoza animacji: z widzem albo z rzeczywistą
skalą zjawiska. Wszystko, co wynika z wewnętrznej logiki animacji, jest proporcją
swojego rodzica.** Test złamania: przy każdej liczbie czasu pytamy, czy stoi tam
z powodu widza, czy z powodu innej animacji; literał z tego drugiego powodu łamie regułę.

**Główna animacja sceny sterowana niezależnie: szybkość i długość jako osobne
parametry, plus liczba powtórzeń dla ruchu okresowego.** `run_time` skleja szybkość
z długością w jedną liczbę i nie odróżnia „obraca się wolno przez 3 sekundy" od
„obraca się szybko przez 3 sekundy".

**Animacje zaawansowane definiuj proceduralnie i wywołuj z metody.** Poziom
definiowania — metoda, klasa czy funkcja — pozostaje otwarty.

### Reset i powroty

**Reset techniczny jest cięciem, nie animacją.** Animowany powrót do stanu wyjściowego
widz czyta jako cofanie pomyłki, czyli sygnał, że poprzednie sekundy się nie liczyły.

Kolejność preferencji ustalona przez autora:

1. Nie resetuj — buduj następny stan z bieżącego.
2. Jeśli reset musi być widoczny w obrębie sceny, schowaj go za wygaszeniem, ruchem
   kamery albo wejściem nowego elementu.
3. Dopiero na końcu: reset jako cięcie na granicy sceny.

**Powrót niosący treść nie jest resetem.** Pokazanie, że operacja jest odwracalna,
albo rozpoznawalny powrót po dygresji, to pełnoprawna animacja i podlega tym samym
regułom co każda inna.

### Wierność fizyczna

**Naginanie i przekłamywanie jest dozwolone.** Stanowisko autora, przyjęte wprost:
biblioteka nie stawia w tej sprawie wymogu. Prowadzący zgłaszał zastrzeżenie do
przypadku oznaczonej podziałki lub liczby w kadrze — zastrzeżenie odnotowane, nie
przyjęte. Decyzja świadoma, nie luka.

## Granularność sceny — dane pomiarowe

Zmierzone na klonie `3b1b/videos`, klasy dziedziczące po `Scene`:

```
_2016/eola            502 sceny    44 linie na scenę
_2025/laplace         190          77
_2023/optics_puzzles  113         113
_2026/cross_entropy   100         164
_2024/holograms        69          89
```

`holograms` to jeden film — 69 klas `Scene`, czyli około 20 sekund gotowego wideo
na klasę. Styl autora ewoluował w stronę większych klas: 44 linie w 2016, 164 w 2026.

**Zastrzeżenia autora do tej metryki, istotne:**

Liczba linii na scenę nie jest dobrą miarą, ponieważ zbudowanie sceny bywa warte
tysiąca linii numeryki i dopracowania wizualnego — ale ten kod jest następnie
**ponownie używany**. To jest właśnie modularność, do której zmierzamy. Miara musi
więc oddzielać treść sceny od maszynerii wielokrotnego użytku.

Wysoką liczbę scen zawyżają cytaty, otwarcia, zamknięcia i bardzo krótkie wstawki,
które z perspektywy tego projektu są nieciekawe.

### Miara poprawiona: długość ciała `construct`

Zastrzeżenie autora dało się rozstrzygnąć pomiarem. Maszyneria wielokrotnego użytku
nie leży w `construct`, tylko w klasach pomocniczych i funkcjach, więc treść sceny
mierzymy samą orkiestracją:

```
                     scen  mediana  średnia   p90   max
_2016/eola            479     18       24      51    143
_2023/optics_puzzles  147     24       55     108    778
_2025/laplace         202     24       61     144    716
_2024/holograms        67     28       79     267    671
_2024/transformers    216     28       70     156   1330
_2026/cross_entropy   121     30      118     294   1725
```

**Mediana trzyma się przedziału 18–30 linii przez całą dekadę**, mimo że średnia
wielkość pliku i klasy rosła. Granularność beatu okazuje się stabilna; zmienił się
ogon. W 2016 nie było scen dłuższych niż 143 linie, później pojawiają się orkiestracje
sięgające 1725 linii.

Reguła kandydacka: **orkiestracja sceny mieści się w około 30 liniach; `construct`
przekraczający ~150 linii robi za dużo i powinien zostać podzielony albo oddać
maszynerię do funkcji.** Sprawdzalne mechanicznie, niezależnie od objętości
kodu pomocniczego.

### Wzory i tekst

**Wzór może pojawić się w kadrze bez wcześniejszego wprowadzenia wizualnego.**
Propozycja prowadzącego, żeby uczynić z tego twardą regułę, została **odrzucona**:
zależy to od celu animacji i jest decyzją użytkownika.

## Runda 2 — systematycznie po kategoriach

### Czytelność

**Grubość obrysu przy ruchomej kamerze.** Autor wskazuje testowanie `stroke_width`
przy `ZoomedScene` i `MovingCameraScene` jako uciążliwe i czasochłonne, wymagające
fine-tuningu. Pozostałe drogi do nieczytelności — zlewanie się kolorów po kompresji,
za mały tekst, informacja niesiona wyłącznie kolorem — dotknęły go „po trochu każda",
bez wyraźnego zwycięzcy.

Reguła, potwierdzona niezależnie w dwóch źródłach społecznościowych:

**Zadeklaruj, czym jest obrys — tuszem czy substancją.** Tusz jest konwencją rysunku
(osie, strzałki, adnotacje, ramki) i ma wyglądać tak samo niezależnie od zoomu, więc
wiąże się go updaterem z szerokością kadru. Substancja jest rzeczą, która naprawdę ma
grubość (wiązka, przewód, ścianka), i skaluje się razem z obiektem. Stała liczba
w scenie z ruchomą kamerą jest błędem, nie wyborem.

Falsyfikowalne mechanicznie: w scenie dziedziczącej po `MovingCameraScene` lub
`ZoomedScene` każdy `stroke_width` jest albo związany z kadrem, albo jawnie skalowany
z obiektem; goły literał łamie regułę.

Dowody: `MF_Tools/src/MF_Tools/rescaling.py` implementuje obie intencje jako osobne
funkcje — `maintain_apparent_stroke_width` (tusz) i `scale_with_stroke_width`
(substancja). `uwezi` znalazł to samo niezależnie (`scale-ze-stroke`) wraz z wariantem
przy dużym zoomie, gdzie obrys ramki kamery wchodzi w powiększany obraz, a naiwną
reakcją jest dobieranie coraz cieńszego `stroke_width` do konkretnego poziomu zoomu.

**Uwaga metodologiczna:** korpus 3b1b nie zawiera o tym praktycznie nic. To pierwszy
przypadek, w którym źródła społecznościowe (ManimCE) okazały się wyraźnie lepsze niż
mielenie kodu 3b1b (ManimGL) — argument za utrzymaniem czwartego źródła.

**Za mały tekst.** Potwierdzony przez autora jako problem występujący czasami.

Reguła ma tę samą strukturę co obrys: mierzy się wynik, nie parametr. Deklarowany
`font_size` przestaje cokolwiek znaczyć po `.scale()` i po ruchu kamery, więc
sprawdzalna jest wysokość napisu w jednostkach kadru w chwili renderu. Kontrolę da
się wykonać na etapie blockoutu, zanim powstanie treść.

Otwarte: czy próg jest jeden, czy dwa — tekst pierwszoplanowy kontra referencyjny
(podpisy osi, indeksy, numery przy krzywych), który bywa świadomie drobny.

**Zlewanie się kolorów po kompresji — odrzucone jako bolączka.** Autorowi się to nie
zdarzyło.

Reguła „kolory niosące różne znaczenia różnią się jasnością, nie tylko barwą"
pozostaje kandydatem, ale **bez poparcia w doświadczeniu autora**. Uzasadnienie jest
wyłącznie dostępnościowe: różnica jasności utrzymuje rozróżnialność dla widza
z zaburzeniem widzenia barw. Sprawdzalna mechanicznie z wartości RGB. Do rozstrzygnięcia
przy kuracji, nie na podstawie tego grillu.

### Stan i updatery

**Updater jest właściwością obiektu, nie zachowaniem sceny.** Pisany pod konkretny
obiekt i konkretną sytuację, więc jego czas życia jest czasem życia obiektu.

Hipoteza prowadzącego o wyciekających updaterach — walka updatera z jawną animacją
o ten sam mobject, updater dziedziczony po sekcji — została **odrzucona**: przy takim
sposobie pisania ten problem nie ma jak powstać. Reguła „każde `add_updater` ma parę
w `remove_updater`" jest więc niepotrzebna.

Autor stosuje zasadę pojedynczej odpowiedzialności: jedna funkcja, jedno zadanie.
Ogólniejsze updatery przy złożonych zestawach scen pozostają niewykluczone, ale autor
się z tym nie zetknął.

**Updater podpinaj jawnie i definiuj jako nazwaną funkcję, najlepiej zwracaną
z funkcji zewnętrznej. `always_redraw` zarezerwuj dla obiektów tanich w budowie.**

Autor zgłosił to jako czystą preferencję stylistyczną; pomiar pokazał, że jest to
praktyka produkcyjna z uzasadnieniem wydajnościowym:

```
3b1b, roczniki 2022+          społeczność (gisty, MF_Tools)
add_updater      1062         add_updater       93
always_redraw     112         always_redraw    112
f_always          144
def update…       258
```

3b1b podpina jawnie w stosunku 9,5 : 1; społeczność woli `always_redraw` 1,2 : 1
w drugą stronę. Rozjazd tłumaczy rodzaj materiału: `always_redraw` odbudowuje obiekt
w każdej klatce, więc przy tanim obiekcie wygrywa zwięzłością i dominuje w gistach,
a przy kosztownym jest pułapką wydajnościową. Łączy się to z bolączką z rundy 1 —
render przy wielu updaterach trwający długie minuty.

### Dane a obraz

**Wewnątrz updatera nie ma solvera ani całkowania. Symulacja liczy się raz, wynik
ląduje w tablicy lub w pliku, updater tylko odczytuje.** Przy symulacji sterowanej
`ValueTracker`-em: tablica na siatce parametru plus interpolacja, nie liczenie na żywo.

Autor uznaje to za dobrą praktykę, ale **jej nie stosuje** — koszt ręcznego zbudowania
pipeline'u i abstrakcji przewyższa doraźny ból, a zwykle potrzebuje czegoś na szybko.

Prowadzący wyciągnął z tego wniosek, że taki idiom nie zadziała bez wsparcia
narzędziowego, bo `scene-coder` odziedziczy tę samą wymówkę. **Autor to odrzucił,
i ma rację.** Koszt, który go powstrzymuje, to dzień lub dwa na obmyślenie
architektury i przypadków brzegowych, zakodowanie, przetestowanie — z niepewnym
wynikiem. Dowolny model wykonuje tę samą pracę w mniej niż godzinę.

Stąd ustalenie odwrotne i ważniejsze: **ograniczenie, które powstrzymuje człowieka,
nie wiąże agenta.** Biblioteka może więc zawierać idiomy, których człowiek świadomie
nie stosuje, bo mu się nie opłacają — i to jest część wartości produktu, a nie jego
niespójność. Nie oznaczamy takich reguł jako wymagających wsparcia; oznaczamy je co
najwyżej jako kosztowne dla człowieka, tanie dla agenta.

**Strojenie wartości przez proof-of-concept w matplotlibie**, zanim cokolwiek trafi
do Manima. Praktyka autora, zgłoszona jako uzupełnienie.

### Ponowne użycie

Prowadzący postawił hipotezę, że przeżywa to, co „nie wie, że jest w filmie", a ginie
to, co ma wbudowaną wiedzę o kadrze. Autor zgodził się z kierunkiem, ale wskazał
kontrprzykład: w serii o jednym zagadnieniu (jego przypadek to centra NV) funkcja
budująca strukturę elektronową i poziomy energetyczne jest uniwersalna i nie wymaga
pisania od nowa, mimo że wygląda na związaną z konkretną sceną.

Sformułowanie poprawione — hipoteza mieszała dwie niezależne osie:

**Specjalizacja dziedzinowa nie ma związku ze zdolnością do ponownego użycia.**
To, *co* funkcja buduje, nie przesądza o tym, *gdzie* to postawi.

**Ponowne użycie zabija wyłącznie wiedza o kadrze i o narracji**: samodzielne
pozycjonowanie, kolor dobrany pod jedną scenę, podpis dobrany pod jeden argument.
Sprawdzalne: w funkcji przeznaczonej do ponownego użycia nie ma `to_edge`, `move_to`
ze stałą, ani nazwy koloru wybranej pod konkretną scenę — pozycjonowanie, kolor
i podpis nakłada wywołujący.

**Specjalizacja wyznacza zasięg ponownego użycia, nie jego brak.** Trzy poziomy:
jedna scena, jedna seria, dowolny projekt. Błędem nie jest napisanie czegoś wąsko,
tylko umieszczenie tego na złym poziomie.

Konsekwencja dla task/10: struktura `package/` plus `tooling/` nie przewiduje miejsca
na bibliotekę współdzieloną w obrębie jednej serii — a według autora to jest poziom,
na którym powstaje najwięcej wartościowego kodu. **Autor zatwierdził dodanie poziomu
serii do struktury repozytorium.**

### Dekompozycja

**Podział na sceny jest aktem planowania, nie odkryciem po fakcie.** Autor decyduje,
co idzie do której sceny, już na etapie myślenia o animacji; struktura czasowa z tego
wynika, a nie odwrotnie. Czytelność pliku zapewnia zasada pojedynczej
odpowiedzialności, koszt renderu jest oczywistym ograniczeniem, a reszta to intuicja
i doświadczenie.

Hipoteza prowadzącego — że scenę należy dzielić, gdy nie da się wyprowadzić wszystkich
czasów z jednego zestawu pokręteł — jest prawdziwa, ale opisuje **skutek**, a nie
przyczynę, i nie nadaje się jako procedura decyzyjna.

To doprecyzowuje potwierdzoną wcześniej granicę: **`plan` decyduje, `idioms/`
sprawdza.** Reguła mechaniczna nie jest sposobem podejmowania decyzji, tylko testem,
czy podjęta decyzja się broni. Intuicji nie da się zakodować; jej wynik da się
zweryfikować. Dotyczy to wszystkich reguł wyprowadzonych w tym grillu.

## Zasada nadrzędna: oddziel pętlę drogą od taniej

Wyszła trzykrotnie, niezależnie, z trzech różnych pytań grillu:

- **blockout na prostokątach** — układ zatwierdzony, zanim wejdzie treść,
- **symulacja policzona wcześniej** — fizyka rozstrzygnięta, zanim zacznie się
  strojenie kadru,
- **proof-of-concept w matplotlibie** — wartości dostrojone przed uruchomieniem Manima.

Za każdym razem chodzi o to samo: rzecz kosztowna rozstrzyga się raz, a rzecz
poprawiana dwadzieścia razy nie ciągnie jej za sobą. Kandydat na zasadę
architektoniczną całego produktu, nie na trzy osobne wskazówki.

## Progi liczbowe należą do konfiguracji, nie do reguły

Ustalenie autora przy okazji progu wielkości tekstu, ale ogólne:

**Reguła orzeka, że niezmiennik jest spełniony; liczba, z którą się porównuje, mieszka
w konfiguracji pakietu.** Idiom brzmi „tekst nie jest mniejszy niż próg", nie „tekst
ma co najmniej 0,2 jednostki". Inaczej biblioteka zaszywa założenie o widzu i o tym,
na czym ogląda — a to zależy od materiału, nie od sztuki animacji.

Konsekwencje:

- `config.default.yaml` (task/11) dostaje klucze progowe.
- Lint (task/20) czyta progi z konfiguracji, zamiast mieć je wpisane w regułę.

Punkt odniesienia dla wartości domyślnej, gdyby był potrzebny: kadr Manima ma
8 jednostek wysokości, co przy 1080p daje 135 pikseli na jednostkę; granica komfortu
czytania na telefonie to około 24–30 pikseli, czyli mniej więcej 0,2 jednostki.

## Granica tego, co `idioms/` może zawierać

Dwa razy w rundzie 1 proponowana reguła spadła do „decyduje użytkownik": przy
identyfikacji głównej animacji i przy kolejności wzór–obraz. Obie dotyczyły
**wyboru narracyjnego**, nie mechaniki.

**Granica potwierdzona przez autora.** Biblioteka opisuje decyzje strukturalne
i mechaniczne, sprawdzalne przez spojrzenie na kod lub storyboard. Decyzje o tym,
co film ma powiedzieć i w jakiej kolejności, należą do użytkownika i trafiają do
`plan`, nie do `idioms/`.

Konsekwencje:

- **Kryterium filtrujące dla kuratora (task/08):** reguła, której nie da się sprawdzić
  bez wiedzy o zamyśle filmu, nie jest idiomem. Dotyczy to również filtrowania 324
  reguł wydobytych z kodu 3b1b.
- **Kategoria `narracja` w większości wypada z `idioms/`.** Pozostałe kategorie ze
  schematu obserwacji — kompozycja, czas i tempo, czytelność, dekompozycja, stan
  i updatery, ponowne użycie, dane a obraz — zostają, bo są sprawdzalne mechanicznie.
- W kategorii `czas-i-tempo` granica przechodzi w poprzek: mechanika pokręteł
  i proporcji zostaje, ocena „jak długo to ma się wydawać" odchodzi do użytkownika.

## Wątki otwarte

- Poziom definiowania: metoda, klasa czy funkcja — dla animacji proceduralnych.
- `buff` wyrażony względem wymiarów obiektu.

Zamknięte w trakcie rundy 1:

- Miara granularności sceny — rozstrzygnięta pomiarem długości `construct`.
- Identyfikacja głównej animacji — rozstrzygnięta jako decyzja użytkownika, nie
  właściwość wyprowadzalna z materiału (patrz niżej).

## Nie idiomy — wymagania wobec produktu

Wyszły przy okazji grillu, nie należą do `idioms/`:

**Strojenie czasu nie może wymagać pełnego renderu.** Iteracje przy scenach z wieloma
updaterami trwają długie minuty nawet w niskiej rozdzielczości. Zakres task/16 i task/18.

**Blockout na prostokątach.** Agent układa scenę i przejścia między scenami na
prostokątach w niskiej rozdzielczości; treść wchodzi dopiero po zatwierdzeniu układu
i widoczności. Rozbraja trzy nazwane bóle naraz: relacje wielkości, koszt iteracji
renderu oraz ocenę widoczności przez `visual-judge`. Zakres task/12, 13, 16, 17.

**Kompozycja czasowa sceny wymaga kontroli — logicznej i wizualnej.** Zakres task/17.

**Główna animacja jest ustalana z użytkownikiem, nie wyprowadzana z materiału.**
Decyzja autora: sekcja może mieć więcej niż jedną główną animację, agent ma prawo
proponować, ale rozstrzyga użytkownik podczas sesji planowania. Skutki:

- `plan` (task/12) musi zadać to pytanie jawnie w trakcie samo-grillu.
- `storyboard` (task/13) musi mieć na to pole, bo bez niego `scene-coder` nie wie,
  czemu przyznać pokrętła czasowe, a `visual-judge` nie wie, czego pilnować.

Reguła „sekcja ma dokładnie jedną główną animację" została **odrzucona** — liczba
mnoga jest dopuszczona świadomie.

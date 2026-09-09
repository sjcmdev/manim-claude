# Grill autorski — runda 1: anty-wzorce

Zapis ustaleń z sesji wydobywania technik manimowych od autora. Trzecie źródło
obserwacji, obok mielenia kodu 3b1b (task/04) i analizy wideo (task/05).

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
(task/19) i tak wymaga dokładnie takiej pary do lintu.

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

## Granica tego, co `idioms/` może zawierać

Dwa razy w rundzie 1 proponowana reguła spadła do „decyduje użytkownik": przy
identyfikacji głównej animacji i przy kolejności wzór–obraz. Obie dotyczyły
**wyboru narracyjnego**, nie mechaniki.

**Granica potwierdzona przez autora.** Biblioteka opisuje decyzje strukturalne
i mechaniczne, sprawdzalne przez spojrzenie na kod lub storyboard. Decyzje o tym,
co film ma powiedzieć i w jakiej kolejności, należą do użytkownika i trafiają do
`plan`, nie do `idioms/`.

Konsekwencje:

- **Kryterium filtrujące dla kuratora (task/07):** reguła, której nie da się sprawdzić
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
updaterami trwają długie minuty nawet w niskiej rozdzielczości. Zakres task/15 i task/17.

**Blockout na prostokątach.** Agent układa scenę i przejścia między scenami na
prostokątach w niskiej rozdzielczości; treść wchodzi dopiero po zatwierdzeniu układu
i widoczności. Rozbraja trzy nazwane bóle naraz: relacje wielkości, koszt iteracji
renderu oraz ocenę widoczności przez `visual-judge`. Zakres task/11, 12, 15, 16.

**Kompozycja czasowa sceny wymaga kontroli — logicznej i wizualnej.** Zakres task/16.

**Główna animacja jest ustalana z użytkownikiem, nie wyprowadzana z materiału.**
Decyzja autora: sekcja może mieć więcej niż jedną główną animację, agent ma prawo
proponować, ale rozstrzyga użytkownik podczas sesji planowania. Skutki:

- `plan` (task/11) musi zadać to pytanie jawnie w trakcie samo-grillu.
- `storyboard` (task/12) musi mieć na to pole, bo bez niego `scene-coder` nie wie,
  czemu przyznać pokrętła czasowe, a `visual-judge` nie wie, czego pilnować.

Reguła „sekcja ma dokładnie jedną główną animację" została **odrzucona** — liczba
mnoga jest dopuszczona świadomie.

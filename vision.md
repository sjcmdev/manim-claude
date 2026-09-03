# manim-claude — założenia projektu

Dokument dla współpracowników. Odpowiada na pytania: co budujemy, dla kogo, dlaczego to ma
sens i czym różni się od tego, co już istnieje.

## 1. Problem

Dobra animacja edukacyjna jest kosztowna nieproporcjonalnie do swojej wartości. Wykładowca,
który potrafi wyjaśnić zjawisko przy tablicy w trzy minuty, potrzebuje kilku dni, żeby zrobić
z tego animację — i zwykle rezygnuje. Bariera nie leży w fizyce ani w dydaktyce, tylko
w narzędziu.

Modele językowe teoretycznie tę barierę znoszą, ale w praktyce nie. Poproszony o scenę Manima
model zwraca kod, który:

- korzysta z API, którego nie ma w zainstalowanej wersji,
- ustawia obiekty na sztywnych współrzędnych, przez co połowa wychodzi poza kadr,
- animuje wszystko w jednym tempie, bez hierarchii uwagi,
- jest napisany jednym ciągiem, więc nie da się go poprawić bez przepisania,
- nikt go nie obejrzał przed oddaniem, bo model nie widzi tego, co wygenerował.

Ostatni punkt jest sednem. Kod, który się kompiluje, i animacja, która wygląda dobrze,
to dwie różne rzeczy, a typowy przepływ pracy z modelem sprawdza tylko pierwszą z nich.

## 2. Co budujemy

Narzędzie, które przyjmuje to, co wykładowca ma naprawdę pod ręką:

- opis słowny tego, co chce pokazać,
- notatki, skrypt wykładu, artykuł, prezentację,
- odręczny szkic — na tablecie albo zdjęcie kartki,

a zwraca gotową animację Manim, powstałą w procesie z **weryfikacją wizualną** i
**bramkami akceptacji**, w którym człowiek zatwierdza kierunek w trzech miejscach i nie
musi robić nic więcej.

Sercem narzędzia nie jest prompt. Sercem jest **autorska biblioteka idiomów i wzorców
projektowania animacji** — skodyfikowana wiedza o tym, jak wygląda dobra animacja
edukacyjna — oraz agenty piszące kod, które z tej biblioteki korzystają.

## 3. Dla kogo

**Odbiorca pierwszy: wykładowca bez umiejętności technicznych.** Zakładamy realistycznie,
że nie skonfiguruje środowiska sam. Zakładamy natomiast, że w zespole albo wśród studentów
jest jedna osoba znająca podstawy Claude Code. Ta osoba uruchamia narzędzie; wykładowca
wrzuca własne slajdy i notatki i dostaje animację **w swojej kolejności tłumaczenia**, a nie
w kolejności narzuconej przez model.

**Odbiorca drugi: my.** Projekt `University-Of-Physics` produkuje kurs Manima dla fizyków.
To narzędzie przyspiesza produkcję materiału i jest jednocześnie poligonem, na którym
sprawdzamy własne tezy dydaktyczne.

Produkt jest niekomercyjny.

## 4. Dlaczego to ma szansę zadziałać

Trzy rozstrzygnięcia odróżniają ten projekt od generatora promptów.

### 4.1 Model naprawdę ogląda to, co zrobił

Manim potrafi wyrenderować pojedynczą klatkę w kilka sekund i podzielić scenę na sekcje,
z których każda renderuje się osobno. Wykorzystujemy to jako pętlę zwrotną: model generuje
kod, renderuje klatkę, **patrzy na obraz**, porównuje z planem i poprawia. To jest różnica
między "kod się kompiluje" a "animacja wygląda tak, jak miała wyglądać".

### 4.2 Wiedza jest skodyfikowana, nie improwizowana

Budujemy bibliotekę reguł — kompozycja kadru, tempo i pauzy, obsługa stanu, czytelność,
anty-wzorce — z dwóch źródeł: analizy publicznie dostępnego kodu i filmów 3Blue1Brown oraz
własnego doświadczenia w Manimie. Każda reguła musi być **falsyfikowalna**: da się spojrzeć
na kod albo na animację i orzec, czy została złamana. Reguły, których nie da się sprawdzić,
odrzucamy — to nie są reguły, tylko motywacje.

Biblioteka jest kuratorowana, nie zbierana automatycznie. Wpis staje się idiomem dopiero
wtedy, gdy autor projektu świadomie go zatwierdzi.

### 4.3 Człowiek zatwierdza kierunek, nie szczegóły

Trzy bramki blokujące:

1. **Plan** — czytelny dokument z narracją, listą bloków i tabelą parametrów. Poprawiasz
   prozę, zanim powstanie linijka kodu.
2. **Statyczny układ** — jedna klatka z każdego bloku, wszystkie obiekty na miejscach, zero
   animacji. Większość nieporozumień typu "nie o to mi chodziło" widać właśnie tutaj, za
   kilka sekund renderu zamiast kilku minut.
3. **Pełny podgląd** — gotowy materiał ze znacznikami, do których można się odnieść
   precyzyjnie ("blok WavePacket, sekcja 2, za szybko").

Pomiędzy bramkami system pracuje sam, z twardym limitem prób i limitem czasu.

## 5. Czego świadomie nie robimy

**Nie weryfikujemy fizyki.** Źródłem prawdy dla wzorów, stałych i modeli jest użytkownik.
Zakładamy, że wykładowca zna swoją dziedzinę lepiej niż model. System nigdy nie zmienia po
cichu podanego wzoru; jeśli czegoś nie rozumie, pyta. Rezygnacja z weryfikacji symbolicznej
i biblioteki "sprawdzonych modeli" zmniejsza zakres o rząd wielkości i usuwa całą klasę
fałszywych alarmów.

**Nie budujemy własnego frameworka nad Manimem.** Wygenerowany projekt jest samowystarczalny:
żyje w repozytorium git użytkownika i nie zależy od naszego pakietu w czasie działania.

**Nie zaczynamy od instalatora.** Bootstrap środowiska jest realnym problemem, ale rozwiążemy
go na końcu, gdy będzie wiadomo, co dokładnie trzeba zainstalować.

**Nie obsługujemy jeszcze ManimGL ani Blendera.** Plan i storyboard projektujemy jednak bez
odwołań do konkretnego API, żeby drugi backend był dopisaniem jednego agenta, a nie
przepisaniem systemu.

## 6. Kwestie prawne

Analizujemy publiczne repozytorium `3b1b/videos`, które jest udostępnione na licencji
CC BY-NC-SA 4.0. Nasz produkt jest niekomercyjny, więc klauzula NonCommercial nie stoi na
przeszkodzie, ale klauzula ShareAlike zaraziłaby projekt, gdyby powstało dzieło zależne.

Dlatego obowiązuje reguła bezwzględna: **żaden plik ani fragment kodu z tego repozytorium
nie trafia do naszego drzewa.** Analiza odbywa się w katalogu tymczasowym, a jej wynikiem
jest wyłącznie własna proza opisująca zaobserwowane regularności — czyli idee i metody, które
nie podlegają prawu autorskiemu. Reguła jest egzekwowana maszynowo przez hook, a nie dobrą
wolą. Pochodzenie inspiracji wskazujemy w dokumentacji, wraz z opisem wartości dodanej.

## 7. Co odróżnia nas od tego, co już istnieje

Istnieją publiczne zbiory "best practices dla Manima" przeznaczone dla agentów. Są to
statyczne dokumenty z regułami. Nasza przewaga nie leży w samej wiedzy, tylko w **procesie**:

| istniejące rozwiązania | manim-claude |
|---|---|
| zbiór reguł do wklejenia w kontekst | biblioteka reguł plus pipeline, który je egzekwuje |
| brak weryfikacji wyniku | render i ocena wizualna w pętli |
| wynik akceptujesz albo nie | trzy bramki, na których korygujesz kierunek |
| jeden wielki plik sceny | bloki renderowane niezależnie, sklejane automatycznie |
| brak pamięci między projektami | profil narracji i preferencje użytkownika utrwalone |

## 8. Stan projektu

Etap projektowania zakończony. Wszystkie decyzje architektoniczne są rozstrzygnięte
i zapisane w `design-spec.md` wraz z uzasadnieniami; przebieg ustaleń w `decision-log.md`.
Kod nie powstał. Kolejne kroki i podział prac: `roadmap.md`.

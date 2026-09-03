# manim-claude — zapis ustaleń projektowych

Data wywiadu: 2026-09-02
Metoda: wywiad rundowy — pytania zadawane falami, każda odpowiedź otwierała kolejne gałęzie
drzewa decyzyjnego. Zapis służy temu, żeby rozstrzygnięcia nie były renegocjowane bez powodu
i żeby nowa osoba w projekcie zobaczyła nie tylko decyzję, ale i odrzucone alternatywy.

Skróty: **P** — pytanie, **O** — odpowiedź, **U** — uzasadnienie.

---

## Runda 1 — zakres i podstawy

**P1. Czy to nowy front-end istniejącego pipeline'u kursu, czy osobny produkt?**
**O:** Osobny, niezależny produkt. Cel: skodyfikować i udostępnić wiedzę o szybkim,
efektywnym i modularnym pisaniu w Manimie, żeby wykładowcy bez umiejętności technicznych —
wspierani przez jedną osobę znającą Claude Code — produkowali animacje na podstawie notatek
i książek. Przy okazji przyspiesza produkcję kursu `University-Of-Physics`.

**P2. Czy render może być automatyczny, skoro w repozytoriach kursu obowiązuje zakaz?**
**O:** Tak. Ustalono, że zakaz pochodzi z własnych plików `CLAUDE.md` i `AGENTS.md`
repozytoriów kursu i dotyczy wyłącznie ich.
**U:** Powodem zakazu była czytelność kodu lekcji i czas oczekiwania. W nowym produkcie
render jest jedynym sposobem sprawdzenia, czy obraz wygląda tak, jak miał wyglądać.

**P3. Skąd agent bierze prawdę o API Manima?**
**O:** Dokumentacja przez `context7`, ale wiedza ma być zaszyta w agentach, skillach, hookach
i w samej idei projektu, nie doklejana ad hoc.

**P4. Jak wygląda wejście?**
**O:** Plik lub pliki plus tekstowy prompt użytkownika.

**P5. Ile warstw pośrednich między pomysłem a kodem?**
**O:** Trzy, z osobnym źródłem prawdy, żeby model nie musiał testować wzorów i algorytmów.

**P6. Blender?**
**O:** Odroczony.

---

## Runda 2 — dystrybucja, weryfikacja, wiedza

**P7. Kształt dystrybucji i instalacja.**
**O:** Instalacją zajmujemy się na końcu. Zakładamy, że użytkownik obsługuje Claude Code
albo Codex, ewentualnie ich wersje w VS Code.

**P8. Ile harnessów wspieramy w wersji pierwszej?**
**O:** Tylko Claude Code.

**P9. Jak działa pętla renderu?**
**O:** Kluczowa jest kolejność: najpierw ustalenie głównych obiektów sceny, potem budowa
statycznych scen kawałek po kawałku z użyciem mechanizmu sekcji. Następnie render pojedynczej
klatki dla potwierdzenia rozmieszczenia obiektów, następnie render kolejnych sekcji. Trzeba
rozróżniać, które fragmenty zależą od siebie, a które nie — jedna scena powinna zawierać
wyłącznie rzeczy wzajemnie zależne. Sklejanie ffmpeg-iem, uruchamianie scen z różnymi
parametrami. Pełny materiał na końcu większego kroku, dla potwierdzenia intencji.
System musi zatrzymywać się w odpowiednich momentach i czekać na walidację użytkownika.

**P10. Źródło prawdy dla fizyki.**
**O:** Prawdą jest to, co powie użytkownik. Ufamy, że zna fizykę na tyle, by nie podawać
błędnych wzorów.
**U:** Odrzucono weryfikację symboliczną (sympy), bibliotekę zweryfikowanych modeli i osobny
etap kontroli fizyki. Zakres zmniejszony o rząd wielkości.

**P11. Skąd bierze się wiedza o dobrym kodzie Manima?**
**O:** Wywiad z autorem, tematycznie, usprawniany w trakcie pracy.

**P12. Modularność: biblioteka runtime czy wzorce?**
**O:** Projekt użytkownika ma być samowystarczalny i żyć w jego repozytorium git.

---

## Runda 3 — struktura i weryfikacja

**P13. Jedna klasa `Scene` z sekcjami czy wiele klas?**
**O:** Wiele klas, w stylu 3b1b. Parametryzacja przez metody tworzące obiekty i animacje
oraz atrybuty klasy. Dodatkowo: przeanalizować publiczny kod 3b1b, wyekstrahować regularności
i opakować je w ogólne dobre praktyki programistyczne — bazujemy na **podejściu do
projektowania animacji**, nie na konkretnym API.
**U:** Wcześniejsza analiza sugerująca trudność parametryzacji była błędna i została
odrzucona przez autora.

**P14. `plan.md` czy `storyboard.yaml`?**
**O:** Oba. `plan.md` weryfikuje i poprawia użytkownik, `storyboard.yaml` jest z niego
generowany.

**P15. Czy hooki mają renderować automatycznie po zapisie?**
**O:** Nie. Hooki wykonują tanie bramki, render jest jawnym krokiem skilla.

**P16. Które bramki blokują?**
**O:** Plan i pełny podgląd blokują zawsze. Statyczny layout jest opcją całego pakietu.

**P17. Parametryzacja scen.**
**O:** Kombinacja pliku parametrów i podklas-wariantów. Dodatkowo: system ma wyławiać
parametry z rozmowy i z dokumentów i zapisywać je do weryfikacji — to naturalny moment
na interwencję użytkownika.

**P18. Jak kończy się samo-grill agenta?**
**O:** Stała lista kategorii dwuznaczności. Agent wypełnia ją samodzielnie i pyta wyłącznie
o pola, których nie da się wywnioskować.

---

## Runda 4 — źródła, licencje, tryby awarii

**P19. Jak korzystać z 3b1b wobec licencji CC BY-NC-SA?**
**O:** Produkt jest niekomercyjny. Wskazujemy pochodzenie inspiracji, jednocześnie zaznaczając
wartość dodaną.
**U:** Ustalono, że `3b1b/videos` jest na CC BY-NC-SA 4.0. Wyciąganie idei i metod jest
dozwolone, kopiowanie ekspresji nie. Klauzula ShareAlike zaraziłaby projekt, gdyby powstało
dzieło zależne, stąd bezwzględny zakaz wprowadzania materiału do drzewa projektu, egzekwowany
hookiem.

**P20. Zakres i metoda analizy.**
**O:** Reprezentatywny wybór, żeby nie zapchać kontekstu: transformata Laplace'a (trzy filmy),
obliczenia kwantowe (dwa), hologramy, cała playlista Optics Puzzles, Origin of Light i pokrewne,
seria o splocie, rozkładzie Gaussa i CLT, serie o algebrze liniowej, rachunku
różniczkowo-całkowym, równaniach różniczkowych i transformacie Fouriera, równania Maxwella.
Preferować nowsze filmy. Analizować również pod kątem wzorców projektowych i architektonicznych.
**U:** Wykryto sprzeczność: część wymienionych serii pochodzi z lat 2016–2018, co kłóci się
z preferencją nowszych. Rozstrzygnięcie zaakceptowane przez autora — nowe serie jako źródło
wzorców kodu, stare klasyki wyłącznie jako źródło wzorców narracyjnych, bez analizy kodu.

**P21. Rozjazd `plan.md` i `storyboard.yaml`.**
**O:** Przy każdej regeneracji powstaje nowa wersja YAML-a, stara trafia do archiwum.
Niedestruktywnie — ktoś może chcieć wrócić.

**P22. Bramka statycznego layoutu.**
**O:** Domyślnie włączona.

**P23. Kształt tabeli parametrów.**
**O:** Wartość, jednostka, pochodzenie, status. Tabela ląduje w `plan.md`, żeby dała się łatwo
edytować; do YAML-a wchodzą wyłącznie dane potwierdzone.

**P24. Obsługa awarii renderu.**
**O:** Rozdzielić błędy techniczne od intencjonalnych. Przy technicznych warto odwołać się do
mocniejszego modelu, zanim zapytamy użytkownika. Tryb pętli jako dodatkowa konfiguracja,
domyślnie włączona.

---

## Runda 5 — narzędzia, modele, wywiad

**P25. ManimCE, ManimGL czy oba?**
**O:** ManimCE teraz; plan i storyboard bez nazw z API, żeby dodanie ManimGL było dopisaniem
jednego agenta.

**P26. Agent nadzorujący czy skill orkiestrujący?**
**O:** Skill orkiestrujący ze stanem w plikach, mechanika w skryptach. Przydział modeli:
Opus do orkiestracji i oceny wizualnej, Sonnet do pisania scen i analizy, skrypty bez modelu.
Zapewnić elastyczność wyboru.

**P27. Sceny-próbki do testowania stylu.**
**O:** Tak, z wnioskiem zapisywanym trwale. Zastrzeżenie autora: uważać na code smell, łatwo
naprodukować bzdur.

**P28. Drabina eskalacji.**
**O:** Eskalacja tylko dla błędów technicznych; liczba prób konfigurowalna na poziomie
całego systemu.

**P29. Plan wywiadu o idiomy.**
**O:** Sesje tematyczne, przed każdą czyszczony kontekst i mały preprompt; ewentualnie
osobni agenci na temat, żeby nie czytać tego samego wielokrotnie. Część tematów — kompozycja,
czytelność, storytelling — można oddelegować do zewnętrznego czatu, podając mu materiał wideo.

**P30. Lokalizacja repozytorium produktu.**
**O:** Osobny projekt.

---

## Runda 6 — wymiana z zewnętrznym czatem, jakość biblioteki

**P31. Podział pracy między analizę kodu a analizę filmów.**
**O:** Kod lokalnie przez subagentów; transkrypcja i siatka klatek do zewnętrznego czatu.
Format odpowiedzi: sztywny YAML zgodny ze schematem, nie proza. Przygotować szablon promptu.
**U:** Ustalono, że `yt-dlp` potrafi pobrać same napisy z czasami, a klatki kluczowe wyciąga
ffmpeg — to zmniejsza koszt o dwa rzędy wielkości względem pobierania filmów i daje artefakt
powtarzalny.

**P32. Ochrona biblioteki przed zaśmieceniem.**
**O:** Na razie wszystko wchodzi, ale Sonnet przeprowadza automatyczną kategoryzację
i grupowanie; przegląd zaczyna się od pozycji uznanych za najlepsze.

**P33. Jak zbierać ocenę estetyczną.**
**O:** Podczas generowania zostawiać znaczniki, do których użytkownik może się odnosić.
Formularz na etapie testowania. System uczy się preferencji konkretnego użytkownika na
podstawie zwrotnych informacji.
**U:** Sprostowano mechanizm: hook nie zbiera odpowiedzi, robi to skill zadający pytanie
z wyborami. Znacznikiem jest para `blok.sekcja`, dostępna za darmo z indeksu sekcji Manima.

**P34. Wierność szkicu.**
**O:** Ustawienie z kilkoma poziomami, do zaproponowania.

**P35. Nazwa.**
**O:** `manim-claude` — utylitarnie proste, od razu wiadomo, o co chodzi.

---

## Runda 7 — profil, pamięć, kategoryzacja

**P36. Styl narracji: profil użytkownika czy materiał projektu?**
**O:** Rozdzielone. Profil na poziomie użytkownika, materiały na poziomie projektu.
Użytkownik ma móc wgrać prezentację albo wskazać preferowany sposób narracji.

**P37. Gdzie mieszka to, czego system uczy się o użytkowniku?**
**O:** Nie wymagać od użytkownika pisania. Ankieta, plus presety typów filmu, dzięki czemu
problem częściowo rozwiązuje się sam.

**P38. Kryterium rankingu obserwacji.**
**O:** Ocena jakości wzorca przez model, w połączeniu z powtarzalnością.
**U:** Falsyfikowalność pozostaje wymaganym polem wpisu — bez niej reguła nie zasili lintu —
ale nie jest kryterium sortowania.

**P39. Domyślna wierność szkicu.**
**O:** Różna dla różnych typów dokumentów: inaczej traktujemy figurę z książki, inaczej
prezentację, inaczej szybki szkic na tablecie.

---

## Runda 8 — korekty autorskie

Autor zgłosił trzy braki w syntezie, wszystkie przyjęte:

**K1. Rdzeniem produktu jest biblioteka idiomów i agenty piszące kod.** Samodoskonalenie
systemu jest sprawą wtórną.
**U:** Wcześniejsza propozycja fazowania "najpierw szkielet, potem biblioteka" odwracała
priorytety produktu. Zastąpiona podziałem na dwa niezależne tory, które mogą powstawać
równolegle.

**K2. Trzeba jasno oddzielić nasze narzędzia deweloperskie od tego, co trafia do paczki.**
**U:** Stąd rozdział `package/` i `tooling/`, egzekwowany testem zakazującym importów.
Hook chroniący przed materiałem na ShareAlike należy do `tooling/`, bo tylko autorzy mają
kontakt z tym materiałem.

**K3. Przydział modeli ma być konfiguracją całego systemu.**
**U:** Wszystkie role modelowe trafiły do `config.default.yaml`, nic nie jest zaszyte w kodzie.

**P40. Czy paczka zawiera narzędzia do mielenia?**
**O:** Nie. Idiomy są nasze, wyekstrahowane z kodu 3b1b i wypracowane niezależnie.
Użytkownik może wyłącznie dopisywać własne, do osobnego pliku.
**U:** Konsekwencja: informacja zwrotna od użytkownika trafia do jego `lessons`, a nie do
idiomów rdzeniowych. Wcześniejsza propozycja awansowania wniosków z próbek do rdzenia została
wycofana.

**P41. Czy biblioteka idiomów jest wersjonowana osobno?**
**O:** Tak, niezależnie od kodu narzędzia; paczka deklaruje zgodną wersję.

---

## Odrzucone kierunki

Zapis tego, czego świadomie nie robimy, jest równie ważny jak zapis decyzji.

| kierunek | powód odrzucenia |
|---|---|
| Weryfikacja fizyki przez sympy i biblioteka zweryfikowanych modeli | Prawdą jest użytkownik; usuwa całą klasę fałszywych alarmów i zmniejsza zakres |
| Osobny etap kontroli fizycznej przed projektowaniem sceny | Rozdmuchiwał proces; kontrola mieści się w bramce planu |
| Hooki renderujące automatycznie po zapisie pliku | Render wymaga obejrzenia przez model z kontekstem, czego hook nie potrafi; kosztowałby czas bez efektu |
| Agent-nadzorca trzymający kontekst całego projektu | Najdroższa możliwa konstrukcja; warunki na plikach sprawdza skrypt za zero tokenów |
| Dwa backendy (ManimCE i ManimGL) od pierwszego dnia | Podwaja pracę, zanim wiadomo, czy produkt jest dobry |
| Katalog-intake, w którym system sam wykrywa nowe pliki | Zgadywanie, co jest świeże, zawodzi |
| Notatki z vaulta jako źródło prawdy w produkcie publicznym | Cudzy wykładowca nie ma dostępu do prywatnego vaulta |
| Skala liczbowa ocen (1–5) | Nie niesie informacji, co zmienić |
| Pobieranie pełnych plików wideo do analizy | Napisy z czasami plus klatki kluczowe dają to samo za dwa rzędy wielkości mniej |
| Fazowanie "szkielet przed biblioteką" | Odwracało priorytety produktu; zastąpione dwoma równoległymi torami |
| Awans preferencji użytkownika do idiomów rdzeniowych | Rdzeń jest autorski i kuratorowany; preferencja osobista to nie reguła sztuki |

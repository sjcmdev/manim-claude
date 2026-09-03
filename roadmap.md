# manim-claude — plan realizacji

Dokument roboczy dla zespołu. Co powstaje, w jakiej kolejności, kto może co przejąć
i po czym poznamy, że etap jest skończony.

Podstawa techniczna: `design-spec.md`. Uzasadnienie biznesowe: `vision.md`.

## 1. Dwa niezależne tory

Projekt dzieli się na dwa strumienie prac, które **nie blokują się nawzajem** i mogą
powstawać równolegle. To jest najważniejsza informacja organizacyjna w tym dokumencie:
dwie osoby mogą zacząć jednocześnie, bez uzgadniania kodu.

### Tor A — biblioteka (rdzeń wartości)

```text
kod 3b1b + transkrypcje + klatki  ->  observations/  ->  kuracja  ->  idioms/ + reguly lintu
```

Produkuje skodyfikowaną wiedzę o projektowaniu animacji. Nie potrzebuje działającego
pipeline'u. Wynik jest wartościowy sam w sobie — nawet gdyby reszta projektu nie powstała,
biblioteka idiomów jest użyteczna przy każdej pracy z Manimem.

### Tor B — harness produkcyjny

```text
wejscie  ->  plan.md  ->  storyboard.yaml  ->  build  ->  assemble  ->  podglad
```

Produkuje maszynę, która zamienia opis w animację. Działa z pustym idiom-bookiem — po prostu
generuje przeciętny kod. Nie czeka na tor A.

Tory spotykają się w jednym punkcie: agent `scene-coder` czyta `idioms/`.

**Zalecenie:** tor B powinien wcześnie mieć jeden działający blok jako poligon, na którym
weryfikujemy reguły z toru A. Reguły, których nie ma na czym sprawdzić, łatwo stają się
zbiorem pobożnych życzeń.

## 2. Etapy

### Etap 1A — pierwsza biblioteka idiomów

**Cel:** przejść od zera do zestawu falsyfikowalnych reguł, z których agent kodujący
naprawdę korzysta.

Zadania:

1. `fetch_reference.py` — pobieranie napisów z czasami (`yt-dlp --write-auto-sub
   --skip-download`) i klatek kluczowych (ffmpeg) do katalogu roboczego poza repozytorium.
2. `no_3b1b_code.py` — hook blokujący wprowadzenie materiału objętego CC BY-NC-SA do drzewa
   projektu. **Powstaje przed pierwszym pobraniem czegokolwiek**, nie po.
3. Agent `code-miner` — analiza kodu scen w katalogu tymczasowym, wynik jako YAML obserwacji.
   Zakres: serie z roku 2022 i późniejsze. Analiza obejmuje warstwę wzorców projektowych
   i architektonicznych, nie tylko idiomy powierzchniowe.
4. Analiza narracji przez zewnętrzny czat — transkrypcje plus siatki klatek, sztywny format
   odpowiedzi YAML (szablon promptu w `design-spec.md`, rozdział 9.4). Zakres obejmuje także
   starsze klasyki, ale wyłącznie na poziomie budowy wyjaśnienia.
5. `merge_observations.py` — scalanie YAML-i do `observations/`.
6. Agent `idiom-curator` — kategoryzacja i ranking.
7. Przegląd autorski i pierwsze `idioms/` w wersji 0.1.

**Skończone, gdy:** `idioms/` zawiera zestaw reguł, z których każda jest falsyfikowalna
i opatrzona uzasadnieniem, a `VERSION` wynosi 0.1.

**Można przejąć:** punkty 1, 2, 5 są samodzielnymi zadaniami inżynierskimi bez zależności.

---

### Etap 1B — szkielet, który chodzi

**Cel:** od promptu i szkicu do sklejonego materiału wideo, z trzema bramkami.

Zadania:

1. Struktura repozytorium: `package/` i `tooling/` plus test zakazujący importów z `tooling/`
   do `package/`.
2. `config.default.yaml` z pełnym zestawem kluczy (modele, bramki, limity, wierność szkicu).
3. Skill `plan` — samo-grill wg stałej listy kategorii, ekstrakcja parametrów z pochodzeniem,
   interpretacja szkicu wg poziomu wierności. Wynik: `plan.md`. **Bramka 1.**
4. Generator `storyboard.yaml` z `plan.md`, z wersjonowaniem i archiwum.
   Hook `storyboard_integrity.py` pilnujący rozdziału sekcji `generated` i `state`.
5. Agent `scene-coder` — jedna klasa `Scene` z nazwanymi sekcjami na blok.
6. Hook `check_scene_contract.py` — tanie bramki: parsowanie, obecność klasy w storyboardzie,
   nazwane sekcje.
7. Render klatki statycznej plus `contact_sheet.py`. **Bramka 2.**
8. Agent `visual-judge` — ocena klatek względem planu, konkretne poprawki.
9. Render sekcji z `skip_animations`, `sections.py` jako parser indeksu JSON.
10. `build.py` — orkiestracja, sklejanie klas przez ffmpeg. **Bramka 3.**

**Skończone, gdy:** jedno realne zagadnienie fizyczne przechodzi całą drogę od opisu do
sklejonego materiału, a wszystkie trzy bramki działają.

**Można przejąć:** punkty 1, 2, 4, 9, 10 to zadania skryptowe bez udziału modelu i bez
zależności od pozostałych.

---

### Etap 2 — egzekwowanie i próbki

1. `lint-rules.yaml` — reguły falsyfikowalne z `idioms/` przełożone na sprawdzenia w hooku
   `check_scene_contract.py`. Tu tory A i B faktycznie się łączą.
2. Skill `probe` — izolowana brudna scena rozstrzygająca jedno pytanie stylistyczne.
3. Znaczniki `blok.sekcja` wypalane w rogu renderów roboczych; znikają w renderze finalnym.

**Skończone, gdy:** złamanie reguły z biblioteki jest wychwytywane automatycznie przy zapisie
pliku, a użytkownik może odnieść się do konkretnego momentu materiału jednym identyfikatorem.

---

### Etap 3 — pamięć i personalizacja

1. Skill `profile` — ankieta plus presety typów filmu, bez wymagania pisania prozy.
   Wynik: `~/.manim-claude/narration-profile.md`.
2. `lessons.yaml` — preferencje użytkownika zbierane na bramkach, obowiązujące globalnie
   z możliwością wyjątku projektowego.
3. `idioms-local.yaml` — miejsce na własne reguły użytkownika, czytane po rdzeniowych.

Zasada: preferencje użytkownika **nigdy** nie awansują do idiomów rdzeniowych. Rdzeń jest
autorski i kuratorowany.

**Skończone, gdy:** dziesiąty projekt tego samego użytkownika startuje z jego tempem
i kolejnością tłumaczenia bez powtarzania ustawień.

---

### Etap 4 — ManimGL

Drugi agent kodujący. Zakres ograniczony do jednego pliku agenta, ponieważ `plan.md`
i `storyboard.yaml` są z założenia wolne od nazw z API.

**Warunek wejścia:** etapy 1A i 1B zamknięte, przynajmniej trzy materiały wyprodukowane
na ManimCE.

---

### Etap 5 — Blender

Przeniesienie kształtu procesu (wejście, plan, kod, weryfikacja, bramki), nie kodu. Blender
różni się zasadniczo: API jest stanowe, operatory zależą od kontekstu, a weryfikacja
wizualna wymaga innego mechanizmu renderowania.

**Warunek wejścia:** proces na Manimie udowodniony w praktyce.

---

### Etap końcowy — dystrybucja

Bootstrap środowiska, sprawdzanie zależności, degradacja bez LaTeX-a, opis instalacji.
Świadomie na końcu: dopiero wtedy wiadomo, co dokładnie trzeba zainstalować.

## 3. Podział na role

| rola | zakres | etapy |
|---|---|---|
| Kurator biblioteki | Ostateczna decyzja o wpisach w `idioms/`, prowadzenie wywiadów, przegląd rankingu | 1A, 2 |
| Inżynier pipeline'u | Skrypty, hooki, orkiestracja, ffmpeg, wersjonowanie storyboardu | 1B, 2 |
| Autor promptów agentów | `scene-coder`, `visual-judge`, `plan`, kategorie samo-grillu | 1B, 3 |
| Testerzy treści | Realne materiały wykładowe przepuszczone przez pipeline, feedback na bramkach | od 1B |

Role mogą się pokrywać. Rozdzielenie kuratora od inżyniera jest jednak istotne: kurator
decyduje, co jest dobrą animacją, i ta decyzja nie powinna zależeć od tego, co łatwo
zaimplementować.

## 4. Zasady pracy

1. **Stan mieszka w plikach, nie w kontekście rozmowy.** Każdy krok czyta plik, pisze plik
   i zostawia status. Sesję można przerwać w dowolnym momencie i wrócić bez powtarzania
   ustaleń. To jedyny powód, dla którego system nie rozsypie się przy dziesiątym materiale.
2. **Hooki są tanie i deterministyczne.** Żaden hook nie renderuje i nie wywołuje modelu.
   Render jest jawnym krokiem, ponieważ jego wynik musi ktoś obejrzeć.
3. **`package/` nie importuje z `tooling/`.** Pilnowane testem. Bez tego za trzy miesiące
   paczka pociągnie za sobą narzędzia deweloperskie.
4. **Reguła musi być falsyfikowalna albo nie jest regułą.** "Używaj przemyślanej kompozycji"
   odpada. "Nie ustawiaj współrzędnych ręcznie, gdy istnieje `.next_to()` lub `.arrange()`"
   zostaje.
5. **Żadnego materiału objętego ShareAlike w drzewie projektu.** Egzekwowane hookiem.
6. **Przydział modeli jest konfiguracją.** Nic nie zaszywamy w kodzie; koszt i jakość są
   decyzją operatora.

## 5. Ryzyka i sposoby ich ograniczenia

| ryzyko | przeciwdziałanie | odpowiedzialny |
|---|---|---|
| Biblioteka zapełnia się regułami bez wartości | Dwa poziomy (`observations` i `idioms`), awans wyłącznie decyzją kuratora, wymóg falsyfikowalności | kurator |
| Zarażenie licencją ShareAlike | Hook blokujący, analiza poza drzewem, wynik wyłącznie jako własna proza | inżynier |
| Narzędzia deweloperskie trafiają do paczki | Rozdział katalogów plus test importów | inżynier |
| Koszt tokenów przy analizie 190 MB kodu | Subagenci zapisujący do plików; do rozmowy głównej wraca strona ustaleń | autor promptów |
| Pętla kosmetycznych poprawek renderu | Sufit prób, limit czasu na blok, rozdzielenie błędów technicznych od intencjonalnych | inżynier |
| Tor A produkuje reguły, których nie ma jak sprawdzić | Wczesny poligon w torze B | oba tory |

## 6. Najbliższe trzy kroki

1. Inicjalizacja repozytorium produktu i przeniesienie dokumentacji projektowej.
2. Hook `no_3b1b_code.py` — powstaje **przed** pierwszym pobraniem materiału referencyjnego.
3. Równolegle: `fetch_reference.py` (tor A) oraz szkielet `package/` z `config.default.yaml`
   (tor B).

## 7. Kwestie do rozstrzygnięcia

1. Nazwa przybija produkt do Manima, a w planie jest Blender. Zmiana nazwy albo osobne
   opakowanie nad wspólnym rdzeniem — decyzja przed publikacją.
2. Limit liczby idiomów rdzeniowych. Limit ma istnieć; wartość do ustalenia po pierwszej
   kuracji.
3. Licencja produktu. Rekomendacja: CC BY-NC-SA 4.0 dla materiałów, osobna licencja dla kodu.
4. Gdzie docelowo mieszka repozytorium produktu i kto ma do niego dostęp.

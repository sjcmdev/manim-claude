Analizujesz kod źródłowy jednego materiału wideo pod kątem KONSTRUKCJI SCENY.

Dostajesz jeden katalog tematyczny z repozytorium `3b1b/videos`. Katalog odpowiada
jednemu filmowi lub jednej serii. Pracujesz wyłącznie w trybie do odczytu.

## Tryb pracy

Pracujesz nieinteraktywnie: nikt nie odpowie na pytanie, a odpowiedź trafia prosto
do pliku. Nie proś o wskazanie pliku, nie zadawaj pytań doprecyzowujących, nie
zapowiadaj, co zamierzasz zrobić.

Materiały nie są wklejone w prompcie — otwórz je sam. Przeczytaj wszystkie pliki
źródłowe w podanym katalogu, łącznie z podkatalogami i plikami innymi niż `.py`
(shadery, dane). Analizujesz katalog jako całość, nie pojedynczy plik. Jeśli katalog
jest zbyt duży, żeby przeczytać go w całości, próbkuj największe pliki i pracuj na
tym, co masz — nie pytaj o zgodę.

Pierwszym znakiem odpowiedzi jest `observations:`.

## Czego NIE robisz

- Nie opisujesz API Manima ani ManimGL. To, że `Transform` przekształca obiekt,
  a `VGroup` grupuje, jest znane. Reguła streszczająca dokumentację biblioteki
  jest bezwartościowa.
- Nie streszczasz treści matematycznej ani fizycznej filmu.
- Nie oceniasz, czy kod jest ładny.
- **Nie cytujesz kodu źródłowego.** Repozytorium jest na licencji CC BY-NC-SA 4.0,
  a klauzula ShareAlike zaraziłaby projekt docelowy. Dowodem jest wskazanie
  `plik:linia`, nigdy przeklejony fragment. Nazwa własnej klasy lub metody autora
  może paść jako identyfikator, ale bez jej ciała.

## Czego szukasz

Powtarzalnych decyzji konstrukcyjnych, które da się przenieść na inny film:

- **Dekompozycja**: jak film dzieli się na klasy `Scene`, po czym przebiega granica
  między scenami, co ląduje w jednym pliku, a co w osobnym.
- **Stan i updatery**: co jest animowane przez `updater`, a co przez jawną animację;
  jak trzymany jest stan między ujęciami; kiedy autor sięga po `ValueTracker`.
- **Ponowne użycie**: co trafia do `helpers.py` lub `objects.py`, a co zostaje lokalne;
  co jest parametryzowane, a co skopiowane.
- **Budowa kadru**: jak ustalane są pozycje — współrzędne wpisane ręcznie kontra
  `.next_to()`, `.arrange()`, `.to_edge()`; jak budowana jest hierarchia obiektów.
- **Sterowanie czasem**: skąd biorą się czasy trwania animacji, czy są wpisane
  na sztywno, czy wynikają ze wspólnych stałych.
- **Dane a obraz**: jak wynik obliczenia numerycznego wchodzi do sceny; co jest
  liczone w trakcie renderu, a co wczytywane z pliku.
- **Anty-wzorce**: rzeczy, które autor robi mimo że sam ich odradza, albo które
  wyraźnie są pozostałością po wcześniejszej wersji.

## Zasady odpowiedzi

1. Zwróć WYŁĄCZNIE YAML w schemacie poniżej, bez komentarza przed ani po.
2. Każda reguła musi być FALSYFIKOWALNA: da się spojrzeć na cudzy plik sceny
   i orzec, czy reguła jest złamana, czy nie. „Kod jest dobrze zorganizowany"
   odpada. „Nie wpisuj współrzędnych liczbowo, gdy wystarczy `.next_to()`" zostaje.
3. Reguł niesprawdzalnych nie zgłaszaj wcale.
4. Każda reguła potrzebuje co najmniej jednego dowodu w postaci `plik:linia`.
   Reguła bez dowodu jest wrażeniem, nie obserwacją.
5. Jedna obserwacja = jedna reguła.
6. Lepiej dziesięć obserwacji z twardym dowodem niż czterdzieści ogólników.
7. Jeśli wzorzec występuje w kilku plikach katalogu, podaj kilka dowodów — liczba
   niezależnych wystąpień jest sygnałem dla kuratora.

```yaml
observations:
  - id: <krótki-slug>
    topic: dekompozycja | stan-i-updatery | ponowne-uzycie | kompozycja | czas-i-tempo | dane-a-obraz | anty-wzorce
    rule: <jedno zdanie w trybie rozkazującym>
    falsifiable: true
    evidence:
      - {source: <katalog tematyczny, np. _2024/holograms>, file: <ścieżka względna>, line: <numer linii>}
    confidence: high | medium | low
    applies_to: <kiedy reguła obowiązuje, jedno zdanie>
```

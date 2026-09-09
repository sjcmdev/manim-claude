Analizujesz zbiór materiałów społeczności Manima: gisty z pojedynczymi technikami,
wyjaśnienia mechanizmów oraz małe biblioteki narzędziowe. To **nie są sceny
produkcyjne** — to przepisy. Każdy rozwiązuje jakiś konkretny problem.

Materiał dotyczy **ManimCE**, nie ManimGL. To jest istotne: nasz projekt celuje
w ManimCE, więc techniki stąd są bezpośrednio stosowalne.

## Tryb pracy

Pracujesz nieinteraktywnie: nikt nie odpowie na pytanie, a odpowiedź trafia prosto
do pliku. Nie proś o wskazanie pliku, nie zadawaj pytań, nie zapowiadaj, co zamierzasz.

Materiały nie są wklejone w prompcie — otwórz je sam. Przeczytaj pliki źródłowe
w podanym katalogu wraz z podkatalogami, w tym pliki `.md` i `_opis.txt`, bo często
to w nich autor tłumaczy, po co dana technika powstała. Jeśli katalog jest zbyt duży,
żeby przeczytać go w całości, próbkuj szeroko — lepiej dotknąć wielu technik płytko
niż kilku głęboko.

Pierwszym znakiem odpowiedzi jest `techniques:`.

## Czego szukasz

Dla każdej techniki interesuje mnie **problem, nie implementacja**:

- **Jaki problem rozwiązuje.** Co jest trudne albo brzydkie, jeśli tej techniki nie znasz.
- **Co zastępuje.** Jak wygląda naiwne podejście, po które sięga ktoś, kto tej
  techniki nie zna. To jest najcenniejsza część — bo to jest przyszły anty-wzorzec.
- **Kiedy po nią sięgnąć.** Warunek uruchamiający, nie ogólnik.

## Czego NIE robisz

- Nie opisujesz API Manima. To, że `ValueTracker` trzyma liczbę, jest znane.
- Nie streszczasz kodu linia po linii.
- **Nie cytujesz ciał funkcji.** Nazwa publicznej klasy, funkcji lub parametru
  może paść jako identyfikator — treść nie. Część materiału jest bez licencji.

## Zwróć szczególną uwagę

Autor projektu nazwał konkretne bolączki. Jeśli którakolwiek technika ich dotyka,
oznacz ją polem `dotyczy_bolaczki`:

- `relacje-wielkosci` — dobieranie `scale`, `font_size`, dopasowań rozmiaru między obiektami
- `buff` — dobieranie odstępów w relacji do skali obiektów
- `pokretla-czasowe` — wystawianie czasu trwania jako parametru
- `szybkosc-vs-dlugosc` — rozdzielenie szybkości ruchu od czasu trwania animacji
- `reset` — powrót do stanu podstawowego tak, żeby wyglądał dobrze
- `przeksztalcanie-wzorow` — kontrolowane animowanie przejść między wzorami
- `przekazywanie-parametrow` — unikanie rozrastających się sygnatur funkcji
- `iteracja-bez-renderu` — skracanie pętli sprawdzania wyniku

## Format odpowiedzi

Zwróć WYŁĄCZNIE YAML w schemacie poniżej, bez komentarza przed ani po.

```yaml
techniques:
  - id: <krótki-slug>
    nazwa: <jak autor to nazywa, jeśli nazywa>
    problem: <co jest trudne bez tej techniki, jedno zdanie>
    zamiast: <naiwne podejście, które ta technika wypiera, jedno zdanie>
    kiedy: <warunek uruchamiający, jedno zdanie>
    dotyczy_bolaczki: <slug z listy powyżej albo null>
    zrodlo: {file: <ścieżka względna>, line: <numer linii>}
    przenosnosc: wysoka | srednia | niska
```

`przenosnosc` oceniaj tym, czy technika jest niezależna od konkretnego przykładu:
wysoka, gdy da się jej użyć w dowolnej scenie; niska, gdy jest zrośnięta z jednym
zagadnieniem.

Lepiej dwadzieścia technik opisanych przez problem, który rozwiązują, niż sto
wpisów streszczających, co robi kod.

Analizujesz kod źródłowy pod kątem SPOSOBU ANIMOWANIA i PROJEKTOWANIA OBIEKTÓW.

To jest druga analiza tego samego materiału. Pierwsza dotyczyła konstrukcji sceny:
podziału na klasy, kolejności faz, budowy kadru. **Tamtej nie powtarzaj.** Tu chodzi
o warstwę niżej — o to, jak zbudowany jest sam ruch i same obiekty.

## Tryb pracy

Pracujesz nieinteraktywnie: nikt nie odpowie na pytanie, a odpowiedź trafia prosto
do pliku. Nie proś o wskazanie pliku, nie zadawaj pytań, nie zapowiadaj, co zamierzasz.

Materiały nie są wklejone w prompcie — otwórz je sam. Przeczytaj wszystkie pliki
źródłowe w podanym katalogu wraz z podkatalogami. Jeśli katalog jest zbyt duży, żeby
przeczytać go w całości, próbkuj największe pliki i pracuj na tym, co masz.

Pierwszym znakiem odpowiedzi jest `observations:`.

## Cztery obszary

**`updatery`** — jak zbudowany jest updater, nie kiedy go użyć. Czy jest funkcją
nazwaną, domknięciem zwracanym z fabryki, metodą obiektu czy lambdą w miejscu
podpięcia. Co updater czyta, a co zapisuje. Jak radzi sobie z `dt` kontra odczytem
trackera. Jak wygląda updater, który musi znać swój stan z poprzedniej klatki.

**`klasy-animacji`** — kiedy autor pisze własną klasę dziedziczącą po `Animation`
zamiast składać gotowe. Co nadpisuje: `interpolate_mobject`, `begin`, `finish`,
`create_starting_mobject`. Jak przekazuje parametry. Jak buduje animacje złożone
z kilku równoległych albo następujących po sobie ruchów. Jak steruje `rate_func`
i po co go zmienia.

**`wejscie-i-sprzatanie`** — jak obiekt pojawia się na scenie i jak z niej znika.
Czym różni się wejście elementu głównego od wejścia adnotacji. Co dzieje się
z obiektem, który przestał być potrzebny: znika, zostaje przygaszony, czy jest
przekształcany w następny. Jak wygląda przejście, po którym scena jest gotowa na
kolejny krok. **Interesuje mnie estetyka tego, a nie samo wywołanie `FadeOut`** —
czyli co autor robi, żeby wejście i wyjście nie wyglądały na przypadkowe.

**`custom-mobject`** — jak zaprojektowana jest własna klasa obiektu. Co ląduje
w `__init__`, a co w metodzie. Jakie metody obiekt wystawia i co one zwracają —
nowy obiekt, siebie samego, czy animację. Jak obiekt trzyma swoje części, żeby dało
się do nich sięgnąć później. Jak parametryzowana jest konstrukcja. Co jest własnością
obiektu, a co narzuca mu scena.

## Zasady odpowiedzi

1. Zwróć WYŁĄCZNIE YAML w schemacie poniżej, bez komentarza przed ani po.
2. Każda reguła musi być FALSYFIKOWALNA: da się spojrzeć na cudzy plik i orzec, czy
   reguła jest złamana. „Pisz czytelne updatery" odpada. „Updater odczytujący tracker
   nie przyjmuje `dt`" zostaje.
3. Nie opisujesz API Manima. To, że `FadeOut` wygasza obiekt, jest znane.
4. **Nie cytujesz kodu.** Dowodem jest `plik:linia`, nigdy przeklejony fragment.
   Nazwa własnej klasy lub metody autora może paść jako identyfikator, bez jej ciała.
5. Jedna obserwacja = jedna reguła.
6. Jeśli wzorzec występuje w kilku plikach, podaj kilka dowodów.
7. Lepiej dziesięć obserwacji z twardym dowodem niż czterdzieści ogólników.

```yaml
observations:
  - id: <krótki-slug>
    topic: updatery | klasy-animacji | wejscie-i-sprzatanie | custom-mobject
    rule: <jedno zdanie w trybie rozkazującym>
    falsifiable: true
    evidence:
      - {source: <katalog, np. _2024/holograms>, file: <ścieżka względna>, line: <numer linii>}
    confidence: high | medium | low
    applies_to: <kiedy reguła obowiązuje, jedno zdanie>
```

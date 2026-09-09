Analizujesz jeden film edukacyjny pod kątem WZORCÓW PROJEKTOWANIA ANIMACJI.

Materiały, które dostajesz: metryczka filmu z linkiem, siatki klatek (każda klatka ma
numer i znacznik czasu w indeksie poniżej) oraz transkrypcja z czasami. Jeśli
potrzebujesz obejrzeć konkretny moment, wejdź na link i przewiń do znacznika.

Nie streszczaj treści. Nie opisuj fizyki ani matematyki. Nie oceniaj, czy film jest
dobry. Interesują mnie wyłącznie powtarzalne decyzje autora dotyczące:

- kompozycji kadru i hierarchii uwagi,
- czasu: tempa, pauz, kolejności pojawiania się elementów,
- czytelności: koloru, kontrastu, rozmiaru, podpisów,
- budowy wyjaśnienia: od czego zaczyna, kiedy wprowadza formalizm.

Zasady odpowiedzi:

1. Zwróć WYŁĄCZNIE YAML w schemacie poniżej, bez komentarza przed ani po.
2. Każda reguła musi być FALSYFIKOWALNA: da się spojrzeć na animację i orzec, czy
   reguła jest złamana, czy nie. „Używaj przemyślanej kompozycji" odpada. „Nie ustawiaj
   współrzędnych ręcznie, gdy istnieje `.next_to()` lub `.arrange()`" zostaje.
3. Reguł niesprawdzalnych nie zgłaszaj wcale, zamiast oznaczać je `falsifiable: false`.
4. Każda reguła potrzebuje co najmniej jednego dowodu: numeru klatki albo znacznika
   czasu z transkrypcji. Reguła bez dowodu jest wrażeniem, nie obserwacją.
5. Jedna obserwacja = jedna reguła. Nie łącz dwóch decyzji w jedno zdanie.
6. Lepiej dziesięć obserwacji z twardym dowodem niż czterdzieści ogólników.

```yaml
observations:
  - id: <krótki-slug>
    topic: kompozycja | czas-i-tempo | czytelnosc | narracja
    rule: <jedno zdanie w trybie rozkazującym>
    falsifiable: true
    evidence:
      - {source: <identyfikator filmu z metryczki>, timestamp: "MM:SS", frame: <numer klatki lub null>}
    confidence: high | medium | low
    applies_to: <kiedy reguła obowiązuje, jedno zdanie>
```

Odpowiedź zapisuję jako `observations.yaml` w katalogu tego filmu, więc nie dodawaj
nagłówka, podsumowania ani pytań na końcu.

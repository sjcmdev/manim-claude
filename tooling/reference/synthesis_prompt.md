Dostajesz surowy zbiór obserwacji o pisaniu animacji w Manimie. Powstał tak: agent
przeczytał po kolei katalogi źródłowe — jeden katalog to jeden film, jedna seria albo
jedna biblioteka — i z każdego wyciągnął reguły w sztywnym schemacie YAML. Każda ma
dowód w postaci `plik:linia`. Dokładny zakres i liczba reguł są podane na końcu tej
instrukcji, razem ze ścieżką do pliku.

Zbiór jest surowy: reguły z różnych źródeł powtarzają się, część jest banalna, część
sprzeczna. Twoim zadaniem jest zamienić go w materiał, który człowiek może przejrzeć
i podjąć decyzję, co awansować do biblioteki idiomów.

## Co masz zrobić

1. **Scal powtórzenia.** Ta sama decyzja projektowa opisana przez kilka źródeł to
   jedna reguła, nie kilka. Liczba niezależnych źródeł, w których wystąpiła, jest
   najważniejszym sygnałem jej siły — podaj ją jawnie przy każdej scalonej regule.
2. **Pogrupuj tematycznie.** Użyj kategorii, które faktycznie wynikają z materiału,
   nie tych z pola `topic` — pole `topic` było zgadywane osobno przy każdym źródle
   i bywa niespójne.
3. **Uszereguj wewnątrz grup.** Na górze reguły potwierdzone w wielu niezależnych
   źródłach i przenośne na inny film. Niżej takie, które widziano raz.
4. **Odsiej banał.** Reguła, która tylko powtarza, co robi funkcja biblioteki
   („`VGroup` grupuje obiekty"), jest bezwartościowa. Wyrzuć ją i policz, ile takich
   było — sama liczba jest informacją o jakości zbioru.
5. **Wskaż sprzeczności.** Jeśli dwa źródła zalecają przeciwne rzeczy, wypisz obie
   strony razem z dowodami. Nie rozstrzygaj — sprzeczność jest tu wynikiem, nie błędem.
6. **Wskaż dziury.** Napisz, o czym ten zbiór milczy, mimo że powinien mieć coś
   do powiedzenia. Interesuje mnie zwłaszcza to, czego z samego kodu wyczytać się nie da.

## Format odpowiedzi

Czytelny markdown po polsku. Nagłówek na grupę tematyczną, wewnątrz lista reguł.
Przy każdej regule:

- treść reguły jednym zdaniem w trybie rozkazującym,
- liczba niezależnych źródeł i ich nazwy,
- jeden reprezentatywny dowód `plik:linia`,
- jedno zdanie o tym, kiedy reguła obowiązuje.

Na końcu trzy osobne sekcje: **Sprzeczności**, **Odsiane jako banał** (sama liczba
plus kilka przykładów), **Czego brakuje**.

Nie streszczaj tego promptu. Nie pisz wstępu o tym, co zaraz zrobisz. Zacznij od
pierwszego nagłówka.

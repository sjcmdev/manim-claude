# Analiza konstrukcji dobrze poprowadzonych filmów (lokalnie, GPU)

**Status:** pomysł, 2026-09-14. Nie wiąże.

## Pomysł

Korpus obserwacji pochodzi dziś wyłącznie z kodu. Nie wiemy, jak zbudowane są filmy,
które działają: jak otwierają problem, gdzie stawiają pytanie, ile trwa ujęcie, kiedy
obraz wyprzedza słowo. Autorzy dostarczają zestaw filmów uznanych za dobrze poprowadzone
(nie tylko 3b1b), a lokalny pipeline na GPU zamienia każdy w mierzalny opis konstrukcji.

Zmiana względem `design-spec.md` 9.3–9.4: zamiast ręcznego przenoszenia pakietu do
zewnętrznego czatu — automatyczna, powtarzalna analiza na własnej maszynie, z manifestem
przebiegu jak w korpusie kodu.

## Wejście

- Filmy wskazane przez autorów, z listą w repozytorium (tytuł, źródło, licencja, powód
  wyboru). Same pliki wyłącznie w katalogu roboczym poza repozytorium.
- Do repozytorium trafiają tylko pomiary i obserwacje, nigdy klatki, audio ani transkrypcja
  w całości.

## Warstwy przetwarzania

| krok | narzędzie (kandydat do sprawdzenia) | wynik |
|---|---|---|
| cięcia i ujęcia | ffmpeg scene detect / PySceneDetect; różnica pikseli jak `verify --shots` | granice ujęć, stany wizualne, czasy trwania |
| mowa | Whisper (np. `faster-whisper`) na GPU | transkrypcja ze znacznikami słów |
| tekst na ekranie | OCR (np. PaddleOCR) | kiedy pojawia się wzór lub napis |
| opis klatki | lokalny model wizyjny (VLM) | co jest w kadrze, co się zmienia |
| struktura | model językowy na złożonym opisie | ruchy wyjaśnienia: pytanie, intuicja, formalizm, przykład, sprawdzenie |

## Mierniki

- tempo: słowa na minutę, długość ujęć, udział pauz wizualnych (obraz bez mowy);
- struktura: czas do postawienia pytania, liczba i rozkład ruchów wyjaśnienia;
- sprzężenie: opóźnienie między wypowiedzeniem pojęcia a jego pojawieniem się w kadrze;
- gęstość: liczba nowych obiektów na ujęcie, czas życia obiektu na ekranie.

## Wynik

YAML obserwacji z dowodem w postaci znacznika czasu (`video`, `t_start`, `t_end`),
walidowany tym samym walidatorem co korpus kodu (rodzaj: obserwacje animacji), z manifestem
`generated`. Reguły mają być falsyfikowalne: da się wskazać fragment, który je łamie.

## Pytania na spotkanie

1. Jaki GPU i ile VRAM? Od tego zależy wybór VLM (7B mieści się w ~16 GB, większe nie).
2. Kto dostarcza filmy i według jakiego kryterium „dobrze poprowadzony”?
3. Licencje: filmy spoza CC — czy wystarczy zasada „tylko pomiary w repozytorium”?
4. Pilotaż: 3 filmy, jeden miernik end-to-end (np. opóźnienie słowo–obraz), zanim
   powstanie cały pipeline.
5. Czy to zadanie toru A (nowy miner), czy osobny tor?

## Ryzyka

- VLM halucynuje opis kadru — dowodem musi być znacznik czasu do ręcznej weryfikacji.
- Mierniki bez punktu odniesienia nic nie mówią: potrzebny zestaw kontrolny filmów słabych.
- Koszt czasowy przetwarzania długich filmów na jednej karcie.

# Licencja treści: CC BY-NC-SA 4.0

Ta licencja obejmuje treść tego repozytorium, która nie jest kodem: dokumentację
projektową, materiały badawcze oraz korpus obserwacji, w tym:

- pliki `*.md` w korzeniu repozytorium (`README.md`, `vision.md`, `roadmap.md`,
  `design-spec.md`, `decision-log.md`, `TODO.md`) i w `docs/`;
- `research/` — analizy poboczne i rozpoznanie terenu;
- `observations/` — korpus obserwacji wydobytych z cudzego kodu, syntezy i
  manifesty pochodzenia;
- `idioms/` — przyszła biblioteka idiomów, gdy powstanie.

Pełny tekst licencji: <https://creativecommons.org/licenses/by-nc-sa/4.0/>.

Skrót warunków: wolno kopiować i przetwarzać pod warunkiem podania autorstwa
(BY), wyłącznie w celach niekomercyjnych (NC), a utwory pochodne muszą być
udostępnione na tej samej licencji (SA).

## Granica wobec licencji kodu

`LICENSE` (MIT) obejmuje kod: skrypty w `tooling/`, przyszły `package/` oraz
testy w `tests/`. Ta licencja (`LICENSE-CONTENT.md`, CC BY-NC-SA 4.0) obejmuje
wszystko, co nie jest kodem uruchamialnym — treść wypisaną wyżej. Plik, który
miesza oba rodzaje treści (np. skrypt z obszernym komentarzem opisowym), jest
objęty licencją kodu; sama treść merytoryczna cytowana w dokumentacji podlega
tej licencji.

## Prawa materiałów źródłowych

Dane i materiały pochodzące ze źródeł zewnętrznych zachowują prawa swoich
właścicieli. W szczególności korpus w `observations/` powstał przez analizę
kodu i filmów 3b1b (CC BY-NC-SA 4.0, materiał nie leży w tym repozytorium —
patrz `tooling/reference/common.py`) oraz bibliotek społecznościowych
wymienionych w `observations/README.md`. Licencja tego repozytorium obejmuje
wyłącznie oryginalny dobór, opis i opracowanie wykonane tutaj: sformułowanie
reguł, ich klasyfikację i syntezy porównawcze. Nie przenosi ani nie rozszerza
praw do materiału źródłowego, z którego reguły zostały wydobyte.

Tak — i tutaj sytuacja jest nawet ciekawsza niż przy Blenderze, bo **poszczególne elementy problemu są już dość dobrze zbadane**, ale prawie nikt nie składa ich w jeden system służący do odtworzenia **indywidualnego sposobu budowania wyjaśnienia**.

Najważniejszy wniosek po przeglądzie literatury, repozytoriów i tego, co już masz w swoich materiałach, jest taki:

> Nie próbowałbym budować „modelu piszącego jak Paweł”.  
> Budowałbym **model procesu konstruowania wyjaśnienia**: jak powstaje pytanie, intuicja, rozróżnienie, formalizm, przykład, analogia, rachunek, sprawdzenie i dopiero na końcu tekst.

To jest znacznie głębsze niż stylistyczne imitation.

Co więcej, Twój istniejący `styl-pisania.md` jest już bardzo dobrym zalążkiem takiego systemu. Wprost rozdziela **strukturę rozumowania od języka**, identyfikuje motywację przed formalizmem, wprowadzanie nowych konstrukcji jako odpowiedzi na brak poprzednich, jawne rozdzielanie łatwo mylonych pojęć, przykład natychmiast po abstrakcji, powiązania przód–tył, fizyczne zakotwiczenie wzorów i obowiązkowe sprawdzanie wyniku.

Problem polega tylko na tym, że obecnie jest to **ręcznie napisana checklista**, a nie model, który można automatycznie wydobywać z nowych dokumentów, porównywać, uczyć i wykorzystywać przy generacji.

# 1. Najważniejsze rozróżnienie: „styl pisania” to tylko ostatnia warstwa

Typowa próba zrobienia czegoś takiego wyglądałaby:

```text
moje dokumenty
      ↓
embedding / prompt / fine-tuning
      ↓
"pisz w moim stylu"
```

I tego właśnie bym nie robił.

Badania z 2025 pokazują zresztą, że nawet mocne modele nadal mają problem z wiarygodnym odtwarzaniem **implicit personal writing style** na podstawie niewielkiej liczby przykładów. ([aclanthology.org](https://aclanthology.org/2025.findings-emnlp.532/?utm_source=chatgpt.com))

W Twoim przypadku to i tak byłby zły cel, ponieważ najbardziej charakterystyczne nie jest:

```text
długość zdania
częstotliwość "therefore"
użycie średników
liczba równań
```

tylko na przykład:

```text
mam obiekt A
↓
pytam co A rzeczywiście potrafi opisać
↓
znajduję konkretny brak
↓
dopiero wtedy wprowadzam B
↓
natychmiast sprawdzam B na prostym niebanalnym przypadku
↓
oddzielam B od podobnego pojęcia C
↓
tłumaczę sens fizyczny
↓
sprawdzam wynik
↓
pokazuję po co B będzie potrzebne dalej
```

To jest **procedura epistemiczno-pedagogiczna**, nie stylistyka.

Dlatego rozdzieliłbym co najmniej sześć warstw:

| Warstwa | Pytanie |
|---|---|
| **Knowledge structure** | Co trzeba powiedzieć i od czego to zależy? |
| **Epistemic / reasoning policy** | Dlaczego kolejny krok jest uzasadniony? |
| **Pedagogical strategy** | Jak doprowadzić czytelnika od niewiedzy do zrozumienia? |
| **Intuition / analogy model** | Jak zbudować model przedformalny i gdzie przestaje działać? |
| **Discourse / rhetoric** | Jak argument i wyjaśnienie są zorganizowane w tekście? |
| **Surface writing style** | Jak dokładnie realizowane są zdania, słownictwo i składnia? |

Do tego dochodzi jeszcze osobno:

```text
Learner model
```

czyli: **co Ty musisz już rozumieć, aby dany sposób wyjaśnienia był dla Ciebie odpowiedni**.

---

# 2. Część tego problemu już ma bardzo dobre narzędzia

Nie znalazłem jednego projektu robiącego dokładnie to, czego chcesz. Znalazłem natomiast bardzo mocne klocki.

| Projekt / kierunek | Co robi | Jak wykorzystałbym u Ciebie |
|---|---|---|
| **LUAR** | uczy reprezentacji autorstwa/stylu tekstu | validator stylu powierzchniowego, nie generator „myślenia” |
| **Stylometry / faststylometry** | mierzy cechy słownictwa, składni, długości zdań itd. | sprawdzanie, czy finalny tekst nie odjechał stylistycznie |
| **DMRST Parser** | buduje drzewa Rhetorical Structure Theory dokumentu | wydobycie: elaboration, contrast, cause, explanation itd.; działa na poziomie dokumentu i obsługuje wiele języków ([github.com](https://github.com/seq-to-mind/DMRST_Parser?utm_source=chatgpt.com)) |
| **SAM / Scholarly Argumentation Mining** | wykrywa jednostki argumentacyjne oraz relacje między nimi | claim → evidence → justification → conclusion w tekstach naukowych ([github.com](https://github.com/DFKI-NLP/sam?utm_source=chatgpt.com)) |
| **Prerequisite Knowledge Graph** | reprezentuje zależności „A trzeba znać przed B” w materiałach edukacyjnych | automatyczna budowa mapy pojęć i prerequisite graph ([link.springer.com](https://link.springer.com/article/10.1007/s10758-023-09682-6?utm_source=chatgpt.com)) |
| **Tutor Move Taxonomy** | rozkłada tutoring na konkretne ruchy pedagogiczne | gotowa inspiracja do stworzenia Twojego `ExplanationMove` ontology ([researchgate.net](https://www.researchgate.net/publication/401692518_Tutor_Move_Taxonomy_A_Theory-Aligned_Framework_for_Analyzing_Instructional_Moves_in_Tutoring?utm_source=chatgpt.com)) |
| **Intent Matters** | używa 11 precyzyjnych pedagogical intents zamiast kilku ogólnych klas | bardzo mocny argument za drobną taksonomią ruchów zamiast promptu „explain clearly” ([aclanthology.org](https://aclanthology.org/2025.bea-1.63/?utm_source=chatgpt.com)) |
| **Teaching Through Analogies** | source finding → sub-concepts → explanation → evaluation | niemal gotowy model do Twojego `analogy-agent`; oparty na Structure Mapping Theory ([aclanthology.org](https://aclanthology.org/2026.bea-1.59/?utm_source=chatgpt.com)) |
| **MRBench / tutor evaluation taxonomy** | ocenia tutorów w ośmiu wymiarach pedagogicznych | baza do QA generowanego wyjaśnienia ([scale.stanford.edu](https://scale.stanford.edu/ai/repository/unifying-ai-tutor-evaluation-evaluation-taxonomy-pedagogical-ability-assessment-llm?utm_source=chatgpt.com)) |

Szczególnie interesujący jest **Tutor Move Taxonomy** z 2026. Autorzy robią dokładnie to, co sugerowałbym Tobie: zamiast traktować całą wypowiedź nauczyciela jako monolit, rozkładają ją na **dyskretne działania dydaktyczne**. Następnie można badać nie tylko występowanie poszczególnych ruchów, ale też ich sekwencje. ([researchgate.net](https://www.researchgate.net/publication/401692518_Tutor_Move_Taxonomy_A_Theory-Aligned_Framework_for_Analyzing_Instructional_Moves_in_Tutoring?utm_source=chatgpt.com))

To jest bezpośredni odpowiednik naszego:

```text
Visual Explanation Pattern Atlas
```

dla 3b1b.

Tutaj mielibyśmy:

```text
Pedagogical Explanation Pattern Atlas
```

---

# 3. Twój `styl-pisania.md` pokazuje, że właściwie już zacząłeś budować taką ontologię

Spójrz, co właściwie jest tam zapisane.

To nie jest:

```text
prefer long sentences
prefer formal language
use equations
```

tylko rzeczy typu:

```text
MOTIVATE_BEFORE_FORMALIZE

INTRODUCE_AS_SOLUTION_TO_LIMITATION

ANTICIPATE_CONFUSION

CONTRAST_SIMILAR_CONCEPTS

ABSTRACT_TO_MINIMAL_EXAMPLE

INTERPRET_EQUATION_PHYSICALLY

VERIFY_RESULT

BACK_REFERENCE

FORWARD_REFERENCE
```

Twój dokument wprost mówi, że nowy obiekt pojawia się dlatego, że poprzednia konstrukcja czegoś nie potrafi, a dwa łatwo mylone pojęcia mają zostać rozdzielone zanim czytelnik sam je pomyli.

I dokładnie to widać w samym dokumencie o przestrzeni Focka. Zaczynasz od pytania „jak z przestrzeni jednocząstkowej zbudować przestrzeń wielu identycznych kwantów?”, a następnie tensor product pojawia się dopiero wtedy, gdy pokazujesz, że suma dwóch wektorów nadal pozostaje stanem jednocząstkowym i nie przechowuje dwóch niezależnych wpisów.

Czyli można by automatycznie oznaczyć:

```yaml
- move: establish_current_model
  object: H_1

- move: test_model_capability
  question: "Can H_1 describe two quanta?"

- move: expose_limitation
  failed_operation: vector_addition

- move: articulate_missing_capability
  capability:
    retain_two_independent_one_particle_states

- move: introduce_new_structure
  concept: tensor_product

- move: justify_structure
  reason:
    solves_previous_limitation
```

To jest dużo bardziej informacyjne niż embedding całego rozdziału.

---

# 4. Najcenniejsze dane wcale nie znajdują się w Twoich gotowych PDF-ach

To jest chyba największy wniosek z całej analizy.

Gotowy PDF pokazuje:

```text
co ostatecznie zaakceptowałeś
```

ale **nie pokazuje procesu selekcji**.

Natomiast rozmowa typu:

```text
source
  ↓
moja pierwsza próba
  ↓
Twoje:
"nie, tak nie chcę"
"to jest math-slop"
"dlaczego wprowadzasz to teraz?"
"nie potrzebuję tej analogii"
"tu brakuje przejścia"
"najpierw pokaż fizyczny problem"
  ↓
druga wersja
  ↓
Twoja poprawka
  ↓
wersja zaakceptowana
```

jest złotem treningowym.

W zasadzie znacznie cenniejszym niż sto gotowych dokumentów.

Bo masz parę:

```text
rejected explanation
          ↕
accepted explanation
```

przy **tej samej treści merytorycznej**.

To pozwala oddzielić:

```text
CONTENT
```

od:

```text
PEDAGOGICAL CHOICE
```

Tak samo jak przy 3b1b próbujemy oddzielić:

```text
co scena pokazuje
```

od:

```text
jak zostało to zakodowane
```

tutaj możemy oddzielić:

```text
co jest prawdą
```

od:

```text
jak zdecydowałeś, że należy tę prawdę wyjaśnić
```

---

# 5. Dlatego statyczna analiza gotowych dokumentów to dopiero pierwszy etap

Ja bym zebrał cztery klasy corpusów:

```text
A. final documents
   → jak wygląda zaakceptowane wyjaśnienie

B. source → final
   → co zostało wybrane ze źródła, pominięte, przesunięte

C. draft → criticism → revision
   → reguły preferencji i odrzucania

D. learning dialogue
   → gdzie pojawia się niezrozumienie,
     jakie pytanie je ujawnia,
     jaka odpowiedź powoduje "aha"
```

D jest szczególnie ciekawe.

Jeżeli rozmowa wygląda:

```text
explanation 1
↓
"nie rozumiem"
↓
explanation 2
↓
"nie, mylisz dwie rzeczy"
↓
explanation 3
↓
"tak, dokładnie"
```

to mamy bardzo rzadki rodzaj danych:

```text
failed mental model
      ↓
correction
      ↓
successful mental model
```

To powinno wejść do osobnego:

```text
CognitiveRepairAtlas
```

---

# 6. Nie próbowałbym „wyciągać Twojego sposobu myślenia” w sensie dosłownym

Z tekstu nie można wiarygodnie odzyskać czyjegoś prywatnego wewnętrznego toku myśli.

Ale można bardzo dobrze wydobyć coś praktyczniejszego:

> **observable reasoning policy**

czyli regularności typu:

```text
co uznajesz za satysfakcjonujące wyjaśnienie
jak ustanawiasz zależność przyczynową
kiedy definicja jest według Ciebie uzasadniona
jak rozdzielasz dwa podobne pojęcia
kiedy przykład naprawdę coś wyjaśnia
kiedy matematyka staje się konieczna
co wymaga sprawdzenia
co uznajesz za hand-waving
```

I właśnie taki model da się później stosować do nowych tematów.

Nazwałbym to nawet nie:

```text
ThinkingStyle
```

ale raczej:

```text
EpistemicPolicy
```

---

# 7. RST jest bardzo interesujące, ale samo zdecydowanie nie wystarczy

Rhetorical Structure Theory może powiedzieć na przykład:

```text
statement A
    └── ELABORATION → B

statement C
    └── CONTRAST → D

statement E
    └── CAUSE → F
```

DMRST potrafi automatycznie segmentować dokument i budować takie hierarchie. ([github.com](https://github.com/seq-to-mind/DMRST_Parser?utm_source=chatgpt.com))

To pomoże wykryć, że u Ciebie występuje dużo:

```text
problem → explanation
claim → justification
concept → contrast
generalization → example
result → interpretation
```

Ale nie wykryje samo najważniejszej rzeczy:

```text
DLACZEGO autor zdecydował się
na tę relację właśnie w tym miejscu
```

Dlatego RST potraktowałbym jako **jeden feature extractor**, a nie główny model.

---

# 8. Podobnie z argument mining

SAM rozpoznaje jednostki argumentacyjne i relacje pomiędzy nimi w publikacjach naukowych. ([github.com](https://github.com/DFKI-NLP/sam?utm_source=chatgpt.com))

Przykład:

```text
CLAIM:
Symmetric tensor products describe identical bosons.

SUPPORT:
Permutation of formal slots cannot represent
a new physical configuration.

EVIDENCE:
P12 |Psi_S> = |Psi_S>

CONCLUSION:
Physical bosonic states belong to Sym^N(H).
```

To świetne do odtworzenia:

```text
argument graph
```

ale jeszcze nie:

```text
teaching graph
```

Bo pedagogicznie mógłbyś najpierw pokazać błędną konstrukcję, potem konflikt, potem dopiero claim.

---

# 9. Dlatego potrzebujesz własnej ontologii `ExplanationMove`

To byłoby odpowiednikiem Twojego IR dla animacji.

Na przykład:

```yaml
move:
  type: expose_limitation

  current_model:
    concept: single_particle_hilbert_space

  attempted_task:
    describe: two_independent_quanta

  failure:
    reason:
      vector_addition_remains_in_same_space

  learner_state:
    expected_before:
      understands_superposition: true
      understands_tensor_product: false

  purpose:
    create_need_for:
      tensor_product
```

Inny fragment:

```yaml
move:
  type: distinction

  concepts:
    - mode_label
    - occupation_number

  confusion_reason:
    both_are_indices_associated_with_states

  contrast:
    mode_label:
      answers: "which one-particle state?"
    occupation_number:
      answers: "how many quanta?"

  importance:
    later_needed_for:
      fock_space
```

Agent nie musi już „naśladować dokumentu”.

On zna **operację pedagogiczną**.

---

# 10. Intuicja powinna być osobnym obiektem

To jest bardzo ważne dla Twoich materiałów.

Nie definiowałbym intuicji jako:

```text
simple explanation
```

ani:

```text
analogy
```

Intuicja może istnieć bez analogii.

Dobry obiekt `IntuitionModel` mógłby wyglądać tak:

```yaml
intuition:
  target:
    tensor_product

  learner_problem:
    "Why isn't adding two state vectors enough?"

  preformal_model:
    "We need an object with two independent slots."

  operational_prediction:
    learner_should_predict:
      - "changing slot 1 need not change slot 2"
      - "dimensions multiply rather than add"

  invariant_structure:
    - independence_of_entries
    - linearity_in_each_slot

  bridge_to_formalism:
    formal_object:
      H_A tensor H_B

  limits:
    - "slots do not yet mean distinguishable physical particles"
```

To ostatnie pole jest krytyczne.

**Prawdziwa intuicja nie tylko pomaga coś zobaczyć; mówi też, gdzie obraz przestaje być prawdziwy.**

---

# 11. Analogia powinna być jeszcze bardziej rygorystyczna

Tutaj trafiłem na bardzo aktualną pracę, która wyjątkowo dobrze pasuje do Twojego projektu.

Barakat i Kochmar w BEA 2026 proponują modularny pipeline:

```text
source finding
     ↓
sub-concept generation
     ↓
analogy explanation
     ↓
evaluation
```

oparty na **Structure Mapping Theory**. Co ciekawe, pokazują, że zakotwiczenie analogii w sub-concepts poprawia retrieval oraz jakość wyjaśnienia. ([aclanthology.org](https://aclanthology.org/2026.bea-1.59/?utm_source=chatgpt.com))

Czyli agent nie powinien generować:

> „przestrzeń Hilberta jest trochę jak pudełko”

bo brzmi intuicyjnie.

Powinien najpierw ustalić:

```text
target relation:
linear functional maps a vector to a scalar

needed structural feature:
an object acts on another object
and returns one number
```

dopiero potem szukać domeny źródłowej.

Ja zapisywałbym analogię tak:

```yaml
analogy:
  target:
    concept: covector

  source:
    concept: measurement_instrument

  mappings:
    - source: instrument
      target: covector
    - source: object_being_measured
      target: vector
    - source: measurement_result
      target: scalar

  preserved_relations:
    - "instrument acts on object"
    - "result is one number"

  non_correspondences:
    - "a covector is not a physical apparatus"
    - "linearity has no automatic analogue in every measurement"

  pedagogical_goal:
    distinguish:
      - vector
      - dual_vector

  exit_condition:
    "Once linearity and basis transformation are introduced,
     stop relying on the instrument analogy."
```

To zmienia jakość analogii radykalnie.

---

# 12. Możesz z tego zrobić `Pedagogy Pattern Atlas`

Tak samo jak wcześniej:

```text
Visual Explanation Pattern Atlas
```

mógłbyś mieć:

```text
Pedagogy Pattern Atlas
```

Na przykład:

```yaml
pattern:
  id: construction_from_failure

  trigger:
    learner_knows: A
    next_concept: B
    relation:
      B_solves_limit_of_A

  sequence:
    - remind_capabilities_of_A
    - pose_new_task
    - attempt_with_A
    - expose_failure
    - state_missing_capability
    - introduce_B
    - show_B_solves_failure
    - test_small_case
    - preview_next_limitation

  examples:
    - tensor_product
    - fock_space
    - creation_operator

  anti_patterns:
    - define_B_without_problem
    - give_general_definition_before_need_is_visible
```

Po pewnym czasie możesz odkrywać takie wzorce automatycznie.

I wtedy model nie dostaje:

> „write like my previous chapter”

tylko:

```text
Problem has form:
old representation cannot encode independent degrees of freedom

Matched pattern:
construction_from_failure

Examples:
tensor product chapter
dual-space chapter
NV SALC chapter
```

To jest retrieval na poziomie **struktury wyjaśnienia**, a nie podobieństwa tematycznego.

---

# 13. Sposób uczenia wymaga jeszcze innego datasetu

Tutaj dokumenty są wręcz niewystarczające.

Do odtworzenia sposobu uczenia potrzebujesz przede wszystkim historii interakcji.

Nie klasyfikowałbym Cię jako:

```text
visual learner
kinesthetic learner
auditory learner
```

To jest zbyt prymitywny model i niewiele daje systemowi.

Modelowałbym konkretne zachowania:

```yaml
learning_profile:
  abstraction:
    tolerance: high
    requirement:
      must_be_motivated: true

  formalism:
    wants_derivation: true
    accepts_definition_without_need: false

  intuition:
    required_before_symbolic_compression: true
    trivial_analogies:
      preference: avoid

  confusion_resolution:
    preferred:
      - distinguish_objects
      - identify_what_each_object_does
      - reconstruct_dependency_chain

  examples:
    preferred:
      complexity: minimal_nontrivial
      purpose:
        - expose_structure
        - verify_general_rule

  verification:
    preferred:
      - substitute_back
      - check_dimension
      - limiting_case
      - count_degrees_of_freedom
```

I aktualizował ten profil na podstawie realnych interakcji.

---

# 14. Szczególnie wartościowe są miejsca, w których zadajesz drugie i trzecie pytanie

Pierwsze pytanie mówi:

```text
czego nie wiem
```

Drugie często mówi:

```text
czego nie zrozumiałem w pierwszym wyjaśnieniu
```

Trzecie:

```text
jaki model próbuję sobie zbudować
```

To pozwala wydobyć coś znacznie ciekawszego niż „preferred answer length”.

Na przykład sekwencja pytań może pokazać:

```text
term confusion
      ↓
object identity confusion
      ↓
relation confusion
      ↓
hierarchy confusion
```

i agent z czasem zacznie przewidywać:

> „Po tym zdaniu prawdopodobnie pojawi się pytanie, czy dual vector jest obiektem czy mappingiem; wyjaśnij tę różnicę zanim przejdziesz dalej.”

To byłby **predictive misconception model**.

---

# 15. Możesz też statycznie analizować Twoje poprawki

Przykład:

```diff
- Let V* be the dual vector space...
+ Before defining V*, ask what kind of object can take
+ a vector from V and return a scalar.
```

Extractor powinien opisać nie słowa, ale transformację:

```yaml
revision:
  removed:
    move: premature_definition

  added:
    move: motivating_question

  inferred_preference:
    formalism_requires_prior_need: true

  confidence:
    high
```

Po setkach takich poprawek masz już preference dataset.

To według mnie będzie **znacznie lepsze niż fine-tuning na gotowych tekstach**.

---

# 16. Dopiero ostatnia warstwa to styl lingwistyczny

Tutaj można używać normalnej stylometrii.

Badania mierzą m.in. długości słów i zdań, lexical diversity, częstości, entropy, funkcje gramatyczne czy wzorce słownikowe. ([academic.oup.com](https://academic.oup.com/dsh/article/40/2/587/8118784?utm_source=chatgpt.com))

LUAR z kolei jest modelem uczącym się reprezentacji autorstwa.

Takich narzędzi użyłbym jako:

```text
STYLE CRITIC
```

czyli:

```text
generated document
       ↓
stylometric features
       ↓
authorship/style embedding
       ↓
distance from reference corpus
```

Nie pozwalałbym im decydować o toku wykładu.

---

# 17. Cały system widzę tak

```text
                SOURCE CORPUS
        ┌────────────┼────────────┐
        ↓            ↓            ↓
      papers       books        lectures
        ↓            ↓            ↓
        └──────── KNOWLEDGE ───────┘
                    GRAPH
                      ↓
             concept dependencies
             claims / evidence
             assumptions
             definitions
             equations
                      ↓
       ┌──────── PEDAGOGY ANALYSIS ───────┐
       │                                  │
       ↓                                  ↓
  Explanation Moves                 Learner Model
       ↓                                  ↓
  Pattern Atlas                     confusion history
       ↓                                  ↓
       └─────────── PLANNER ──────────────┘
                       ↓
                ExplanationSpec
                       ↓
          ┌────────────┼─────────────┐
          ↓            ↓             ↓
      prose/PDF     animation      slides
          ↓            ↓             ↓
          └────────────┼─────────────┘
                       ↓
                    critics
         ┌─────────────┼─────────────┐
         ↓             ↓             ↓
      science       pedagogy       style
      critic         critic        critic
```

To bardzo dobrze skleja się z poprzednim systemem Manim + Blender.

---

# 18. Wspólny IR mógłby zaczynać się jeszcze przed animacją

Poprzednio mieliśmy:

```text
AnimationSpec
```

Teraz dodałbym poziom wyżej:

```text
ExplanationSpec
```

Przykład:

```yaml
explanation:
  topic: tensor_product

  target_knowledge:
    learner_should_understand:
      - why direct addition is insufficient
      - what information tensor slots retain
      - why dimensions multiply

  prerequisites:
    - vector_space
    - linear_combination
    - basis

  misconceptions:
    - id: tensor_product_vs_vector_product
    - id: tensor_slots_vs_physical_particle_labels

  conceptual_arc:
    - current_model
    - new_problem
    - failed_attempt
    - missing_capability
    - new_construction
    - minimal_example
    - physical_interpretation
    - verification

  intuition:
    model: independent_slots
    validity:
      until: identical_particle_symmetry

  formalism:
    introduce_after:
      - need_for_two_independent_entries

  checks:
    - dimensional_counting

  style_profile:
    ref: pawel-v3
```

A dopiero później:

```text
ExplanationSpec
       ↓
VisualDirector
       ↓
AnimationSpec
       ↓
Manim / Blender
```

---

# 19. Powstaje więc bardzo elegancki cały pipeline

```text
SOURCE
  ↓
Knowledge Graph
  ↓
Explanation Planner
  ↓
Pedagogical Pattern Atlas
  ↓
ExplanationSpec
  ↓
Narration
  ↓
Visual Explanation Planner
  ↓
AnimationSpec
  ↓
Manim / Blender
  ↓
video / slides / PDF
```

I wtedy wszystkie produkty mają dokładnie ten sam **rdzeń epistemiczny**.

Nie może już wystąpić sytuacja:

```text
PDF tłumaczy A → B → C
film tłumaczy A → C
slajdy pokazują C → B
```

bo wszystkie są kompilowane z tego samego drzewa.

---

# 20. Fine-tuning zostawiłbym zdecydowanie na później

Najpierw:

```text
explicit ontology
+
structured extraction
+
pattern retrieval
+
few-shot exemplars
+
critics
```

Dopiero potem fine-tuning.

To tym bardziej ma sens, że wyniki badań nad imitacją stylu nie są takie, aby można było powiedzieć „daj trzy teksty i problem rozwiązany”. Duże badanie EMNLP 2025 pokazuje istotne problemy z imitowaniem subtelnego stylu indywidualnych autorów z niewielu przykładów. ([aclanthology.org](https://aclanthology.org/2025.findings-emnlp.532/?utm_source=chatgpt.com))

Z drugiej strony istnieją techniki tworzenia osobnych reprezentacji stylu i nawet kontrolowania intensywności cech stylistycznych, co pokazuje, że **styl dobrze jest traktować jako osobny wymiar**, a nie mieszać go z treścią. ([aclanthology.org](https://aclanthology.org/2025.acl-long.767/?utm_source=chatgpt.com))

U Ciebie rozdzielenie to jest jeszcze ważniejsze.

---

# 21. Później możesz zrobić preference learning z własnych poprawek

Jeżeli uzbierasz:

```text
prompt/source
+
bad version
+
your criticism
+
accepted version
```

to masz naturalny dataset:

```text
chosen
vs
rejected
```

który nadaje się później do:

```text
DPO / ORPO / reward model / GRPO
```

lub po prostu jako judge.

Można nawet mieć trzy rewardy:

```text
R_science
R_pedagogy
R_style
```

zamiast jednego magicznego:

```text
"does this sound like Paweł?"
```

---

# 22. QA powinno być bardzo mocne

W poprzednim systemie doszliśmy do:

```text
semantic verification
+
visual verification
```

Tutaj analogicznie:

```text
scientific verification
+
pedagogical verification
+
discourse verification
+
style verification
```

Przykładowo pedagogical critic sprawdza:

```yaml
checks:
  - every_new_concept_has_motivation
  - no_symbol_before_semantic_role
  - likely_confusions_are_explicitly_separated
  - general_rule_has_nontrivial_example
  - every_major_equation_has_interpretation
  - assumptions_are_named
  - calculation_has_consistency_check
  - analogy_has_limit_statement
```

To już niemal bezpośrednio wynika z Twojego obecnego `styl-pisania.md`.

---

# 23. Bardzo ciekawy jest też pomysł używania kontrastów

Nie analizowałbym tylko:

```text
Twoje teksty
```

ale:

```text
Twoje teksty
VS
standard textbook
VS
AI-generated explanation
VS
tekst, który sam odrzuciłeś
```

Wtedy model może odkryć cechę:

```text
"motivation before formalism"
```

nie dlatego, że często występuje u Ciebie, tylko dlatego, że:

```text
P(feature | Pawel accepted)
>>
P(feature | generic text)
```

To jest dużo mocniejsze statystycznie.

---

# 24. I właśnie tutaj Twój obecny plik powinien się zmienić

Nie wyrzucałbym `styl-pisania.md`.

Wręcz przeciwnie.

Przekształciłbym go z:

```text
human-readable reference
```

w dwa artefakty:

```text
docs/pedagogy/style-reference.md

schemas/pedagogy-profile.yaml
```

Pierwszy służy Tobie.

Drugi agentom.

Na przykład:

```yaml
profile:
  concept_introduction:
    default:
      problem_before_definition: required
      previous_model_limitation: preferred

  formalism:
    introduce:
      only_after_semantic_need: true
    math_without_interpretation:
      allowed: false

  example:
    timing:
      after_general_rule: immediate
    complexity:
      preferred: minimal_nontrivial

  misconception:
    proactive_contrast: true

  analogy:
    triviality:
      avoid: true
    require_mapping: true
    require_limits: true

  verification:
    required_after_derivation: true

  navigation:
    backward_reference: preferred
    forward_reference: preferred
```

---

# 25. Najbliższy odpowiednik tego, co robicie teraz z 3b1b

Dla 3b1b masz:

```text
video
↕
YAML
↕
code
```

Tutaj zrobiłbym:

```text
final explanation
↕
Pedagogy YAML
↕
source material
```

a dla rozmów:

```text
draft
↓
user critique
↓
revision
```

zamienić na:

```text
pedagogical transformation
```

Czyli finalnie dwa atlasy:

```text
Pedagogical Pattern Atlas
          ↓
Visual Explanation Pattern Atlas
          ↓
Implementation Pattern Atlas
```

To już jest bardzo potężny system.

---

# 26. Wtedy „burza mózgów” z agentem też może działać zupełnie inaczej

Nie:

> „Mam temat spin, zaproponuj film.”

tylko agent najpierw odpowiada wewnętrznie:

```text
Co użytkownik powinien po filmie umieć przewidzieć?

Co jest największym conceptual obstacle?

Jakie wcześniejsze modele mentalne będą przeszkadzać?

Co można najpierw pokazać bez formalizmu?

Gdzie formalizm staje się konieczny?

Jaki przykład jest minimalny, ale nie trywialny?

Czy analogia zachowuje właściwe relacje?

Gdzie analogia się psuje?

Co można zweryfikować rachunkiem?

Które elementy potrzebują wizualizacji?
```

Dopiero potem powstaje scenariusz.

To jest dużo bliższe temu, jak rzeczywiście powstaje dobre naukowe wyjaśnienie.

---

# 27. Co bym zrobił teraz

Tutaj kolejność projektu widzę tak:

| Etap | Co robimy | Wynik |
|---|---|---|
| **0** | formalizujemy istniejący `styl-pisania.md` | `PedagogyProfile v0.1` |
| **1** | analizujemy 3–5 gotowych dokumentów | `explanation_events/*.yaml` |
| **2** | analizujemy RST + argument graph + concept dependencies | trzy niezależne reprezentacje |
| **3** | analizujemy rozmowy draft → correction → accepted | `revision_events.yaml` |
| **4** | tworzymy własną ontologię `ExplanationMove` | `ontology.yaml` |
| **5** | wykrywamy powtarzalne sekwencje | `pedagogy_pattern_atlas/` |
| **6** | osobno budujemy `AnalogySpec` i `IntuitionSpec` | reusable patterns |
| **7** | generujemy ExplanationSpec dla nowego tematu | pierwszy planner |
| **8** | robimy multi-critic QA | science/pedagogy/style |
| **9** | łączymy z Visual Director | ExplanationSpec → AnimationSpec |
| **10** | dopiero po zgromadzeniu danych | LoRA / preference learning |

## Najważniejsza rzecz

Po tej analizie powiedziałbym, że masz właściwie **trzy projekty, które można złożyć w jeden**:

```text
1. Jak wiedza jest zorganizowana?
       Knowledge Model

2. Jak Ty budujesz z niej zrozumienie?
       Pedagogy / Epistemic Model

3. Jak zrozumienie zamieniasz na obraz?
       Visual Explanation Model
```

A potem:

```text
Knowledge
   ↓
Understanding
   ↓
Explanation
   ↓
Visualization
   ↓
Implementation
```

To jest według mnie znacznie ciekawszy system niż „LLM generujący Manima”.

Można go już prawie nazwać:

> **compiler for scientific understanding**

gdzie źródłowym językiem są publikacje, wykłady, PDF-y i dyskusje, pośrednią reprezentacją jest **model pojęciowo-pedagogiczny**, a backendami są tekst, LaTeX, Manim, Blender, slides i film.

I co istotne: `styl-pisania.md`, który już masz, wskazuje, że w przypadku Twojego corpus ten pomysł nie jest hipotetyczny — **da się już wskazać konkretne, powtarzalne operacje pedagogiczne, które można zamienić na strukturę danych**, zamiast pozostawiać je jako luźny prompt „pisz w moim stylu”.

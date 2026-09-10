# Comparison: manim-claude and informant-video

Date: 2026-09-10. Basis: a full read of both repositories, test runs, and a parse of the
whole observation corpus. Companion to [`peer-review-manim-claude.md`](peer-review-manim-claude.md),
which turns the gaps named here into action items.

Reference project: [AdamKrysztopa/informant-video](https://github.com/AdamKrysztopa/informant-video)
(package `informant`). It is a private repository shared with the maintainers of
manim-claude; every link below points at a file on its `main` branch.

## Frame

The two repositories are at different stages and that has to be said first.

- manim-claude: design documents closed, a reference-mining toolchain, a 900-rule
  observation corpus with `file:line` evidence, two blind syntheses, an author grill,
  7 unit tests. No pipeline code yet. Thirteen commits in two days.
- informant-video: a working paper-to-video pipeline, 20 skills, 4 subagents, 8 hooks,
  49 test scripts in five measured lanes, 11 ADRs, 117 registered gates, 34 produced
  projects, about two hundred archived lessons. Sixty-plus commits in three days after a
  history restart.

So "does better" below means better practice, not more code. Where the gap is only
maturity, it is labelled as such. And one thing should be said up front: manim-claude's
corpus has already proved its worth outside its own repository. The idioms it mined were
distilled into [`docs/plans/house-idioms/`](https://github.com/AdamKrysztopa/informant-video/tree/main/docs/plans/house-idioms)
in informant-video, and the first of those rules now run as lint there, with the
`construct` length measurement from the author grill sitting as a threshold in
[`informant.toml`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant.toml).
That is a stronger validation than any synthesis table.

## What manim-claude does better

This section comes first because it is the part informant-video cannot copy in an
afternoon.

- **Knowledge comes from the best practitioner, not only from own defects.** A decade of
  `3b1b/videos` plus three community libraries, mined into 900 rules with `file:line`
  evidence. informant-video learns from what it shipped wrong; its lessons archive is
  long precisely because nobody measured the outside world first.
- **Measurement before rule.** `construct` median stable at 18 to 30 lines over a decade,
  `add_updater` to `always_redraw` at 9.5 to 1. informant-video asserts thresholds and
  ratchets them. It borrowed the first number above rather than measuring its own.
- **Falsifiability as the price of entry.** Every rule must be falsifiable or it is not a
  rule. informant-video's `CLAUDE.md` still mixes measured tables with advice prose.
- **Two blind synthesis passes, agreement counted as signal, contradictions listed and left
  open.** informant-video has no protocol for testing whether an invented rule is in the
  material or in the question.
- **The author grill records rejections with reasons**, including rejected proposals from
  the facilitator. informant-video's lessons record what went wrong, never what was
  proposed and refused.
- **A clear boundary between idiom and narrative choice.** Structural rules go to the
  library, story decisions go to the user. informant-video's skills blend the two.
- **Two independent tracks with a defined meeting point** (`scene-coder` reads `idioms/`).
  informant-video is one long chain; nothing in it can be developed without the rest.
- **A decision log readable in one sitting**, question by question, with a table of
  rejected directions. informant-video's ADRs total 380 KB and supersede each other.
- **Scope discipline.** Physics is the user's truth, no framework over Manim, no installer
  yet. informant-video built derivation, critics, domain packs, brand kits, music and audio
  judging, and now carries 117 gates and a lessons archive to match.
- **Licence thinking done before mining.** Out-of-tree root enforced by a path refusal with
  a test, prompts that forbid quoting, a scan that finds zero code lines in 48 files.
  informant-video has no stated position on incoming material.
- **Cheap loop first as an architectural principle** (blockout on rectangles, precomputed
  simulation, matplotlib proof of concept). informant-video discovers layout problems after
  a full render, through `verify --shots`.
- **A stated primary user who is not the author** (a lecturer with one technical helper),
  and a design that keeps that user editing prose, never YAML. informant-video's user is
  the maintainer.

## What informant-video does better

Each point names the file to read, so the maintainers can lift the mechanism, not the
description.

### 1. Enforcement is real, not promised

- informant-video: every rule that matters has a machine home. Lint runs as a PostToolUse
  hook and in-process before render
  ([`informant/lint.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/lint.py),
  registered in [`informant/control_plane/settings.json`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/control_plane/settings.json)).
  Layout checks are ten named lanes with a rejecting and an accepting control each
  ([`informant/checks.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/checks.py),
  [`tests/test_lane_controls.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/tests/test_lane_controls.py)).
  Gates are registered in [`tests/gates.toml`](https://github.com/AdamKrysztopa/informant-video/blob/main/tests/gates.toml);
  a gate with no row fails the run; the count of uncontrolled gates may only fall.
- manim-claude: the load-bearing legal claim ("enforced by a hook, not goodwill") points at
  a hook that does not exist. The only guards are a path refusal in `common.py` and
  `.gitignore`. The roadmap said the hook must exist before the first download; two mining
  tasks were completed without it.
- Why it matters: manim-claude's whole idea is "rules plus a pipeline that enforces them".
  Today nothing is enforced.

### 2. Knowledge lives where it bites

- informant-video: a rule is a `Rule(slug, pattern, message, lesson)` in lint, a lane in
  checks, a fixed first question in a skill, or a measured table in `CLAUDE.md`. Each
  carries the defect it came from in its `lesson` field. The house-idioms port shows the
  full shape in one place: a rule, its threshold key, a bad fixture, a good fixture, and a
  gate row, all in one diff
  ([`tests/test_idiom_rules.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/tests/test_idiom_rules.py),
  [`tests/fixtures/idioms/`](https://github.com/AdamKrysztopa/informant-video/tree/main/tests/fixtures/idioms)).
- manim-claude: knowledge is 882 parseable YAML rules plus six synthesis documents plus a
  grill transcript. None of it is executable, none is read by an agent, and the path from
  observation to lint rule (task/20) is many tasks away.
- Why it matters: rules that nothing reads do not change output. The corpus is excellent
  raw material; it needs one consumer.

### 3. A learning loop with a routing ladder

- informant-video: `lessons` captures at the moment of the mistake with mandatory Condition
  and Home fields
  ([`LESSONS.md`](https://github.com/AdamKrysztopa/informant-video/blob/main/LESSONS.md),
  [`LESSONS-ARCHIVE.md`](https://github.com/AdamKrysztopa/informant-video/blob/main/LESSONS-ARCHIVE.md)).
  Each lesson is routed by hardness: hook, then build-failing machinery, then engine code,
  then skill, then `CLAUDE.md` last. The archive is a graph;
  [`scripts/lessons.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/scripts/lessons.py)
  detects oscillation, recurrence and dangling edges and injects findings at SessionStart
  ([`session_start_lessons.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/control_plane/hooks/session_start_lessons.py)).
  A Stop hook nags only when the session changed something
  ([`stop_lessons_gate.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/control_plane/hooks/stop_lessons_gate.py)).
- manim-claude: the author grill is a strong capture method, but its outcomes have no home.
  Three grill decisions changed the design (series-level shared library, blockout on
  rectangles, main-animation field in the storyboard) and neither `design-spec.md` nor
  `decision-log.md` was updated. `lessons.yaml` is planned for stage 3.
- Why it matters: without routing, learned rules re-enter as prose and are forgotten.

### 4. Honesty is structural

- informant-video: [`README.md`](https://github.com/AdamKrysztopa/informant-video/blob/main/README.md)
  opens with a "Status, read this first" table of what is not true. ADR headers state
  supersession and what actually shipped
  ([`docs/adr/`](https://github.com/AdamKrysztopa/informant-video/tree/main/docs/adr)).
  Reversals are written next to the decision they reverse. The CI file says in its header
  what has never run.
- manim-claude: README's "what exists / what does not" split is good and honest, and it is
  the best-written README of the two. But the spec still says "status: awaiting approval"
  while vision says design is closed; spec 9.3 says video is not downloaded while the script
  downloads it by default; spec 9.2 says code scope is 2022+ while the corpus is 2016+;
  spec 13 says the repo is not in git. TODO knows about two of these and the spec was left
  wrong.
- Why it matters: manim-claude's docs are its only product so far, and they already drift.

### 5. Tests as evidence, not as ritual

- informant-video: no pytest; every test script exits with a code; the runner reads exit
  codes only, because a test once printed "2 passed" as a literal
  ([`tests/harness.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/tests/harness.py),
  [`tests/run_all.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/tests/run_all.py)).
  Lanes are named by measured requirements (unit, corpus, render, host, paid). `--require`
  turns a skip in a promised lane into a failure. Control artifacts are capped and
  sha256-manifested. CI matrix across Python 3.11 to 3.14
  ([`.github/workflows/ci.yml`](https://github.com/AdamKrysztopa/informant-video/blob/main/.github/workflows/ci.yml)).
- manim-claude: 7 tests over 3 of 6 modules; `mine_code.py` and `fetch_reference.py`
  untested; no `pyproject.toml`, no ruff, no mypy, no CI, no branch protection. The branch
  policy requires green technical gates before merge and those gates do not exist, so the
  policy is unenforceable.

### 6. The control plane is a product, and it is portable

- informant-video: skills, agents, hooks and settings are canonical inside the package
  ([`informant/control_plane/`](https://github.com/AdamKrysztopa/informant-video/tree/main/informant/control_plane))
  and generated into `.claude/`, `.agents/` and `.codex/`. A closed transformation set
  translates between harnesses and a test fails when the set and its documentation
  disagree ([`tests/test_control_plane.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/tests/test_control_plane.py)).
  Agents declare a model tier with a refusal floor (`refuse_below: frontier` in
  [`informant-critic.md`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/control_plane/agents/informant-critic.md)),
  not a model name; [`tests/test_model_tier.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/tests/test_model_tier.py)
  holds the mapping.
- manim-claude: D2 says "Claude Code only", D16 says "models in config, nothing hardcoded".
  The only working tool shells out to the Codex CLI and hardcodes the Windows shim path.
  There is no `.claude/` directory at all. The planned `config.default.yaml` names models
  (`opus`, `sonnet`) directly, which ages within months.

### 7. The picture is measured before it is judged

- informant-video: [`informant/verify.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/verify.py)
  with `--shots` segments a render into holds and transitions by changed-pixel fraction and
  writes one PNG per visual state. Legibility is asserted in scene units per format
  ([`tests/test_typemetrics.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/tests/test_typemetrics.py),
  [`tests/test_safe_area.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/tests/test_safe_area.py)).
  Equation containers were found to report fill opacity 0.0, which made every equation
  invisible to layout checks; that finding became a rule
  ([`tests/test_opacity_and_sidecar.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/tests/test_opacity_and_sidecar.py)).
- manim-claude: `visual-judge` is designed as a model looking at a frame with the plan in
  context. The grill already found the right principle ("thresholds in config, the rule
  asserts an invariant", text height in frame units) but the spec has no mechanical checks
  before the model looks.

### 8. Approval is a flag the machine reads

- informant-video: `script_approved` in the brief is read by the renderer
  ([`informant/brief.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/brief.py)),
  not remembered by the model. Persona and voice are recorded in the same file so a resumed
  session cannot drift.
- manim-claude: three blocking gates are described in prose. The storyboard `state` section
  is the right idea and it is not built.

### 9. Extension seams exist and were tested against a real wheel

- informant-video: `informant.toml` found by walking up; plugin entry-point groups
  ([`tests/test_plugins.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/tests/test_plugins.py));
  brand as a Protocol with no null default ([`tests/test_null_brand.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/tests/test_null_brand.py));
  `_repo_root()` deleted after it resolved to `site-packages` under a real install
  ([`docs/adr/007-extension-seams.md`](https://github.com/AdamKrysztopa/informant-video/blob/main/docs/adr/007-extension-seams.md)).
- manim-claude: the `package/` versus `tooling/` split is a decision with a promised
  import-ban test. Nothing exists.

### 10. Output exists to falsify the rules against

- informant-video: 34 projects, reels shipped weekly, defects traced to specific project
  numbers inside skill text.
- manim-claude: the roadmap itself warns that Track B needs one working block early or
  Track A's rules become wishful thinking. Track B has zero checked items. The grill's rules
  have no example pairs yet, by its own admission.

### 11. Reproducibility of generated knowledge

- informant-video: one run trace per CLI run
  ([`informant/runlog.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/runlog.py)),
  verdicts bound to artifact hashes
  ([`informant/state.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/state.py)),
  controls with manifests.
- manim-claude: no YAML records the model, effort level, prompt hash, date, or clone
  revision that produced it. The copy from the working root into `observations/` was
  manual. One file is invalid YAML and the miner only checks that output starts with
  `observations:`.

## Where informant-video is weaker, briefly

Fairness requires the other side, and manim-claude's maintainers should not copy these.

- Its knowledge is reactive: it learns from its own shipped defects only. The house-idioms
  port is the first time it took rules from outside.
- It carries its own contradictions: reel bottom inset wrong for a week while README stated
  the fix as fact; format counts that disagree between the registry, README and
  `FORMATS.md`; an ADR bans a root `.env` while a skill mandates it. 29 of 117 gates have
  never been shown to reject anything (`uncontrolled_max = 29`). Most of the suite is
  maintainer-only because projects are gitignored.
- It has no stated position on incoming material and no licence firewall. manim-claude
  thought this through first.

## What to take first

1. Build the licence hook and one Track B block before curating a single idiom.
2. Give every observation a run manifest and a parse-validating test.
3. Route grill outcomes into the spec the same day, with a "superseded by" line.
4. Replace model names in config with tiers and a refusal floor.
5. Define the mechanical checks the visual judge runs before the model looks.

Each of these has a worked example in informant-video, linked in the sections above and
turned into checkboxes in [`peer-review-manim-claude.md`](peer-review-manim-claude.md).

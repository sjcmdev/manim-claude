# Peer review: manim-claude

Date: 2026-09-10. Basis: every document, the tooling, the tests, and a parse of the whole
observation corpus. Written for the maintainers as an honest outside review. The
comparison that grounds it is in
[`comparison-with-informant-video.md`](comparison-with-informant-video.md).

Where an item says "see informant-video", the link points at a working implementation of
the same idea in [AdamKrysztopa/informant-video](https://github.com/AdamKrysztopa/informant-video),
a private repository shared with the maintainers. It is offered as a reference, not as a
template: informant-video made its own mistakes on the way and some of them are named in
the comparison document.

## Verdict

The design is coherent, the documents are unusually well argued, and the corpus is a rare
asset. In one week the project produced 900 rules with line-level provenance from a decade
of the best practitioner's code, ran two blind syntheses over them, and confronted the
result with the author's own practice. That is more knowledge work than most animation
tooling ever does, and it has already paid off outside this repository: the rules were
distilled into a lint plan in informant-video and the first of them run there as gates
today. The `construct` length measurement from the grill became a threshold in another
project's config within a day.

The repository is also a set of promises with almost no machinery behind them, and it has
already broken the one rule it called absolute. Nothing below is fatal. All of it compounds
if left another month.

## What is worth protecting

Said first, because the action list is long and should not be read as a verdict on the
ideas.

- The corpus and its no-quoted-code discipline; a scan found zero code lines in 48 files.
- The three miner prompts and the one-script-three-analyses design.
- The blind double synthesis and the comparison documents, including their own warning
  that source counts are not comparable.
- The grill, especially the recorded rejections and the `construct` length measurement.
- The boundary rule: structural and mechanical rules only; narrative choices belong to the
  user.
- "Thresholds in config, the rule asserts the invariant."
- "Separate the expensive loop from the cheap one."
- The decision log's table of rejected directions.
- The README's honest split between what exists and what does not.

## Blocking oversights

- [ ] The licence hook does not exist. `vision.md` and `design-spec.md` say the ShareAlike
      rule "is enforced by a hook, not goodwill". `roadmap.md` says the hook comes before
      the first download. Downloads and two full mining passes happened first. Build
      `no_3b1b_code.py`, test it with a copied line, register it in a Claude Code settings
      file, and only then mine again. See informant-video for the shape of a blocking
      PreToolUse guard with a test:
      [`git_restore_guard.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/control_plane/hooks/git_restore_guard.py)
      and its registration in
      [`settings.json`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/control_plane/settings.json).
- [ ] Track B has zero checked items. The roadmap itself warns that rules with nothing to
      test them on become wishful thinking. Build one block end to end (plan, storyboard,
      one Scene with sections, static frame, section render) before curating a single
      idiom.
- [ ] Technical gates are policy without teeth. `TODO.md` requires lint, types and tests
      before a merge to `dev`; none exist. Add `pyproject.toml`, `ruff`, `mypy`, a test
      runner and a CI workflow now, not in task/10. See informant-video's
      [`pyproject.toml`](https://github.com/AdamKrysztopa/informant-video/blob/main/pyproject.toml)
      and [`ci.yml`](https://github.com/AdamKrysztopa/informant-video/blob/main/.github/workflows/ci.yml)
      for a matrix over Python 3.11 to 3.14 that runs the same lanes the maintainer runs.
- [ ] No `LICENSE` file. A public repository without one is all rights reserved, which
      contradicts the stated non-commercial, share-friendly intent and blocks
      contributors. Pick the licence for code and for materials separately, as the roadmap
      already recommends, and commit both.

## The corpus

Numbers below come from parsing every file under `observations/`.

- [ ] `observations/code/_2022-puzzles.yaml` is invalid YAML (unquoted colon on line 4).
      Eighteen rules are unreachable to any program. The miner only checks that output
      starts with `observations:`; it never parses. Parse and schema-validate in the miner
      and in a test that runs over the committed corpus.
- [ ] `confidence` carries no information: 787 high, 10 medium, 0 low. Either drop the
      field or change the prompt until it produces a spread. Rank by independent source
      count, as the synthesis prompt already does.
- [ ] `falsifiable` is `true` on every one of 882 entries. The field is required for lint
      later, but as produced it is a checkbox. Have the curator re-assess it per rule, and
      make the proof concrete: a rule is falsifiable when it has a breaking scene and a
      passing scene. informant-video holds exactly that pair per idiom rule under
      [`tests/fixtures/idioms/`](https://github.com/AdamKrysztopa/informant-video/tree/main/tests/fixtures/idioms)
      and asserts both directions in
      [`tests/test_idiom_rules.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/tests/test_idiom_rules.py).
- [ ] Topic taxonomy drifts between runs: `updatery` and `stan-i-updatery` coexist;
      `recipes/` uses a different schema entirely. Fix the taxonomy in one file that all
      prompts and the validator read.
- [ ] Thirty-three ids are reused across files. Ids must be unique corpus-wide or carry
      the source prefix.
- [ ] One evidence entry stores `line: 420-422` as a string range where the schema says
      integer. The validator would have caught it.
- [ ] No provenance of the run. No file records the model, effort, prompt hash, date or
      clone revision that produced it. The copy from the working root into `observations/`
      was manual. Add a header block per file and script the copy. See
      [`informant/runlog.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/runlog.py)
      for one trace per run and
      [`informant/state.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/state.py)
      for verdicts bound to artifact hashes.
- [ ] Nobody has verified that `file:line` evidence points at what the rule claims. Sample
      thirty entries by hand and record the hit rate before curation starts.
- [ ] The animation corpus is uniform across its four topics (128, 118, 122, 123). The
      comparison document already suspects a schema artefact. Treat per-topic counts as
      meaningless until a run with an open taxonomy shows otherwise.
- [ ] The video track has produced nothing. Six playlists are listed, packets can be built,
      and no film has been through the external chat. Every "animation" rule so far came
      from code. Run one film and check whether the prompt yields checkable rules.
- [ ] Community sources: the recipe prompt notes that part of the material has no licence.
      Record the licence of `abul4fia`, `mf_tools` and `uwezi` per source in
      `observations/README.md`, and keep unlicensed gists prose-only.
- [ ] Two blind syntheses plus a comparison is the strongest idea in the repository. It
      stops one step short: the comparison lists ten contradictions and no decisions.
      Schedule the author session and record each ruling next to the contradiction.

## Documentation drift

The documents are good and they already disagree with each other and with the code.

- [ ] `design-spec.md` header still says "spec do zatwierdzenia"; `vision.md` says the
      design stage is closed. Pick one.
- [ ] Spec 9.3 says full video is not downloaded; `fetch_reference.py` downloads it by
      default. `TODO.md` knows. Fix the spec, do not park it in TODO.
- [ ] Spec 9.2 limits code mining to 2022 and later; the corpus covers 2016 to 2026.
      `TODO.md` knows. Fix the spec.
- [ ] Spec 13 says the repository is not in git and has no remote. Stale since the first
      commit.
- [ ] Spec 8.3 and 8.4 list agents and hooks as if they exist. Mark each row planned or
      built. informant-video's README does this with a "Status, read this first" table at
      the top ([`README.md`](https://github.com/AdamKrysztopa/informant-video/blob/main/README.md)).
- [ ] Three grill outcomes changed the design and the spec was not touched: a series-level
      shared library in the repository layout, blockout on rectangles as a stage, a
      main-animation field in the storyboard. Every grill ruling needs a home the same day:
      a spec amendment with a "supersedes" line, or a decision-log entry. informant-video
      writes supersession into the ADR header and the reversal next to the decision it
      reverses ([`docs/adr/`](https://github.com/AdamKrysztopa/informant-video/tree/main/docs/adr)).
- [ ] Python 3.14 or newer is required with no reason given anywhere. Manim CE 0.21
      declares 3.11. Either justify the floor or lower it.
- [ ] `README.md` says `pytest tests/`; pytest is not a declared dependency and there is no
      dependency file. The direct-run path works; say which is canonical.
- [ ] Language is mixed with no decision recorded: documents, prompts and rule text in
      Polish, commit subjects in English, `research/` in English. Decide and write it
      down, because the target user is a lecturer and the rule library will be read by an
      agent.
- [ ] `research/` contains raw transcripts with references to private material (a personal
      vault, a private manager repo). The status disclaimer is good. Redact or summarise
      before the repository is shown to anyone outside.

## Design gaps

Things the design does not yet say, found by asking what the first implementer would have
to invent.

- [ ] No definition of an idiom entry. Write the template now: rule, rationale, when it
      applies, a minimal breaking scene, a minimal passing scene, the lint check that
      enforces it, the config key for any threshold. The grill already decided that the
      breaking-and-passing pair is the proof. Make it the price of entry. The plan in
      informant-video's [`docs/plans/house-idioms/`](https://github.com/AdamKrysztopa/informant-video/tree/main/docs/plans/house-idioms)
      is one worked answer, built from this project's own corpus: five rules as lint with
      controls, the rest as one page a skill reads, thresholds under `[idioms]` in
      [`informant.toml`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant.toml).
- [ ] No mechanical checks before the visual judge. The judge is a model looking at a
      frame. Define what a script checks first: objects outside the frame, overlaps,
      minimum text height in frame units, safe margins. The grill found the right principle
      (threshold in config, rule asserts the invariant); the spec does not apply it to the
      judge. See [`informant/checks.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/checks.py)
      for ten named lanes and
      [`informant/verify.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/verify.py)
      for segmenting a render into one frame per visual state before anyone looks.
- [ ] Config names models (`opus`, `sonnet`). Names age within months and mean nothing to
      a second harness. Declare tiers with a refusal floor and map tiers to names in one
      place. See `refuse_below` in
      [`informant-critic.md`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/control_plane/agents/informant-critic.md)
      and the mapping test
      [`tests/test_model_tier.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/tests/test_model_tier.py).
- [ ] D2 says Claude Code only. The only working tool depends on the Codex CLI and
      hardcodes its Windows shim path. Either the decision is wrong or the tooling belongs
      to a dev-only exception that the decision log should record.
- [ ] No Claude Code configuration exists in the repository: no settings, no hooks, no
      skills, no `CLAUDE.md`. For a project whose product is skills, agents and hooks, the
      repository itself should be the first user. informant-video keeps the canonical copy
      inside the package and generates `.claude/` and `.codex/` from it, with a test that
      fails when they diverge
      ([`informant/control_plane/`](https://github.com/AdamKrysztopa/informant-video/tree/main/informant/control_plane),
      [`tests/test_control_plane.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/tests/test_control_plane.py)).
- [ ] Gates are prose. `storyboard.yaml` has a `state` section with a status cycle; say
      which script writes `approved`, and require the renderer to read it. A gate the model
      remembers is not a gate. See `script_approved` in
      [`informant/brief.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/informant/brief.py):
      the renderer refuses when the flag is not literally `true`.
- [ ] Error handling: the spec classifies technical versus intentional errors. It does not
      say who classifies, on what signal, or how a hook distinguishes "could not run" from
      "found a defect". Three exit codes, minimum.
- [ ] The section mechanism is assumed (`--save_sections`, `skip_animations`, section index
      JSON). Nothing has exercised it on Manim CE 0.21. One probe scene would settle it in
      an hour and should exist before task/13.
- [ ] Lessons are scheduled for stage 3, yet the project already produces lessons (the
      grill, the syntheses' gap lists, the TODO's parked contradictions). Start the queue
      now, with a routing rule: hook first, then script, then skill, then prose. See
      [`LESSONS.md`](https://github.com/AdamKrysztopa/informant-video/blob/main/LESSONS.md)
      for the queue format with mandatory Condition and Home fields, and
      [`scripts/lessons.py`](https://github.com/AdamKrysztopa/informant-video/blob/main/scripts/lessons.py)
      for the checks that catch recurrence and oscillation.
- [ ] Every test that matters should be registered. informant-video's
      [`tests/gates.toml`](https://github.com/AdamKrysztopa/informant-video/blob/main/tests/gates.toml)
      requires every gate to name the control that rejects and the control that accepts;
      a gate without a row fails the suite, and the count of uncontrolled gates may only
      fall. This is the cheapest way to make "each rule has a breaking and a passing
      example" (task/20) enforceable rather than aspirational.
- [ ] `tooling/reference/mine_code.py` does not catch `TimeoutExpired`. One hung run
      aborts the pool and loses every remaining status.
- [ ] `--threshold 0.35` for scene-cut detection is a guess and every frame packet rests
      on it. Calibrate on one series and record the value with its reason.
- [ ] The clone of `3b1b/videos` is placed by hand and never pinned. Record the revision
      in the run manifest, or fetch it by script at a fixed commit.
- [ ] Nothing measures the author's own code. The `add_updater` ratio and `construct`
      medians were measured on someone else's decade. Run the same measurements on the
      course repositories to see where the author's practice and the rule disagree.

## Process observations

- Bus factor is one: one author, one machine, no CI, no lockfile, thirteen commits on two
  days. Any claim of "tests pass" is a claim about one laptop.
- The task branch for task/03 still exists on the remote although the policy says task
  branches are deleted after merge. `merge:` is used as a commit type the policy does not
  list. Small, but the policy was written eight days ago.
- The roadmap's ordering was violated once (hook before download) without a note. Record
  the violation in the decision log so the next one is a choice, not a habit.
- Numbers in `README.md` (900 rules) are counted by hand. Have a test count them.

## Suggested order

1. Licence hook, `LICENSE`, `pyproject.toml`, CI. One day.
2. Corpus validator and run manifest; fix the broken file; sample thirty evidences.
3. One Track B block end to end, with a probe of sections on Manim CE 0.21.
4. Idiom entry template; first five idioms with breaking and passing scenes. The
   house-idioms plan in informant-video can be read as a dry run of this step on the same
   material.
5. Spec amendments for every grill ruling and every TODO-parked contradiction.

"""Testy kontraktu korpusu obserwacji i manifestów pochodzenia."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tooling" / "reference"))

import validate_observations as validator  # noqa: E402
from manifest import sha256_file  # noqa: E402


def test_data_hash_ignores_line_endings(tmp_path: Path) -> None:
    lf = tmp_path / "lf.yaml"
    crlf = tmp_path / "crlf.yaml"
    lf.write_bytes(b"observations:\n  - id: a\n")
    crlf.write_bytes(b"observations:\r\n  - id: a\r\n")

    assert sha256_file(lf) == sha256_file(crlf)


OBSERVATION = """\
observations:
  - id: poprawna-regula
    topic: stan-i-updatery
    rule: Steruj stanem przez jeden tracker.
    falsifiable: true
    evidence:
      - {source: _2024/demo, file: scene.py, line: 12}
    confidence: high
    applies_to: Gdy kilka obiektów zależy od tej samej wartości.
"""

RECIPE = """\
techniques:
  - id: poprawna-technika
    nazwa: pomocnik
    problem: Powtarzalna konstrukcja zasłania intencję sceny.
    zamiast: Kopiowanie konstrukcji w każdej scenie.
    kiedy: Gdy konstrukcja pojawia się co najmniej dwa razy.
    dotyczy_bolaczki: ponowne-uzycie
    zrodlo: {file: helper.py, line_start: 4, line_end: 9}
    przenosnosc: wysoka
"""


def write_document(root: Path, kind: str, name: str, text: str) -> Path:
    path = root / kind / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def write_manifest(
    root: Path,
    data_path: Path,
    kind: str,
    *,
    data_sha256: str | None = None,
    data_path_value: str | None = None,
) -> Path:
    relative = data_path.relative_to(root).as_posix()
    payload = {
        "schema_version": 1,
        "data_path": data_path_value or relative,
        "document_type": kind,
        "source_path": None,
        "source_revision": None,
        "prompt_path": None,
        "prompt_sha256": None,
        "model": None,
        "effort": None,
        "generated_at": None,
        "data_sha256": data_sha256 or hashlib.sha256(data_path.read_bytes()).hexdigest(),
        "provenance_status": "legacy-unverified",
    }
    path = root / "manifests" / kind / data_path.with_suffix(".json").name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


@pytest.mark.parametrize(
    ("kind", "name", "text"),
    [
        ("code", "code.yaml", OBSERVATION),
        ("animation", "animation.yaml", OBSERVATION),
        ("recipes", "recipe.yaml", RECIPE),
    ],
)
def test_accepts_each_document_contract(tmp_path: Path, kind: str, name: str, text: str) -> None:
    data_path = write_document(tmp_path, kind, name, text)
    write_manifest(tmp_path, data_path, kind)

    assert validator.validate_corpus(tmp_path) == []


def test_reports_yaml_and_field_errors_with_locations(tmp_path: Path) -> None:
    broken_yaml = write_document(
        tmp_path,
        "code",
        "broken.yaml",
        "observations:\n  - id: zle\n    rule: dwukropek: bez cytowania\n",
    )
    write_manifest(tmp_path, broken_yaml, "code")
    wrong_fields = write_document(
        tmp_path,
        "animation",
        "wrong.yaml",
        """\
observations:
  - id: ""
    topic: updatery
    rule: 7
    falsifiable: tak
    evidence:
      - {source: demo, file: scene.py}
    confidence: pewne
    applies_to: ""
""",
    )
    write_manifest(tmp_path, wrong_fields, "animation")

    errors = validator.validate_corpus(tmp_path)
    rendered = "\n".join(str(error) for error in errors)

    assert "code/broken.yaml: $: niepoprawny YAML" in rendered
    assert "animation/wrong.yaml: observations[0].id" in rendered
    assert "animation/wrong.yaml: observations[0].topic" in rendered
    assert "animation/wrong.yaml: observations[0].rule" in rendered
    assert "animation/wrong.yaml: observations[0].falsifiable" in rendered
    assert "animation/wrong.yaml: observations[0].evidence[0]" in rendered
    assert "animation/wrong.yaml: observations[0].confidence" in rendered
    assert "animation/wrong.yaml: observations[0].applies_to" in rendered


def test_reports_identifiers_duplicated_between_files_and_kinds(tmp_path: Path) -> None:
    first = write_document(tmp_path, "code", "first.yaml", OBSERVATION)
    second = write_document(tmp_path, "animation", "second.yaml", OBSERVATION)
    write_manifest(tmp_path, first, "code")
    write_manifest(tmp_path, second, "animation")

    errors = validator.validate_corpus(tmp_path)

    assert sum("powtórzony identyfikator `poprawna-regula`" in str(e) for e in errors) == 2


def test_reports_missing_and_inconsistent_manifests(tmp_path: Path) -> None:
    missing = write_document(tmp_path, "code", "missing.yaml", OBSERVATION)
    mismatched = write_document(tmp_path, "animation", "mismatch.yaml", OBSERVATION)
    write_manifest(
        tmp_path,
        mismatched,
        "animation",
        data_sha256="0" * 64,
        data_path_value="animation/elsewhere.yaml",
    )

    errors = validator.validate_corpus(tmp_path)
    rendered = "\n".join(str(error) for error in errors)

    assert f"{missing.as_posix()}" not in rendered
    assert "code/missing.yaml: manifest: brak manifestu" in rendered
    assert "manifests/animation/mismatch.json: data_path" in rendered
    assert "manifests/animation/mismatch.json: data_sha256" in rendered


def test_repository_corpus_is_valid() -> None:
    corpus = Path(__file__).resolve().parents[1] / "observations"

    assert validator.validate_corpus(corpus) == []

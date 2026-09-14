"""Testy lokalnego punktu wejścia dla bramek technicznych."""

from __future__ import annotations

import sys
from pathlib import Path

from tooling import check


def python_stage(name: str, code: str, *, required: Path | None = None) -> check.Stage:
    return check.Stage(name, (sys.executable, "-c", code), required)


def test_run_stages_stops_after_first_failure(tmp_path: Path, capsys) -> None:
    log = tmp_path / "stages.txt"
    append_a = f"from pathlib import Path; Path({str(log)!r}).write_text('A')"
    append_b_and_fail = (
        "from pathlib import Path; "
        f"p = Path({str(log)!r}); p.write_text(p.read_text() + 'B'); "
        "raise SystemExit(7)"
    )
    append_c = (
        f"from pathlib import Path; p = Path({str(log)!r}); p.write_text(p.read_text() + 'C')"
    )

    result = check.run_stages(
        [
            python_stage("pierwszy", append_a),
            python_stage("wadliwy", append_b_and_fail),
            python_stage("nieuruchomiony", append_c),
        ],
        cwd=tmp_path,
    )

    assert result == 7
    assert log.read_text() == "AB"
    output = capsys.readouterr().out
    assert "pierwszy" in output
    assert "wadliwy" in output
    assert "kod 7" in output
    assert "nieuruchomiony" not in output


def test_run_stages_reports_missing_optional_script_and_continues(tmp_path: Path, capsys) -> None:
    marker = tmp_path / "ran.txt"
    missing = tmp_path / "missing.py"
    write_marker = f"from pathlib import Path; Path({str(marker)!r}).write_text('ok')"

    result = check.run_stages(
        [
            python_stage("opcjonalny", "raise SystemExit(99)", required=missing),
            python_stage("następny", write_marker),
        ],
        cwd=tmp_path,
    )

    assert result == 0
    assert marker.read_text() == "ok"
    output = capsys.readouterr().out
    assert "POMINIĘTO" in output
    assert str(missing) in output
    assert "następny" in output
    assert "OK" in output


def test_default_stages_have_the_documented_order(tmp_path: Path) -> None:
    stages = check.default_stages(tmp_path, python=sys.executable)

    assert [stage.name for stage in stages] == [
        "formatowanie",
        "lint",
        "typowanie",
        "testy",
        "skan licencyjny",
        "walidacja korpusu",
    ]
    assert stages[0].command == ("ruff", "format", "--check", ".")
    assert stages[1].command == ("ruff", "check", ".")
    assert stages[2].command == ("mypy", ".")
    assert stages[3].command == ("pytest",)
    assert stages[4].command == (
        sys.executable,
        str(tmp_path / "tooling" / "hooks" / "no_3b1b_code.py"),
        "--scan",
    )
    assert stages[5].command == (
        sys.executable,
        str(tmp_path / "tooling" / "reference" / "validate_observations.py"),
    )

"""Testy bezpiecznego publikowania wyników przez miner kodu."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tooling" / "reference"))

import mine_code  # noqa: E402
import validate_observations as validator  # noqa: E402

GENERATED = """\
observations:
  - id: wynik-minera
    topic: dekompozycja
    rule: Dziel scenę według kolejnych faz wyjaśnienia.
    falsifiable: true
    evidence:
      - {source: _2024/demo, file: scene.py, line: 12}
    confidence: high
    applies_to: Gdy scena ma kilka odrębnych etapów.
"""


def mining_paths(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path]:
    clone = tmp_path / "clone"
    topic = clone / "_2024" / "demo"
    topic.mkdir(parents=True)
    prompt = tmp_path / "prompt.md"
    prompt.write_text("Wydobądź reguły.", encoding="utf-8")
    out_dir = tmp_path / "results" / "code"
    manifest_dir = tmp_path / "results" / "manifests" / "code"
    return clone, topic, prompt, out_dir, manifest_dir


def test_miner_publishes_only_a_valid_pair(tmp_path: Path, monkeypatch) -> None:
    clone, topic, prompt, out_dir, manifest_dir = mining_paths(tmp_path)

    def successful_run(cmd, **kwargs):
        if "-o" not in cmd:
            return subprocess.CompletedProcess(cmd, 0, "a" * 40 + "\n", "")
        output = Path(cmd[cmd.index("-o") + 1])
        output.write_text(GENERATED, encoding="utf-8")
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr(mine_code.subprocess, "run", successful_run)

    rel, status = mine_code.mine(
        topic,
        clone,
        out_dir,
        "Wydobądź reguły.",
        ["codex"],
        "high",
        prompt_path=prompt,
        manifest_dir=manifest_dir,
        timeout=10,
    )

    data_path = out_dir / "_2024-demo.yaml"
    manifest_path = manifest_dir / "_2024-demo.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert rel == "_2024/demo"
    assert status.startswith("gotowe")
    assert manifest["provenance_status"] == "generated"
    expected = hashlib.sha256(data_path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    assert manifest["data_sha256"] == expected
    assert manifest["prompt_sha256"] == hashlib.sha256(prompt.read_bytes()).hexdigest()
    assert validator.validate_pair(data_path, manifest_path, "code") == []


def test_miner_rejects_invalid_output_without_partial_files(tmp_path: Path, monkeypatch) -> None:
    clone, topic, prompt, out_dir, manifest_dir = mining_paths(tmp_path)

    def invalid_run(cmd, **kwargs):
        if "-o" not in cmd:
            return subprocess.CompletedProcess(cmd, 0, "a" * 40 + "\n", "")
        output = Path(cmd[cmd.index("-o") + 1])
        output.write_text("To nie jest YAML obserwacji.", encoding="utf-8")
        return subprocess.CompletedProcess(cmd, 0, "", "")

    monkeypatch.setattr(mine_code.subprocess, "run", invalid_run)

    _, status = mine_code.mine(
        topic,
        clone,
        out_dir,
        "Wydobądź reguły.",
        ["codex"],
        "high",
        prompt_path=prompt,
        manifest_dir=manifest_dir,
        timeout=10,
    )

    assert status.startswith("BŁĄD: walidacja")
    assert not (out_dir / "_2024-demo.yaml").exists()
    assert not (manifest_dir / "_2024-demo.json").exists()


def test_timeout_is_isolated_and_leaves_no_partial_files(tmp_path: Path, monkeypatch) -> None:
    clone, topic, prompt, out_dir, manifest_dir = mining_paths(tmp_path)

    def timed_out(cmd, **kwargs):
        output = Path(cmd[cmd.index("-o") + 1])
        output.write_text("częściowy wynik", encoding="utf-8")
        raise subprocess.TimeoutExpired(cmd, kwargs["timeout"])

    monkeypatch.setattr(mine_code.subprocess, "run", timed_out)

    rel, status = mine_code.mine(
        topic,
        clone,
        out_dir,
        "Wydobądź reguły.",
        ["codex"],
        "high",
        prompt_path=prompt,
        manifest_dir=manifest_dir,
        timeout=1,
    )

    assert rel == "_2024/demo"
    assert "BŁĄD: timeout" in status
    assert not (out_dir / "_2024-demo.yaml").exists()
    assert not (manifest_dir / "_2024-demo.json").exists()

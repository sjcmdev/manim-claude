"""Testy hooka ochrony przed kopiowaniem kodu 3b1b (`tooling/hooks/no_3b1b_code.py`).

Fixture'y budują sztuczny „klon" w `tmp_path`, więc testy nie dotykają
prawdziwego katalogu referencyjnego ani sieci. Cztery scenariusze z spec
(„Lokalna ochrona”) plus konfiguracja hooka w `.claude/settings.json`.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tooling" / "hooks"))

import build_fingerprint_index as bfi  # noqa: E402
import no_3b1b_code as hook  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]

# Fragment kodu wystarczająco długi, by dać >=50 znaczących tokenów po
# normalizacji — dokładnie to, co miałby skopiowany fragment 3b1b.
SNIPPET = """\
def compute_layout(items, width, height):
    total = 0
    positions = []
    for index in range(len(items)):
        row = index // width
        col = index % width
        x = col * 2.5 + 1
        y = row * 1.5 - 3
        if x > width or y > height:
            total += 1
        else:
            positions.append((x, y))
    return positions, total
"""


def make_clone(root: Path) -> Path:
    clone = root / "_code" / "videos"
    clone.mkdir(parents=True)
    return clone


def test_no_clone_allows(tmp_path):
    root = tmp_path / "ref"
    payload = {"tool_name": "Write", "tool_input": {"content": SNIPPET}}
    code, reason = hook.evaluate(payload, str(root))
    assert code == 0
    assert reason == ""


def test_clone_without_index_blocks_with_remediation(tmp_path):
    root = tmp_path / "ref"
    make_clone(root)
    payload = {"tool_name": "Write", "tool_input": {"content": SNIPPET}}
    code, reason = hook.evaluate(payload, str(root))
    assert code == 2
    assert "build_fingerprint_index.py" in reason


def test_matching_window_blocks_with_reason(tmp_path):
    root = tmp_path / "ref"
    clone = make_clone(root)
    (clone / "scene.py").write_text(SNIPPET, encoding="utf-8")
    index = bfi.build(clone)
    assert index["token_hashes"], "fixture powinien dać przynajmniej jedno okno"
    (root / hook.INDEX_NAME).write_text(json.dumps(index), encoding="utf-8")

    payload = {"tool_name": "Write", "tool_input": {"content": SNIPPET}}
    code, reason = hook.evaluate(payload, str(root))
    assert code == 2
    assert "podobieństwo" in reason

    # inny, niepodobny tekst nie blokuje
    payload_ok = {"tool_name": "Write", "tool_input": {"content": "x = 1\n"}}
    code_ok, reason_ok = hook.evaluate(payload_ok, str(root))
    assert (code_ok, reason_ok) == (0, "")


def test_forbidden_media_hash_blocks(tmp_path):
    data = b"\x89PNG\r\n\x1a\nfake-binary-payload-not-real-png"
    digest = hashlib.sha256(data).hexdigest()
    violation = hook.check_bytes(
        "stolen.png", data, token_hashes=set(), media_hashes={digest}, window=hook.WINDOW_SIZE
    )
    assert violation is not None
    assert "stolen.png" in violation

    clean = hook.check_bytes(
        "own.png",
        b"different bytes",
        token_hashes=set(),
        media_hashes={digest},
        window=hook.WINDOW_SIZE,
    )
    assert clean is None


def test_internal_error_with_clone_present_blocks(tmp_path):
    root = tmp_path / "ref"
    make_clone(root)
    (root / hook.INDEX_NAME).write_text("{to nie jest json", encoding="utf-8")

    payload = {"tool_name": "Write", "tool_input": {"content": SNIPPET}}
    code, reason = hook.protect(payload, str(root))
    assert code == 2
    assert reason  # jakikolwiek opis błędu — ważne, że nie ciche zezwolenie


def test_non_write_tool_is_ignored(tmp_path):
    root = tmp_path / "ref"
    make_clone(root)  # klon jest, indeksu brak — mimo to Bash nie jest sprawdzany
    payload = {"tool_name": "Bash", "tool_input": {"command": "echo hi"}}
    code, reason = hook.evaluate(payload, str(root))
    assert (code, reason) == (0, "")


def test_settings_json_registers_hook_without_machine_specific_paths():
    settings_path = REPO_ROOT / ".claude" / "settings.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8"))

    pre_tool_use = settings["hooks"]["PreToolUse"]
    matchers = [entry["matcher"] for entry in pre_tool_use]
    assert any("Write" in m and "Edit" in m and "MultiEdit" in m for m in matchers)

    commands = [h["command"] for entry in pre_tool_use for h in entry["hooks"]]
    assert any("no_3b1b_code.py" in c for c in commands)

    raw = settings_path.read_text(encoding="utf-8")
    for forbidden in ("C:\\Users", "/home/", "/Users/", str(Path.home())):
        assert forbidden not in raw, f"ścieżka właściwa jednej maszynie: {forbidden!r}"


if __name__ == "__main__":
    import tempfile

    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            if "tmp_path" in fn.__code__.co_varnames[: fn.__code__.co_argcount]:
                with tempfile.TemporaryDirectory() as td:
                    fn(Path(td))
            else:
                fn()
            print("ok", name)

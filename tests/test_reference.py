"""Samosprawdzenie logiki skryptów referencyjnych. Uruchom `pytest` albo wprost:
`python tests/test_reference.py`. Nie dotyka sieci, ffmpega ani dysku."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tooling" / "reference"))

import common  # noqa: E402
import extract_frames as ef  # noqa: E402
import make_packet as mp  # noqa: E402

SCENES = """\
frame:0    pts:12000   pts_time:0.5
lavfi.scene_score=0.512000
frame:1    pts:96000   pts_time:4
lavfi.scene_score=0.402000
"""

VTT = """\
WEBVTT
Kind: captions
Language: en

00:00:01.000 --> 00:00:03.000
so the determinant

00:00:03.000 --> 00:00:05.000
so the determinant

00:00:05.000 --> 00:01:02.000
<c.colorE5E5E5>tells you</c> how area scales
"""


def test_parse_scene_file():
    assert ef.parse_scene_file(SCENES) == [0.5, 4.0]
    assert ef.parse_scene_file("") == []


def test_thin_keeps_cap_and_spread():
    times = [float(i) for i in range(100)]
    picked = ef.thin(times, 5)
    assert len(picked) == 5
    assert picked[0] == 0.0
    assert picked == sorted(picked)
    assert ef.thin([1.0, 2.0], 5) == [1.0, 2.0]


def test_uniform_stays_inside_the_video():
    picked = ef.uniform(100.0, 4)
    assert len(picked) == 4
    assert 0 < picked[0] < picked[-1] < 100.0
    assert ef.uniform(0.0, 4) == []


def test_parse_vtt_dedupes_and_strips_tags():
    cues = mp.parse_vtt(VTT)
    assert cues == [(1, "so the determinant"), (5, "tells you how area scales")]


def test_hhmmss_crosses_the_hour():
    assert common.hhmmss(62) == "01:02"
    assert common.hhmmss(3723) == "1:02:03"


def test_frame_index_splits_frames_across_sheets():
    index = {
        "cols": 2,
        "rows": 1,
        "source": "scene",
        "sheets": ["sheet_01.jpg", "sheet_02.jpg"],
        "frames": [{"n": i, "t": i, "label": f"00:0{i}"} for i in range(1, 4)],
    }
    text = mp.frame_index(index)
    assert "`sheet_01.jpg` — klatki 1–2" in text
    assert "`sheet_02.jpg` — klatki 3–3" in text


def test_reference_root_refuses_the_repository():
    repo = Path(__file__).resolve().parents[1]
    try:
        common.reference_root(str(repo / "reference"))
    except SystemExit as exc:
        assert "odmowa" in str(exc)
    else:
        raise AssertionError("katalog w repozytorium powinien zostać odrzucony")


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)

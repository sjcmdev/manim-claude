#!/usr/bin/env python3
"""Wyciąga klatki kluczowe z pobranych filmów i skleja je w siatki.

Detekcja cięć przez filtr `scene` ffmpega, a nie próbkowanie co stałą liczbę sekund:
w animacji interesujące są momenty zmiany kadru, nie równy metronom. Gdy film nie ma
wykrywalnych cięć, skrypt schodzi na próbkowanie równomierne, żeby nie zostawić
pustego katalogu.

Trzy limity trzymają objętość materiału w ryzach, bo to on kosztuje w czacie:
liczba klatek na film (`--max-frames`), szerokość klatki (`--width`) i sklejenie
klatek w siatki (`--cols`, `--rows`), dzięki czemu do czatu idzie kilka obrazów
zamiast kilkudziesięciu.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

from common import hhmmss, reference_root, run, video_dirs, video_file

PTS = re.compile(r"pts_time:([0-9.]+)")


def parse_scene_file(text: str) -> list[float]:
    """Znaczniki czasu z wyjścia filtra `metadata=print`."""
    return [float(m.group(1)) for m in PTS.finditer(text)]


def thin(times: list[float], cap: int) -> list[float]:
    """Przycina listę do `cap` pozycji, zachowując równomierne rozłożenie."""
    if cap <= 0 or len(times) <= cap:
        return times
    step = len(times) / cap
    return [times[int(i * step)] for i in range(cap)]


def uniform(duration: float, count: int) -> list[float]:
    """Równomierne próbkowanie z marginesem na czołówkę i tyłówkę."""
    if duration <= 0 or count <= 0:
        return []
    span = duration * 0.96
    start = duration * 0.02
    return [start + span * (i + 0.5) / count for i in range(count)]


def duration(video: Path) -> float:
    out = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nw=1:nk=1",
            str(video),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return float(out.stdout.strip() or 0.0)


def scene_times(video: Path, threshold: float) -> list[float]:
    """Uruchamia detekcję w katalogu filmu: ścieżki w filtrze ffmpega muszą być względne,
    bo dwukropek z 'C:\\' jest w grafie filtrów separatorem."""
    vdir = video.parent
    report = vdir / "scenes.txt"
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            video.name,
            "-vf",
            f"select='gt(scene,{threshold})',metadata=print:file=scenes.txt",
            "-an",
            "-f",
            "null",
            "-",
        ],
        cwd=vdir,
    )
    text = report.read_text(encoding="utf-8", errors="replace")
    report.unlink(missing_ok=True)
    return parse_scene_times_sorted(text)


def parse_scene_times_sorted(text: str) -> list[float]:
    return sorted(set(parse_scene_file(text)))


def extract(video: Path, times: list[float], width: int) -> Path:
    frames = video.parent / "frames"
    frames.mkdir(exist_ok=True)
    for old in frames.glob("f_*.jpg"):
        old.unlink()
    for i, t in enumerate(times, start=1):
        run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-ss",
                f"{t:.3f}",
                "-i",
                video.name,
                "-frames:v",
                "1",
                "-vf",
                f"scale={width}:-2",
                "-q:v",
                "4",
                f"frames/f_{i:04d}.jpg",
            ],
            cwd=video.parent,
        )
    return frames


def tile(vdir: Path, cols: int, rows: int) -> list[str]:
    sheets = vdir / "sheets"
    sheets.mkdir(exist_ok=True)
    for old in sheets.glob("sheet_*.jpg"):
        old.unlink()
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-start_number",
            "1",
            "-i",
            "frames/f_%04d.jpg",
            "-vf",
            f"tile={cols}x{rows}:padding=6:margin=6:color=0x101010",
            "-q:v",
            "4",
            "sheets/sheet_%02d.jpg",
        ],
        cwd=vdir,
    )
    return sorted(p.name for p in sheets.glob("sheet_*.jpg"))


def process(vdir: Path, args: argparse.Namespace) -> None:
    video = video_file(vdir)
    if video is None:
        print(f"pominięte (brak wideo): {vdir}")
        return
    index_path = vdir / "frames" / "index.json"
    if index_path.exists() and not args.force:
        print(f"pominięte (klatki są): {vdir}")
        return

    times = scene_times(video, args.threshold)
    source = "scene"
    if len(times) < args.min_frames:
        times = uniform(duration(video), args.max_frames)
        source = "uniform"
    times = thin(times, args.max_frames)

    extract(video, times, args.width)
    sheets = tile(vdir, args.cols, args.rows)
    index_path.write_text(
        json.dumps(
            {
                "video": video.name,
                "source": source,
                "cols": args.cols,
                "rows": args.rows,
                "sheets": sheets,
                "frames": [
                    {"n": i, "t": round(t, 2), "label": hhmmss(t)}
                    for i, t in enumerate(times, start=1)
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"{vdir.name}: {len(times)} klatek ({source}), {len(sheets)} siatek")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", help="katalog roboczy poza repozytorium")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.35,
        help="czułość detekcji cięcia; niżej = więcej klatek. Do wykalibrowania na "
        "pierwszym filmie, bo zależy od serii",
    )
    parser.add_argument("--max-frames", type=int, default=60)
    parser.add_argument(
        "--min-frames",
        type=int,
        default=12,
        help="poniżej tej liczby wykrytych cięć skrypt schodzi na próbkowanie równomierne",
    )
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--cols", type=int, default=4)
    parser.add_argument("--rows", type=int, default=3)
    parser.add_argument("--force", action="store_true", help="przelicz mimo gotowych klatek")
    args = parser.parse_args()

    root = reference_root(args.root)
    dirs = video_dirs(root)
    if not dirs:
        raise SystemExit(f"brak pobranych filmów w {root}; uruchom najpierw fetch_reference.py")
    for vdir in dirs:
        process(vdir, args)


if __name__ == "__main__":
    main()

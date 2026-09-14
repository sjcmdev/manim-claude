#!/usr/bin/env python3
"""Buduje manifesty pochodzenia dla plików korpusu obserwacji."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    """SHA-256 zawartości pliku, liczony strumieniowo."""
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(
    data_path: Path,
    document_type: str,
    relative_data_path: str,
    *,
    provenance_status: str,
    source_path: str | None = None,
    source_revision: str | None = None,
    prompt_path: str | None = None,
    prompt_sha256: str | None = None,
    model: str | None = None,
    effort: str | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """Zwraca kompletny manifest; nieznane dane pozostają jawnie puste."""
    if generated_at is None and provenance_status == "generated":
        generated_at = datetime.now(UTC).isoformat().replace("+00:00", "Z")
    return {
        "schema_version": 1,
        "data_path": relative_data_path,
        "document_type": document_type,
        "source_path": source_path,
        "source_revision": source_revision,
        "prompt_path": prompt_path,
        "prompt_sha256": prompt_sha256,
        "model": model,
        "effort": effort,
        "generated_at": generated_at,
        "data_sha256": sha256_file(data_path),
        "provenance_status": provenance_status,
    }


def write_manifest(path: Path, payload: dict[str, Any]) -> None:
    """Zapisuje manifest jako stabilny, czytelny JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

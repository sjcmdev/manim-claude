#!/usr/bin/env python3
"""Waliduje kontrakt korpusu obserwacji oraz manifesty pochodzenia."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from manifest import sha256_file

DOCUMENT_KEYS = {
    "code": "observations",
    "animation": "observations",
    "recipes": "techniques",
}
OBSERVATION_TOPICS = {
    "code": {
        "dekompozycja",
        "ponowne-uzycie",
        "stan-i-updatery",
        "kompozycja",
        "dane-a-obraz",
        "czas-i-tempo",
        "anty-wzorce",
    },
    "animation": {
        "stan-i-updatery",
        "klasy-animacji",
        "wejscie-i-sprzatanie",
        "custom-mobject",
    },
}
RECIPE_TOPICS = {
    "ponowne-uzycie",
    "pokretla-czasowe",
    "iteracja-bez-renderu",
    "przeksztalcanie-wzorow",
    "relacje-wielkosci",
    "przekazywanie-parametrow",
    "reset",
    "buff",
    "szybkosc-vs-dlugosc",
}
CONFIDENCE = {"high", "medium", "low"}
PORTABILITY = {"wysoka", "srednia", "niska"}
MANIFEST_FIELDS = {
    "schema_version",
    "data_path",
    "document_type",
    "source_path",
    "source_revision",
    "prompt_path",
    "prompt_sha256",
    "model",
    "effort",
    "generated_at",
    "data_sha256",
    "provenance_status",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True, order=True)
class ValidationError:
    """Jeden błąd z lokalizacją zrozumiałą dla człowieka."""

    file: str
    field: str
    message: str

    def __str__(self) -> str:
        return f"{self.file}: {self.field}: {self.message}"


def _relative(path: Path, root: Path | None) -> str:
    if root is not None:
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            pass
    return path.as_posix()


def _error(errors: list[ValidationError], file: str, field: str, message: str) -> None:
    errors.append(ValidationError(file, field, message))


def _nonempty_string(value: Any, errors: list[ValidationError], file: str, field: str) -> bool:
    if not isinstance(value, str) or not value.strip():
        _error(errors, file, field, "wymagany niepusty tekst")
        return False
    return True


def _line_reference(
    value: Any,
    errors: list[ValidationError],
    file: str,
    field: str,
    *,
    require_source: bool,
) -> None:
    if not isinstance(value, dict):
        _error(errors, file, field, "wymagany obiekt dowodu")
        return
    required_text = ["file"] + (["source"] if require_source else [])
    for name in required_text:
        _nonempty_string(value.get(name), errors, file, f"{field}.{name}")

    line = value.get("line")
    line_start = value.get("line_start")
    line_end = value.get("line_end")
    single = type(line) is int and line > 0
    line_range = (
        type(line_start) is int
        and type(line_end) is int
        and line_start > 0
        and line_end >= line_start
    )
    if single == line_range:
        _error(
            errors,
            file,
            field,
            "podaj dodatnie `line` albo poprawne `line_start` i `line_end`",
        )


def _validate_observation(
    item: Any,
    kind: str,
    index: int,
    file: str,
    errors: list[ValidationError],
) -> str | None:
    prefix = f"observations[{index}]"
    if not isinstance(item, dict):
        _error(errors, file, prefix, "wymagany obiekt obserwacji")
        return None
    identifier = item.get("id")
    valid_id = _nonempty_string(identifier, errors, file, f"{prefix}.id")
    topic = item.get("topic")
    if topic not in OBSERVATION_TOPICS[kind]:
        allowed = ", ".join(sorted(OBSERVATION_TOPICS[kind]))
        _error(errors, file, f"{prefix}.topic", f"temat spoza taksonomii: {allowed}")
    _nonempty_string(item.get("rule"), errors, file, f"{prefix}.rule")
    if type(item.get("falsifiable")) is not bool:
        _error(errors, file, f"{prefix}.falsifiable", "wymagana wartość logiczna")
    evidence = item.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        _error(errors, file, f"{prefix}.evidence", "wymagana niepusta lista dowodów")
    else:
        for evidence_index, reference in enumerate(evidence):
            _line_reference(
                reference,
                errors,
                file,
                f"{prefix}.evidence[{evidence_index}]",
                require_source=True,
            )
    if item.get("confidence") not in CONFIDENCE:
        _error(
            errors,
            file,
            f"{prefix}.confidence",
            "dozwolone wartości: high, medium, low",
        )
    _nonempty_string(item.get("applies_to"), errors, file, f"{prefix}.applies_to")
    return identifier if valid_id else None


def _validate_recipe(item: Any, index: int, file: str, errors: list[ValidationError]) -> str | None:
    prefix = f"techniques[{index}]"
    if not isinstance(item, dict):
        _error(errors, file, prefix, "wymagany obiekt techniki")
        return None
    identifier = item.get("id")
    valid_id = _nonempty_string(identifier, errors, file, f"{prefix}.id")
    for name in ("nazwa", "problem", "zamiast", "kiedy"):
        _nonempty_string(item.get(name), errors, file, f"{prefix}.{name}")
    topic = item.get("dotyczy_bolaczki")
    if topic is not None and topic not in RECIPE_TOPICS:
        allowed = ", ".join(sorted(RECIPE_TOPICS))
        _error(
            errors,
            file,
            f"{prefix}.dotyczy_bolaczki",
            f"temat spoza taksonomii: {allowed}",
        )
    _line_reference(
        item.get("zrodlo"),
        errors,
        file,
        f"{prefix}.zrodlo",
        require_source=False,
    )
    if item.get("przenosnosc") not in PORTABILITY:
        _error(
            errors,
            file,
            f"{prefix}.przenosnosc",
            "dozwolone wartości: wysoka, srednia, niska",
        )
    return identifier if valid_id else None


def _validate_document(
    data_path: Path, kind: str, *, root: Path | None
) -> tuple[list[ValidationError], list[str]]:
    errors: list[ValidationError] = []
    identifiers: list[str] = []
    file = _relative(data_path, root)
    try:
        payload = yaml.safe_load(data_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        detail = str(exc).splitlines()[0]
        _error(errors, file, "$", f"niepoprawny YAML: {detail}")
        return errors, identifiers
    if not isinstance(payload, dict):
        _error(errors, file, "$", "korzeń dokumentu musi być obiektem")
        return errors, identifiers
    key = DOCUMENT_KEYS[kind]
    items = payload.get(key)
    if not isinstance(items, list) or not items:
        _error(errors, file, key, "wymagana niepusta lista")
        return errors, identifiers
    for index, item in enumerate(items):
        if kind == "recipes":
            identifier = _validate_recipe(item, index, file, errors)
        else:
            identifier = _validate_observation(item, kind, index, file, errors)
        if identifier is not None:
            identifiers.append(identifier)
    return errors, identifiers


def _expected_data_path(data_path: Path, kind: str) -> str:
    return f"{kind}/{data_path.name}"


def _validate_manifest(
    data_path: Path,
    manifest_path: Path,
    kind: str,
    *,
    root: Path | None,
) -> list[ValidationError]:
    errors: list[ValidationError] = []
    data_file = _relative(data_path, root)
    manifest_file = _relative(manifest_path, root)
    if not manifest_path.is_file():
        _error(errors, data_file, "manifest", "brak manifestu")
        return errors
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        _error(errors, manifest_file, "$", f"niepoprawny JSON: {exc}")
        return errors
    if not isinstance(payload, dict):
        _error(errors, manifest_file, "$", "korzeń manifestu musi być obiektem")
        return errors
    for field in sorted(MANIFEST_FIELDS - payload.keys()):
        _error(errors, manifest_file, field, "brak wymaganego pola")
    if payload.get("schema_version") != 1:
        _error(errors, manifest_file, "schema_version", "obsługiwana wersja to 1")
    expected_path = _expected_data_path(data_path, kind)
    if payload.get("data_path") != expected_path:
        _error(errors, manifest_file, "data_path", f"oczekiwano `{expected_path}`")
    if payload.get("document_type") != kind:
        _error(errors, manifest_file, "document_type", f"oczekiwano `{kind}`")
    for field in (
        "source_path",
        "source_revision",
        "prompt_path",
        "prompt_sha256",
        "model",
        "effort",
        "generated_at",
    ):
        if payload.get(field) is not None and not isinstance(payload.get(field), str):
            _error(errors, manifest_file, field, "wymagany tekst albo null")
    prompt_hash = payload.get("prompt_sha256")
    if prompt_hash is not None and not SHA256_RE.fullmatch(prompt_hash):
        _error(errors, manifest_file, "prompt_sha256", "wymagany hash SHA-256")
    expected_hash = sha256_file(data_path)
    if payload.get("data_sha256") != expected_hash:
        _error(errors, manifest_file, "data_sha256", "hash nie zgadza się z plikiem YAML")
    if payload.get("provenance_status") not in {"legacy-unverified", "generated"}:
        _error(
            errors,
            manifest_file,
            "provenance_status",
            "dozwolone wartości: legacy-unverified, generated",
        )
    return errors


def validate_pair(data_path: Path, manifest_path: Path, kind: str) -> list[ValidationError]:
    """Waliduje jeden dokument i odpowiadający mu manifest."""
    if kind not in DOCUMENT_KEYS:
        raise ValueError(f"nieznany typ dokumentu: {kind}")
    document_errors, _ = _validate_document(data_path, kind, root=None)
    return sorted(document_errors + _validate_manifest(data_path, manifest_path, kind, root=None))


def validate_corpus(root: Path) -> list[ValidationError]:
    """Waliduje cały korpus, agregując błędy ze wszystkich plików."""
    root = root.resolve()
    errors: list[ValidationError] = []
    occurrences: dict[str, list[tuple[str, str]]] = {}
    expected_manifests: set[Path] = set()
    for kind in DOCUMENT_KEYS:
        for data_path in sorted((root / kind).glob("*.yaml")):
            document_errors, identifiers = _validate_document(data_path, kind, root=root)
            errors.extend(document_errors)
            data_file = _relative(data_path, root)
            key = DOCUMENT_KEYS[kind]
            for index, identifier in enumerate(identifiers):
                occurrences.setdefault(identifier, []).append((data_file, f"{key}[{index}].id"))
            manifest_path = root / "manifests" / kind / data_path.with_suffix(".json").name
            expected_manifests.add(manifest_path.resolve())
            errors.extend(_validate_manifest(data_path, manifest_path, kind, root=root))
    for identifier, locations in occurrences.items():
        if len(locations) > 1:
            for file, field in locations:
                _error(
                    errors,
                    file,
                    field,
                    f"powtórzony identyfikator `{identifier}`",
                )
    manifests_root = root / "manifests"
    if manifests_root.is_dir():
        for manifest_path in manifests_root.rglob("*.json"):
            if manifest_path.resolve() not in expected_manifests:
                _error(
                    errors,
                    _relative(manifest_path, root),
                    "$",
                    "manifest bez odpowiadającego pliku YAML",
                )
    return sorted(errors)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "observations",
        help="katalog observations do sprawdzenia",
    )
    args = parser.parse_args()
    errors = validate_corpus(args.root)
    for error in errors:
        print(error)
    if errors:
        print(f"walidacja nieudana: {len(errors)} błędów")
        return 1
    print("walidacja udana: korpus i manifesty są spójne")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

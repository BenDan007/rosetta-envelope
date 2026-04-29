from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class EnvelopeValidationError(ValueError):
    """Raised when an envelope fails JSON Schema validation."""


def _load_schema() -> dict[str, Any]:
    schema_path = Path(__file__).resolve().parents[2] / "schemas" / "envelope.schema.json"
    return json.loads(schema_path.read_text(encoding="utf-8"))


def validate_envelope(envelope: dict[str, Any]) -> None:
    """Validate a Rosetta Envelope payload against the JSON Schema."""
    try:
        import jsonschema
    except ImportError as exc:
        raise RuntimeError(
            "Validation requires optional dependency 'jsonschema'. Install with: pip install -e '.[validate]'"
        ) from exc

    schema = _load_schema()

    try:
        jsonschema.validate(instance=envelope, schema=schema)
    except jsonschema.ValidationError as exc:
        path = " -> ".join(str(part) for part in exc.absolute_path) or "<root>"
        raise EnvelopeValidationError(f"Envelope validation failed at {path}: {exc.message}") from exc

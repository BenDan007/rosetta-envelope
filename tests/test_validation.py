import json

import pytest

from rosetta_envelope import build_envelope
from rosetta_envelope.cli import main
from rosetta_envelope.validation import EnvelopeValidationError, validate_envelope


jsonschema = pytest.importorskip("jsonschema")


def test_validate_envelope_valid_payload():
    envelope = build_envelope(document_type="invoice", fields={"amount": 100})
    validate_envelope(envelope)


def test_validate_envelope_invalid_payload_message_is_readable():
    envelope = build_envelope(document_type="invoice", fields={"amount": 100})
    del envelope["payload_hash"]

    with pytest.raises(EnvelopeValidationError) as exc_info:
        validate_envelope(envelope)

    message = str(exc_info.value)
    assert "Envelope validation failed" in message
    assert "payload_hash" in message


def test_cli_validate_command(tmp_path, capsys, monkeypatch):
    envelope = build_envelope(document_type="invoice", fields={"amount": 100})
    valid_file = tmp_path / "valid.json"
    valid_file.write_text(json.dumps(envelope), encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["rosetta-envelope", "validate", str(valid_file)])
    assert main() == 0
    assert "Envelope is valid." in capsys.readouterr().out

    envelope.pop("payload_hash")
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text(json.dumps(envelope), encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["rosetta-envelope", "validate", str(invalid_file)])
    assert main() == 1
    assert "Invalid envelope:" in capsys.readouterr().out

from __future__ import annotations

import base64
import copy
import hashlib
import hmac
import json
import time
import uuid
import zlib
from typing import Any

PROTOCOL = "rosetta-envelope"
VERSION = "0.1.0"
QR_PREFIX = "ros0:"


class EnvelopeError(ValueError):
    """Raised when an envelope cannot be parsed or verified."""


def canonical_json(data: dict[str, Any]) -> bytes:
    """Return deterministic JSON bytes.

    Deterministic serialization is important because signatures and hashes should
    not change when Python dictionary insertion order changes.
    """
    return json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_hex(data: bytes | str) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def sign_hmac_demo(data: bytes, secret: str) -> str:
    """Return a demo HMAC-SHA256 signature.

    This is useful for local experiments only. Production deployments should use
    proper asymmetric signatures, key rotation, issuer identity, timestamps, and
    verification policies.
    """
    return hmac.new(secret.encode("utf-8"), data, hashlib.sha256).hexdigest()


def _unsigned_payload(envelope: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(envelope)
    payload.pop("payload_hash", None)
    payload.pop("signature", None)
    return payload


def build_envelope(
    *,
    document_type: str,
    fields: dict[str, Any],
    document_id: str | None = None,
    issuer: str | None = None,
    source_hash: str | None = None,
    signature_secret: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a Rosetta Envelope payload.

    Args:
        document_type: Application-level type, e.g. "invoice", "exam", "delivery_note".
        fields: Structured business fields.
        document_id: Stable document identifier. If omitted, a UUID is generated.
        issuer: Human-readable issuer name.
        source_hash: Optional hash of the source document or source data.
        signature_secret: Optional demo HMAC secret.
        metadata: Optional extra metadata.

    Returns:
        A JSON-serializable envelope dictionary.
    """
    envelope: dict[str, Any] = {
        "protocol": PROTOCOL,
        "version": VERSION,
        "document_id": document_id or str(uuid.uuid4()),
        "document_type": document_type,
        "created_at_unix": int(time.time()),
        "issuer": issuer,
        "source_hash": source_hash,
        "fields": fields,
        "metadata": metadata or {},
    }

    unsigned = _unsigned_payload(envelope)
    envelope["payload_hash"] = sha256_hex(canonical_json(unsigned))

    if signature_secret:
        envelope["signature"] = {
            "algorithm": "HMAC-SHA256-DEMO",
            "value": sign_hmac_demo(canonical_json(unsigned), signature_secret),
        }

    return envelope


def verify_envelope(envelope: dict[str, Any], signature_secret: str | None = None) -> dict[str, Any]:
    """Verify the envelope hash and optional demo signature.

    Returns a report dictionary instead of raising on invalid envelopes so callers
    can show partial results safely.
    """
    unsigned = _unsigned_payload(envelope)
    expected_hash = sha256_hex(canonical_json(unsigned))
    actual_hash = envelope.get("payload_hash")

    report = {
        "hash_valid": actual_hash == expected_hash,
        "expected_hash": expected_hash,
        "actual_hash": actual_hash,
        "signature_checked": False,
        "signature_valid": None,
    }

    if signature_secret is not None:
        report["signature_checked"] = True
        signature = envelope.get("signature") or {}
        actual_signature = signature.get("value")
        expected_signature = sign_hmac_demo(canonical_json(unsigned), signature_secret)
        report["signature_valid"] = hmac.compare_digest(
            str(actual_signature or ""),
            expected_signature,
        )

    return report


def encode_qr_payload(envelope: dict[str, Any]) -> str:
    """Compress and encode an envelope into QR-friendly text."""
    compressed = zlib.compress(canonical_json(envelope), level=9)
    encoded = base64.urlsafe_b64encode(compressed).decode("ascii").rstrip("=")
    return QR_PREFIX + encoded


def decode_qr_payload(text: str) -> dict[str, Any]:
    """Decode QR-friendly text back into an envelope."""
    if not text.startswith(QR_PREFIX):
        raise EnvelopeError(f"QR payload must start with {QR_PREFIX!r}")

    encoded = text[len(QR_PREFIX):]
    padding = "=" * (-len(encoded) % 4)

    try:
        compressed = base64.urlsafe_b64decode(encoded + padding)
        raw = zlib.decompress(compressed)
        data = json.loads(raw.decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - intentionally wraps any decode error
        raise EnvelopeError("Invalid QR payload") from exc

    if data.get("protocol") != PROTOCOL:
        raise EnvelopeError(f"Unsupported protocol: {data.get('protocol')!r}")

    return data

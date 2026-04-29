# Rosetta Envelope Draft Spec

Version: 0.1.0

## Scope

Rosetta Envelope defines a minimal structured payload that can be bound to a generated PDF or paper document.

It is designed for documents generated from known source data, not for arbitrary scanned documents.

## Envelope fields

| Field | Required | Description |
|---|---:|---|
| `protocol` | Yes | Must be `rosetta-envelope`. |
| `version` | Yes | Envelope version. |
| `document_id` | Yes | Stable document identifier. |
| `document_type` | Yes | Application-level type, e.g. `invoice`, `delivery_note`, `exam_paper`. |
| `created_at_unix` | Yes | Creation timestamp. |
| `issuer` | No | Human-readable issuer. |
| `source_hash` | No | Optional hash of source data or rendered source. |
| `fields` | Yes | Application-specific structured fields. |
| `metadata` | No | Optional extra metadata. |
| `payload_hash` | Yes | SHA-256 hash over the unsigned canonical envelope. |
| `signature` | No | Signature block. The demo implementation uses HMAC and is not production signing. |

## Canonicalization

Payloads are serialized as JSON with:

- UTF-8
- sorted keys
- no insignificant whitespace
- `ensure_ascii=false`

## QR payload format

QR-friendly payloads use:

```text
ros0:<base64url(zlib(canonical_json(envelope)))>
```

This is intentionally simple for the proof of concept.

## Security notes

The current demo HMAC signature is only for local experiments.

A production design should use:

- asymmetric signatures
- issuer identity
- key rotation
- timestamping
- certificate or DID-based trust
- field-level verification policies
- anti-replay checks
- size limits
- safe parsing rules

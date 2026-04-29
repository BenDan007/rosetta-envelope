from rosetta_envelope import (
    build_envelope,
    decode_qr_payload,
    encode_qr_payload,
    verify_envelope,
)


def test_roundtrip_qr_payload():
    envelope = build_envelope(
        document_type="invoice",
        document_id="test-001",
        issuer="Example",
        fields={"amount": 100},
        signature_secret="secret",
    )

    encoded = encode_qr_payload(envelope)
    decoded = decode_qr_payload(encoded)

    assert decoded["protocol"] == "rosetta-envelope"
    assert decoded["document_id"] == "test-001"
    assert decoded["fields"]["amount"] == 100


def test_verify_envelope_hash_and_signature():
    envelope = build_envelope(
        document_type="invoice",
        fields={"amount": 100},
        signature_secret="secret",
    )

    report = verify_envelope(envelope, "secret")

    assert report["hash_valid"] is True
    assert report["signature_checked"] is True
    assert report["signature_valid"] is True


def test_verify_detects_field_tampering():
    envelope = build_envelope(
        document_type="invoice",
        fields={"amount": 100},
        signature_secret="secret",
    )
    envelope["fields"]["amount"] = 999

    report = verify_envelope(envelope, "secret")

    assert report["hash_valid"] is False
    assert report["signature_valid"] is False

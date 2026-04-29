from __future__ import annotations

import pytest

from rosetta_envelope.core import build_envelope
from rosetta_envelope.pdf import generate_simple_pdf, read_envelope_from_pdf


def _pdf_dependencies_available() -> bool:
    try:
        import pypdf  # noqa: F401
        import qrcode  # noqa: F401
        import reportlab  # noqa: F401
    except ImportError:
        return False
    return True


pytestmark = pytest.mark.skipif(
    not _pdf_dependencies_available(),
    reason="PDF dependencies not installed; install with pip install -e '.[pdf]'",
)


def test_read_envelope_from_pdf_roundtrip(tmp_path):
    envelope = build_envelope(
        document_type="invoice",
        document_id="demo-invoice-001",
        issuer="Example Ltd",
        fields={"invoice_number": "INV-2026-0001", "total_amount": 1280.0},
        signature_secret="demo-secret",
    )

    pdf_path = tmp_path / "demo.pdf"
    generate_simple_pdf(
        output_path=pdf_path,
        title="Demo Invoice",
        lines=["Invoice number: INV-2026-0001"],
        envelope=envelope,
    )

    decoded = read_envelope_from_pdf(pdf_path)
    assert decoded == envelope


def test_read_envelope_from_pdf_missing_metadata(tmp_path):
    pdf_path = tmp_path / "plain.pdf"
    generate_simple_pdf(
        output_path=pdf_path,
        title="Plain PDF",
        lines=["No envelope metadata here"],
        envelope=None,
    )

    with pytest.raises(ValueError, match="No /RosettaEnvelopeJson metadata"):
        read_envelope_from_pdf(pdf_path)

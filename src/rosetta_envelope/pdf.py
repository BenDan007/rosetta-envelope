from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

from .core import canonical_json, encode_qr_payload


def generate_simple_pdf(
    *,
    output_path: str | Path,
    title: str,
    lines: list[str],
    envelope: dict[str, Any] | None = None,
) -> Path:
    """Generate a simple demo PDF with optional QR code footer.

    This is a demo helper, not a production PDF engine.
    """
    try:
        import qrcode
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.pdfgen import canvas
        from pypdf import PdfReader, PdfWriter
    except ImportError as exc:
        raise RuntimeError(
            "PDF support requires optional dependencies. Install with: "
            'pip install -e ".[pdf]"'
        ) from exc

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        base_pdf = tmpdir_path / "base.pdf"

        c = canvas.Canvas(str(base_pdf), pagesize=A4)
        width, height = A4

        c.setFont("Helvetica-Bold", 18)
        c.drawString(20 * mm, height - 25 * mm, title)

        c.setFont("Helvetica", 10)
        y = height - 40 * mm
        for line in lines:
            c.drawString(20 * mm, y, line)
            y -= 7 * mm

        if envelope:
            qr_text = encode_qr_payload(envelope)
            qr_img = qrcode.make(qr_text)
            qr_path = tmpdir_path / "qr.png"
            qr_img.save(qr_path)

            c.setFont("Helvetica", 7)
            c.drawString(20 * mm, 23 * mm, "Rosetta Envelope demo payload:")
            c.drawImage(str(qr_path), 20 * mm, 30 * mm, width=28 * mm, height=28 * mm)
            c.drawString(52 * mm, 43 * mm, f"Document ID: {envelope.get('document_id')}")
            c.drawString(52 * mm, 37 * mm, f"Payload hash: {str(envelope.get('payload_hash'))[:24]}...")

        c.showPage()
        c.save()

        if envelope:
            reader = PdfReader(str(base_pdf))
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            # Keep metadata short. Full payloads may exceed what some PDF readers
            # comfortably show as document metadata.
            writer.add_metadata({
                "/RosettaEnvelopeProtocol": envelope.get("protocol", ""),
                "/RosettaEnvelopeVersion": envelope.get("version", ""),
                "/RosettaEnvelopeDocumentId": envelope.get("document_id", ""),
                "/RosettaEnvelopePayloadHash": envelope.get("payload_hash", ""),
                "/RosettaEnvelopeJson": canonical_json(envelope).decode("utf-8"),
            })

            with output_path.open("wb") as f:
                writer.write(f)
        else:
            output_path.write_bytes(base_pdf.read_bytes())

    return output_path

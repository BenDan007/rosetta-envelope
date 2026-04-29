# Rosetta Envelope

**Rosetta Envelope** is a small open-source proof of concept for making generated PDFs and paper documents easier for machines and AI agents to read.

The core idea is intentionally simple:

> When a business document is generated, attach a signed structured payload to it, so software does not need to OCR or guess the document structure later.

This project is **not** an OCR replacement, not a universal PDF parser, and not a finished standard. It is a minimal experiment around:

- structured JSON payloads for generated documents
- PDF metadata embedding
- QR / matrix-code friendly payloads
- document hashes
- demo signatures
- AI-readable document workflows

## Why this exists

PDFs and printed documents are usually optimized for human eyes. AI systems and business software often have to reconstruct structure from layout, OCR, or heuristics.

Rosetta Envelope explores a different approach:

1. Generate a human-readable document.
2. Generate a machine-readable JSON payload from the same source data.
3. Bind them together with hashes and signatures.
4. Store the payload in the PDF and/or print a QR code on the page.
5. Let downstream systems read the structured payload directly.

## What this project does today

This repository currently provides a small Python package that can:

- build a canonical structured envelope
- compute stable SHA-256 hashes
- add a demo HMAC signature
- compress and encode an envelope for QR usage
- decode QR payload text back into JSON
- generate a simple demo PDF with an optional QR code footer

## What this project does not do

Rosetta Envelope does **not** claim to:

- end OCR
- understand all documents
- preserve all semantic meaning
- replace PDF, QR codes, XML, EDI, Peppol, Factur-X, ZUGFeRD, or e-invoicing standards
- provide production-grade cryptographic signing
- define a global standard

It is a small building block for experiments.

## Example payload

```json
{
  "protocol": "rosetta-envelope",
  "version": "0.1.0",
  "document_id": "demo-invoice-001",
  "document_type": "invoice",
  "issuer": "Example Ltd",
  "fields": {
    "invoice_number": "INV-2026-0001",
    "buyer": "Acme Corp",
    "currency": "GBP",
    "total_amount": 1280.0
  },
  "payload_hash": "...",
  "signature": {
    "algorithm": "HMAC-SHA256-DEMO",
    "value": "..."
  }
}
```

## Install locally

```bash
git clone https://github.com/YOUR_USERNAME/rosetta-envelope.git
cd rosetta-envelope
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[pdf,test]"
```

## Try the demo

```bash
rosetta-envelope pack examples/invoice.json
rosetta-envelope unpack "ros0:..."
rosetta-envelope generate-demo --output examples/out/demo.pdf
```

The PDF demo requires optional dependencies:

```bash
pip install -e ".[pdf]"
```

## Repository status

This is an early concept repo. The recommended use is experimentation, discussion, and prototype building.

## Roadmap

See [`docs/roadmap.md`](docs/roadmap.md).

## License

MIT. See [`LICENSE`](LICENSE).

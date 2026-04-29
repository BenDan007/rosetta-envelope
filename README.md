# Rosetta Envelope

**Anti-OCR for generated documents: attach structure before AI has to guess it.**

Rosetta Envelope is a small, open-source proof of concept for generated PDFs and paper documents.

Plain English version: when you create a document, also create a structured JSON payload from the same source data, then bind them together so downstream software can read the structure directly instead of reconstructing it from layout.

---

## Before / after

```text
Before
------
System A -> PDF (human layout)
             -> OCR / parsing / guessing -> System B JSON

After (Rosetta Envelope)
------------------------
System A -> PDF + envelope JSON (same source data)
             -> read structured payload directly -> System B JSON
```

---

## Quickstart

### 1) Install locally

```bash
git clone https://github.com/YOUR_USERNAME/rosetta-envelope.git
cd rosetta-envelope
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[pdf,validate]"
```

- `pdf` adds demo PDF generation + PDF metadata reading.
- `validate` adds JSON Schema validation.

### 2) Generate a demo PDF

```bash
rosetta-envelope generate-demo --output examples/out/demo.pdf
```

### 3) Read the envelope back from that PDF

```bash
rosetta-envelope read-pdf examples/out/demo.pdf
```

### 4) Validate an example JSON file

```bash
rosetta-envelope validate examples/invoice.json
```

---

## What this is

- A minimal envelope format (`protocol`, `document_id`, `fields`, hashes, optional signature).
- A Python package + CLI for packing/unpacking payloads and generating a demo PDF.
- A way to experiment with structure-first document workflows for generated documents.

## What this is not

- Not an OCR replacement.
- Not a universal parser for arbitrary PDFs or scans.
- Not a production trust framework yet.
- Not a claim that AI can "understand all documents" from this alone.

---

## Why this might matter

- Many business documents start as structured data, then lose structure when rendered to PDF/print.
- OCR and layout heuristics are useful, but brittle and expensive to maintain.
- Carrying a signed/hashed payload with the document can reduce ambiguity for downstream automation.

---

## Demo workflow

1. Start with source data (for example, invoice fields).
2. Build an envelope JSON with hashes/signature.
3. Embed it in PDF metadata and QR text.
4. Read payload back using `read-pdf` (metadata path) or `unpack` (QR payload path).
5. Validate schema and verify signatures according to your trust model.

---

## Roadmap

See [`docs/roadmap.md`](docs/roadmap.md) for upcoming work (schema evolution, stronger signing, QR chunking, browser demo).

## Security / trust warning

This is a proof-of-concept. Current demo signing is HMAC-based and not a full production trust system.

Read [`SECURITY.md`](SECURITY.md) before using this beyond local experiments.

## Spec and design notes

- Draft spec: [`docs/spec.md`](docs/spec.md)
- Positioning notes: [`docs/positioning.md`](docs/positioning.md)

## License

MIT. See [`LICENSE`](LICENSE).

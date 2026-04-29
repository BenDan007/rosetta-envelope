# Useful Codex prompts

Use these prompts after opening the repository in Codex CLI, IDE extension, or Codex web.

## Prompt 1: Add JSON Schema validation

```text
Add JSON Schema validation for Rosetta Envelope payloads.

Requirements:
- Add a schema file under schemas/envelope.schema.json.
- Add a validation function in src/rosetta_envelope/validation.py.
- Add an optional dependency on jsonschema.
- Add CLI command: rosetta-envelope validate <file>.
- Add tests for valid and invalid envelopes.
- Keep error messages human-readable.
```

## Prompt 2: Extract payload from PDF metadata

```text
Implement extraction of Rosetta Envelope payloads from PDF metadata.

Requirements:
- Add function read_envelope_from_pdf(path) in src/rosetta_envelope/pdf.py.
- Read /RosettaEnvelopeJson metadata from PDFs produced by generate_simple_pdf.
- Add CLI command: rosetta-envelope read-pdf <path>.
- Add tests if PDF dependencies are installed; otherwise skip gracefully.
```

## Prompt 3: Add real signing option

```text
Add optional Ed25519 signing support.

Requirements:
- Keep the existing HMAC demo for backwards compatibility.
- Add a new optional dependency group: crypto.
- Use a well-maintained Python crypto package.
- Add sign_ed25519 and verify_ed25519 functions.
- Update SECURITY.md to explain the difference between demo HMAC and Ed25519.
- Add tests.
```

## Prompt 4: Improve QR handling

```text
Improve QR payload handling for larger envelopes.

Requirements:
- Add a function estimate_qr_size(envelope).
- Add chunking: ros0c:<doc_id>:<index>:<total>:<payload>.
- Add reassemble_chunks(chunks).
- Add tests for chunking and reassembly.
- Document limits in docs/spec.md.
```

## Prompt 5: Build a simple web demo

```text
Create a minimal web demo for Rosetta Envelope.

Requirements:
- Use a lightweight Python web framework or a static HTML page.
- Let the user paste JSON and generate a QR payload.
- Let the user paste a ros0 payload and decode it.
- Keep it local-only; no external API calls.
- Add instructions to README.
```

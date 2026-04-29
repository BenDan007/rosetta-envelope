# Codex / Agent Instructions

You are working on Rosetta Envelope, a small proof-of-concept open-source project.

## Project goal

Build a minimal, honest implementation of a structured payload envelope for generated PDFs and paper documents.

Do not overclaim. This is not an OCR replacement or universal document standard.

## Preferred engineering style

- Keep the core small.
- Prefer plain Python and explicit functions.
- Add tests for every behavior change.
- Avoid heavyweight frameworks until there is a real need.
- Keep security warnings visible.
- Make examples easy to run.

## Good next tasks

1. Add JSON Schema validation for envelopes.
2. Add PDF extraction for `/RosettaEnvelopeJson`.
3. Replace demo HMAC with optional Ed25519 signing.
4. Add multi-page QR chunking.
5. Add a simple browser demo for scanning QR payloads.
6. Add a delivery note example.
7. Add an exam paper example with generated PDF output.

## Things not to do

- Do not claim 100% document understanding.
- Do not claim the project ends OCR.
- Do not add semantic-vector magic.
- Do not hide security limitations.
- Do not introduce cloud services without a local-first path.

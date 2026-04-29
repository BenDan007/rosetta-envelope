# Demo artifacts

This folder contains small, committed demo artifacts for first-time visitors.

## Included files

- `demo_envelope.json`: A readable Rosetta Envelope payload for a demo invoice.

## Optional PDF artifact

The CLI can generate `demo.pdf` with embedded `/RosettaEnvelopeJson` metadata:

```bash
PYTHONPATH=src python -m rosetta_envelope.cli generate-demo --output examples/demo/demo.pdf
```

In this environment, optional PDF dependencies were unavailable, so `demo.pdf` is not committed here.

## Read the envelope back

If you generated `demo.pdf`, extract metadata with:

```bash
PYTHONPATH=src python -m rosetta_envelope.cli read-pdf examples/demo/demo.pdf
```

You can always inspect the committed JSON directly:

```bash
cat examples/demo/demo_envelope.json
```

## Validate the extracted JSON

```bash
PYTHONPATH=src python -m rosetta_envelope.cli validate examples/demo/demo_envelope.json
```

Validation requires the optional `jsonschema` dependency.

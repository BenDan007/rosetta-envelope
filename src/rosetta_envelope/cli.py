from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .core import build_envelope, decode_qr_payload, encode_qr_payload, verify_envelope
from .pdf import generate_simple_pdf
from .validation import EnvelopeValidationError, validate_envelope


def _load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def cmd_pack(args: argparse.Namespace) -> int:
    data = _load_json(args.input)
    envelope = build_envelope(
        document_type=data.get("document_type", "document"),
        document_id=data.get("document_id"),
        issuer=data.get("issuer"),
        fields=data.get("fields", data),
        metadata=data.get("metadata", {}),
        signature_secret=args.secret,
    )
    print(encode_qr_payload(envelope))
    return 0


def cmd_unpack(args: argparse.Namespace) -> int:
    envelope = decode_qr_payload(args.payload)
    print(json.dumps(envelope, ensure_ascii=False, indent=2, sort_keys=True))
    if args.secret:
        print("\nVerification:")
        print(json.dumps(verify_envelope(envelope, args.secret), indent=2, sort_keys=True))
    return 0


def cmd_generate_demo(args: argparse.Namespace) -> int:
    fields = {
        "invoice_number": "INV-2026-0001",
        "buyer": "Acme Corp",
        "seller": "Example Ltd",
        "currency": "GBP",
        "total_amount": 1280.0,
        "line_items": [
            {
                "description": "Demo sensor",
                "quantity": 2,
                "unit_price": 640.0,
                "amount": 1280.0,
            }
        ],
    }

    envelope = build_envelope(
        document_type="invoice",
        document_id="demo-invoice-001",
        issuer="Example Ltd",
        fields=fields,
        signature_secret=args.secret,
    )

    output = generate_simple_pdf(
        output_path=args.output,
        title="Demo Invoice",
        lines=[
            "Invoice number: INV-2026-0001",
            "Seller: Example Ltd",
            "Buyer: Acme Corp",
            "Item: Demo sensor x 2",
            "Total: GBP 1280.00",
            "",
            "This PDF contains a demo Rosetta Envelope payload in metadata and QR form.",
        ],
        envelope=envelope,
    )
    print(f"Wrote {output}")
    return 0



def cmd_validate(args: argparse.Namespace) -> int:
    envelope = _load_json(args.file)
    try:
        validate_envelope(envelope)
    except EnvelopeValidationError as exc:
        print(f"Invalid envelope: {exc}")
        return 1
    except RuntimeError as exc:
        print(str(exc))
        return 2

    print("Envelope is valid.")
    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rosetta-envelope")
    sub = parser.add_subparsers(required=True)

    pack = sub.add_parser("pack", help="Build and encode a QR-friendly envelope from JSON.")
    pack.add_argument("input", help="Input JSON file.")
    pack.add_argument("--secret", default=None, help="Optional demo HMAC secret.")
    pack.set_defaults(func=cmd_pack)

    unpack = sub.add_parser("unpack", help="Decode a QR-friendly envelope.")
    unpack.add_argument("payload", help="Payload text beginning with ros0:")
    unpack.add_argument("--secret", default=None, help="Optional demo HMAC secret for verification.")
    unpack.set_defaults(func=cmd_unpack)

    demo = sub.add_parser("generate-demo", help="Generate a demo PDF.")
    demo.add_argument("--output", default="examples/out/demo.pdf")
    demo.add_argument("--secret", default="demo-secret")
    demo.set_defaults(func=cmd_generate_demo)

    validate = sub.add_parser("validate", help="Validate an envelope JSON file against the schema.")
    validate.add_argument("file", help="Envelope JSON file to validate.")
    validate.set_defaults(func=cmd_validate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

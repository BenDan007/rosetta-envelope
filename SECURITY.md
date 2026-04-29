# Security

This repository is a proof of concept.

Do not use the demo HMAC signing implementation for production trust workflows.

A production implementation should include:

- asymmetric signatures
- issuer verification
- key rotation
- timestamping
- payload size limits
- safe JSON parsing
- anti-replay controls
- strict validation against schemas
- explicit trust policies

If you find a vulnerability, please open a private security advisory if the repository is hosted on GitHub, or contact the maintainer.

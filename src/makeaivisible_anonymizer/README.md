# Anonymization Service Package

This package is the first privacy boundary after an upload. It accepts conversation
messages, redacts supported identifiers, and returns anonymized messages plus a redaction
report.

## File Map

- `main.py`: FastAPI app, `/health`, and `/anonymize`.
- `models.py`: request and response schemas, validation limits, and output shapes.
- `limits.py`: request body size guard before JSON parsing.
- `detectors.py`: active regex detectors and documented detector gaps.
- `redaction.py`: matching, overlap handling, replacement labels, and redaction counts.

## Request Flow

1. `limits.py` rejects oversized HTTP bodies.
2. `models.py` validates message roles, content lengths, and unknown fields.
3. `main.py` loops through messages and calls `redaction.py`.
4. `redaction.py` uses `detectors.py` to replace matched identifiers.
5. The response includes generated `conversation_id`, redacted messages, and a report.

## Where To Add New PII Work

Start with tests in `tests/test_redaction.py`, then update `detectors.py`. Do not add
real names, real schools, real addresses, or real conversations as fixtures. Use synthetic
examples only.

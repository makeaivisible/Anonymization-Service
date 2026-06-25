# Anonymization Service

Privacy-preserving ingestion service for Make AI Visible.

This repository owns the first protected boundary after a contributor submits an AI conversation export. Its job is to remove or transform personally identifying information before anything is stored, reviewed, scored, or published.

## MVP Scope

- Accept raw export uploads from the portal.
- Normalize supported export formats into a common conversation schema.
- Detect and redact direct identifiers such as names, emails, phone numbers, addresses, schools, usernames, URLs, and account IDs.
- Produce an anonymized record and a structured redaction report.
- Discard raw input after processing unless an explicit, reviewed retention mode is enabled.
- Provide tests for common and adversarial PII examples.

## Privacy Boundary

Raw conversations are considered highly sensitive. The MVP must treat raw text as temporary processing input, not durable research data.

## Suggested Stack

- Python FastAPI service.
- Presidio, spaCy, regex detectors, or equivalent layered PII detection.
- Pytest fixtures with synthetic teen conversation examples.
- JSON schema for anonymized conversation output.

## First Milestone

Expose a local `/anonymize` endpoint with deterministic redaction tests and a documented anonymized output schema.

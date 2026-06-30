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

## Current Baseline

The repository now includes a runnable deterministic baseline. It detects emails, phone
numbers, URLs, usernames, and explicitly labeled account IDs. It processes requests in
memory and does not include a database or file persistence layer.

This baseline is not sufficient for production or real contributor data. Names, schools,
free-form addresses, indirect identifiers, and context-dependent identifiers require a
layered detector and expert privacy review.

### Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn makeaivisible_anonymizer.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the generated API documentation, or submit the
synthetic example directly:

```bash
curl -s http://127.0.0.1:8000/anonymize \
  -H 'content-type: application/json' \
  --data @examples/request.json
```

### Contract

`POST /anonymize` accepts a conversation identifier and a non-empty list of messages.
The response contains:

- `schema_version`: version of the anonymized record contract.
- `conversation_id`: caller-provided identifier; callers must not use a personal identifier.
- `messages`: roles and redacted message content.
- `redaction_report`: counts and source spans without the original sensitive values.

The generated OpenAPI schema is the canonical machine-readable contract for this MVP.

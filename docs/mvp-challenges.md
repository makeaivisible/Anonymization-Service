# MVP Challenges

This repository implements challenge 3 and starts challenge 4. The full Make AI Visible
MVP is split into 12 contributor-sized challenges so people can find a useful place to
edit without needing to understand every repository first.

## Challenge Map

| # | Repository | Challenge | Best first edit |
| --- | --- | --- | --- |
| 1 | Portal-Frontend | Build mobile-first consent and upload prototype | Copy the anonymization API contract from this repo into a mock upload flow. |
| 2 | Portal-Frontend | Add platform export guidance | Draft teen- and caregiver-friendly export instructions with no secrets or credentials. |
| 3 | Anonymization-Service | Implement anonymized conversation schema and `/anonymize` endpoint | Extend `src/makeaivisible_anonymizer/models.py` or endpoint tests. |
| 4 | Anonymization-Service | Add PII detector test suite | Add synthetic detector cases in `tests/test_redaction.py`. |
| 5 | NLP-Scoring-Engine | Create baseline scoring schema and deterministic rubric scorer | Use anonymized output examples from this service as scoring input fixtures. |
| 6 | NLP-Scoring-Engine | Build evaluation harness for human-label comparison | Define synthetic label fixtures before model-backed scoring. |
| 7 | Dashboard | Build synthetic aggregate dashboard | Consume aggregate-only sample outputs, never individual messages. |
| 8 | Dashboard | Add privacy threshold and suppression rules | Add small-cell suppression examples and tests. |
| 9 | Dataset-Publishing-Pipeline | Create release manifest and aggregate export builder | Require anonymized, reviewed input metadata. |
| 10 | Dataset-Publishing-Pipeline | Draft dataset card and release checklist generator | Generate a review-ready dataset card from release metadata. |
| 11 | Governance-Documentation | Draft data lifecycle and consent documents | Keep unresolved legal, IRB, and expert-review questions visible. |
| 12 | Governance-Documentation | Draft human review and scoring validation protocol | Separate draft tooling from validated research claims. |

## Current Editable Areas

- `src/makeaivisible_anonymizer/detectors.py`: add or review detector definitions.
- `tests/test_redaction.py`: add synthetic positive and near-miss examples.
- `examples/challenge_backlog.json`: turn challenge notes into issues or project cards.
- `docs/pii-detector-playbook.md`: document detector rules, assumptions, and known gaps.

Use only synthetic examples. Do not add real contributor conversations, real student names,
real schools, addresses, screenshots, or exports.

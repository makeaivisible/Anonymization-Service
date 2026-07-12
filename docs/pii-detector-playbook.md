# PII Detector Playbook

The MVP detector is intentionally conservative. It is good enough for synthetic demos and
local integration work, not for real contributor data.

## How To Add A Detector

1. Add synthetic positive examples and near misses in `tests/test_redaction.py`.
2. Add the detector in `src/makeaivisible_anonymizer/detectors.py`.
3. Confirm the redaction report includes type, span, and replacement metadata.
4. Update this playbook with limitations and review notes.

## Active Detectors

| Entity type | Current approach | Known limitation |
| --- | --- | --- |
| `EMAIL` | Regex for common email formats | Does not detect obfuscated emails like `name at example dot org`. |
| `URL` | Regex for `http`, `https`, and `www` links | May include trailing punctuation in unusual prose. |
| `PHONE` | Regex for North American synthetic examples | Not international or locale-aware. |
| `USERNAME` | Regex for `@handle` patterns | Can miss usernames without `@`. |
| `ACCOUNT_ID` | Regex for explicitly labeled account/user/member IDs | Does not infer unlabeled IDs. |

## Open Detector Gaps

These are visible in `DETECTOR_GAPS` so contributors can pick them up intentionally:

- `PERSON_NAME`
- `SCHOOL`
- `ADDRESS`
- `INDIRECT_IDENTIFIER`

Each gap needs examples, false-positive checks, and privacy review before it should be
enabled for real data.

`tests/test_redaction.py` includes expected-failure tests for these gaps. They should
only be converted into passing tests when the detector behavior, limitations, and review
requirements are documented.

## Challenge #4 Acceptance Progress

| Identifier type | Status |
| --- | --- |
| Emails | Active deterministic detector and tests |
| Phone numbers | Active deterministic detector and tests |
| Usernames | Active deterministic detector and tests |
| URLs | Active deterministic detector and tests |
| Account IDs | Active deterministic detector and tests |
| Names | Expected-failure synthetic gap test |
| Schools | Expected-failure synthetic gap test |
| Addresses | Expected-failure synthetic gap test |
| Indirect identifiers | Expected-failure synthetic gap test |

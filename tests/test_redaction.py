from collections import defaultdict

import pytest

from makeaivisible_anonymizer.redaction import redact_text


@pytest.mark.parametrize(
    ("source", "expected_type"),
    [
        ("student+test@example.co.uk", "EMAIL"),
        ("604-555-0100", "PHONE"),
        ("(604) 555-0100", "PHONE"),
        ("www.example.ca/path?q=1", "URL"),
        ("@student_01", "USERNAME"),
        ("account-id: ABCD_1234", "ACCOUNT_ID"),
    ],
)
def test_supported_identifier_types(source: str, expected_type: str) -> None:
    result, redactions = redact_text(source, 0, defaultdict(int))

    assert source not in result
    assert len(redactions) == 1
    assert redactions[0].entity_type == expected_type
    assert result == f"[{expected_type}_1]"


@pytest.mark.parametrize(
    "source",
    [
        "Version 1.2.3 is available",
        "The score was 604 points",
        "Use the word at without a handle",
        "example dot org",
    ],
)
def test_common_near_misses_are_not_redacted(source: str) -> None:
    result, redactions = redact_text(source, 0, defaultdict(int))

    assert result == source
    assert redactions == []

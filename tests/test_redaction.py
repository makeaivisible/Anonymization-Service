from collections import defaultdict

import pytest

from makeaivisible_anonymizer.detectors import DETECTOR_GAPS, DETECTORS
from makeaivisible_anonymizer.redaction import redact_text


def test_detector_registry_exposes_active_and_gap_work() -> None:
    active_types = {detector.entity_type for detector in DETECTORS}
    gap_types = {gap["entity_type"] for gap in DETECTOR_GAPS}

    assert active_types == {"ACCOUNT_ID", "EMAIL", "PHONE", "URL", "USERNAME"}
    assert {"ADDRESS", "INDIRECT_IDENTIFIER", "PERSON_NAME", "SCHOOL"} <= gap_types


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


@pytest.mark.xfail(reason="Challenge #4 gap: person-name detection needs expert review")
def test_future_person_name_detection_gap() -> None:
    result, redactions = redact_text("My name is Maya Chen.", 0, defaultdict(int))

    assert "Maya Chen" not in result
    assert redactions[0].entity_type == "PERSON_NAME"


@pytest.mark.xfail(reason="Challenge #4 gap: school detection needs curated examples")
def test_future_school_detection_gap() -> None:
    result, redactions = redact_text("I go to Cedar Ridge Secondary.", 0, defaultdict(int))

    assert "Cedar Ridge Secondary" not in result
    assert redactions[0].entity_type == "SCHOOL"


@pytest.mark.xfail(reason="Challenge #4 gap: address detection needs locale-aware rules")
def test_future_address_detection_gap() -> None:
    result, redactions = redact_text("Please pick me up at 42 Maple Street.", 0, defaultdict(int))

    assert "42 Maple Street" not in result
    assert redactions[0].entity_type == "ADDRESS"


@pytest.mark.xfail(reason="Challenge #4 gap: indirect identifiers need policy decisions")
def test_future_indirect_identifier_detection_gap() -> None:
    result, redactions = redact_text(
        "I am the only grade 10 student on the robotics team in my town.",
        0,
        defaultdict(int),
    )

    assert "only grade 10 student" not in result
    assert redactions[0].entity_type == "INDIRECT_IDENTIFIER"

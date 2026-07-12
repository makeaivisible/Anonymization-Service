import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Detector:
    entity_type: str
    pattern: re.Pattern[str]
    notes: str


DETECTORS = (
    Detector(
        "EMAIL",
        re.compile(r"(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[\w-]+)+", re.I),
        "Direct email addresses.",
    ),
    Detector(
        "URL",
        re.compile(r"\b(?:https?://|www\.)[^\s<>]+", re.I),
        "Web links that may expose profiles, schools, or accounts.",
    ),
    Detector(
        "PHONE",
        re.compile(r"(?<!\w)(?:\+?1[ .-]?)?(?:\(\d{3}\)|\d{3})[ .-]\d{3}[ .-]\d{4}(?!\w)"),
        "North American phone-number formats used in synthetic fixtures.",
    ),
    Detector(
        "USERNAME",
        re.compile(r"(?<![\w@])@[A-Za-z0-9_]{2,32}\b"),
        "Social or platform handles.",
    ),
    Detector(
        "ACCOUNT_ID",
        re.compile(r"\b(?:account|user|member)[ _-]?id\s*[:=#]\s*[A-Za-z0-9_-]{4,64}\b", re.I),
        "Explicitly labeled account, user, or member identifiers.",
    ),
)


DETECTOR_GAPS = (
    {
        "entity_type": "PERSON_NAME",
        "challenge": 4,
        "status": "needs layered detection and expert review",
        "edit_hint": "Add synthetic fixtures in tests/test_redaction.py before enabling a detector.",
    },
    {
        "entity_type": "SCHOOL",
        "challenge": 4,
        "status": "needs curated examples and false-positive review",
        "edit_hint": "Start with examples/challenge_backlog.json and avoid real student data.",
    },
    {
        "entity_type": "ADDRESS",
        "challenge": 4,
        "status": "needs locale-aware detection",
        "edit_hint": "Cover street, city, postal-code, and near-miss examples.",
    },
    {
        "entity_type": "INDIRECT_IDENTIFIER",
        "challenge": 4,
        "status": "needs policy decision",
        "edit_hint": "Document risky context combinations before writing automated rules.",
    },
)

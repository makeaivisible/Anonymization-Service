import re
from collections import Counter, defaultdict
from dataclasses import dataclass

from .models import Redaction


@dataclass(frozen=True)
class Detector:
    entity_type: str
    pattern: re.Pattern[str]


DETECTORS = (
    Detector("EMAIL", re.compile(r"(?<![\w.+-])[\w.+-]+@[\w-]+(?:\.[\w-]+)+", re.I)),
    Detector("URL", re.compile(r"\b(?:https?://|www\.)[^\s<>]+", re.I)),
    Detector(
        "PHONE",
        re.compile(r"(?<!\w)(?:\+?1[ .-]?)?(?:\(\d{3}\)|\d{3})[ .-]\d{3}[ .-]\d{4}(?!\w)"),
    ),
    Detector("USERNAME", re.compile(r"(?<![\w@])@[A-Za-z0-9_]{2,32}\b")),
    Detector(
        "ACCOUNT_ID",
        re.compile(r"\b(?:account|user|member)[ _-]?id\s*[:=#]\s*[A-Za-z0-9_-]{4,64}\b", re.I),
    ),
)


@dataclass(frozen=True)
class Match:
    entity_type: str
    start: int
    end: int


def _matches(text: str) -> list[Match]:
    candidates = [
        Match(detector.entity_type, match.start(), match.end())
        for detector in DETECTORS
        for match in detector.pattern.finditer(text)
    ]
    candidates.sort(key=lambda item: (item.start, -(item.end - item.start)))

    accepted: list[Match] = []
    for candidate in candidates:
        if any(candidate.start < item.end and item.start < candidate.end for item in accepted):
            continue
        accepted.append(candidate)
    return accepted


def redact_text(
    text: str,
    message_index: int,
    counters: defaultdict[str, int],
) -> tuple[str, list[Redaction]]:
    matches = _matches(text)
    output: list[str] = []
    redactions: list[Redaction] = []
    cursor = 0

    for match in matches:
        counters[match.entity_type] += 1
        replacement = f"[{match.entity_type}_{counters[match.entity_type]}]"
        output.extend((text[cursor : match.start], replacement))
        redactions.append(
            Redaction(
                message_index=message_index,
                entity_type=match.entity_type,
                start=match.start,
                end=match.end,
                replacement=replacement,
            )
        )
        cursor = match.end

    output.append(text[cursor:])
    return "".join(output), redactions


def count_by_type(redactions: list[Redaction]) -> dict[str, int]:
    return dict(sorted(Counter(item.entity_type for item in redactions).items()))

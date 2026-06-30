from collections import defaultdict

from fastapi import FastAPI

from . import __version__
from .models import (
    AnonymizeRequest,
    AnonymizeResponse,
    ConversationMessage,
    RedactionSummary,
)
from .redaction import count_by_type, redact_text

app = FastAPI(
    title="Make AI Visible Anonymization Service",
    description="Deterministic baseline for removing direct identifiers from conversations.",
    version=__version__,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.post("/anonymize", response_model=AnonymizeResponse)
def anonymize(request: AnonymizeRequest) -> AnonymizeResponse:
    counters: defaultdict[str, int] = defaultdict(int)
    messages: list[ConversationMessage] = []
    redactions = []

    for index, message in enumerate(request.messages):
        content, message_redactions = redact_text(message.content, index, counters)
        messages.append(ConversationMessage(role=message.role, content=content))
        redactions.extend(message_redactions)

    return AnonymizeResponse(
        schema_version="0.1.0",
        conversation_id=request.conversation_id,
        messages=messages,
        redaction_report=RedactionSummary(
            total=len(redactions),
            by_type=count_by_type(redactions),
            redactions=redactions,
        ),
    )

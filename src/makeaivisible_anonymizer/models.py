from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


MAX_TOTAL_CONTENT_CHARS = 1_000_000


class Role(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConversationMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: Role
    content: str = Field(min_length=1, max_length=50_000)

    @field_validator("content")
    @classmethod
    def content_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("content must not be blank")
        return value


class AnonymizeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    messages: list[ConversationMessage] = Field(min_length=1, max_length=1_000)

    @model_validator(mode="after")
    def total_content_must_fit_limit(self) -> "AnonymizeRequest":
        total = sum(len(message.content) for message in self.messages)
        if total > MAX_TOTAL_CONTENT_CHARS:
            raise ValueError(
                f"total message content must not exceed {MAX_TOTAL_CONTENT_CHARS} characters"
            )
        return self


class Redaction(BaseModel):
    message_index: int
    entity_type: str
    start: int
    end: int
    replacement: str


class RedactionSummary(BaseModel):
    total: int
    by_type: dict[str, int]
    redactions: list[Redaction]


class AnonymizeResponse(BaseModel):
    schema_version: str
    conversation_id: UUID = Field(default_factory=uuid4)
    messages: list[ConversationMessage]
    redaction_report: RedactionSummary

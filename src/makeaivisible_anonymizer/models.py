from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator


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

    conversation_id: str = Field(min_length=1, max_length=128)
    messages: list[ConversationMessage] = Field(min_length=1, max_length=1_000)


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
    conversation_id: str
    messages: list[ConversationMessage]
    redaction_report: RedactionSummary

from uuid import UUID

from fastapi.testclient import TestClient

from makeaivisible_anonymizer.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}


def test_anonymizes_synthetic_conversation_without_echoing_values() -> None:
    sensitive_values = (
        "maya@example.org",
        "+1 604-555-0199",
        "https://example.org/profile/maya",
        "@maya_student",
        "user_id: abc_12345",
    )
    response = client.post(
        "/anonymize",
        json={
            "messages": [
                {"role": "user", "content": f"Email me at {sensitive_values[0]}."},
                {
                    "role": "assistant",
                    "content": "Contact " + ", ".join(sensitive_values[1:]),
                },
            ],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    serialized = response.text
    assert payload["schema_version"] == "0.1.0"
    UUID(payload["conversation_id"])
    assert payload["redaction_report"]["total"] == 5
    assert payload["redaction_report"]["by_type"] == {
        "ACCOUNT_ID": 1,
        "EMAIL": 1,
        "PHONE": 1,
        "URL": 1,
        "USERNAME": 1,
    }
    for value in sensitive_values:
        assert value not in serialized


def test_replacements_are_stable_within_a_request() -> None:
    response = client.post(
        "/anonymize",
        json={
            "messages": [
                {"role": "user", "content": "First: a@example.org"},
                {"role": "user", "content": "Second: b@example.org"},
            ],
        },
    )

    assert response.status_code == 200
    messages = response.json()["messages"]
    assert messages[0]["content"] == "First: [EMAIL_1]"
    assert messages[1]["content"] == "Second: [EMAIL_2]"


def test_generates_a_new_opaque_id_for_each_request() -> None:
    request = {"messages": [{"role": "user", "content": "hello"}]}

    first = client.post("/anonymize", json=request)
    second = client.post("/anonymize", json=request)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["conversation_id"] != second.json()["conversation_id"]


def test_rejects_blank_messages_and_caller_supplied_identifiers() -> None:
    blank = client.post(
        "/anonymize",
        json={"messages": [{"role": "user", "content": "   "}]},
    )
    supplied_identifier = client.post(
        "/anonymize",
        json={
            "conversation_id": "provider-account-123",
            "messages": [{"role": "user", "content": "hello"}],
        },
    )

    assert blank.status_code == 422
    assert supplied_identifier.status_code == 422


def test_rejects_requests_over_the_aggregate_content_limit() -> None:
    response = client.post(
        "/anonymize",
        json={"messages": [{"role": "user", "content": "x" * 50_000} for _ in range(21)]},
    )

    assert response.status_code == 422
    assert "total message content must not exceed 1000000 characters" in response.text


def test_rejects_oversized_http_body_before_parsing() -> None:
    response = client.post(
        "/anonymize",
        content=b"x" * 5_000_001,
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 413
    assert response.json() == {"detail": "request body too large"}


def test_rejects_oversized_stream_without_content_length() -> None:
    def chunks():
        for _ in range(6):
            yield b"x" * 1_000_000

    response = client.post(
        "/anonymize",
        content=chunks(),
        headers={"content-type": "application/json"},
    )

    assert response.status_code == 413

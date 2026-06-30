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
            "conversation_id": "synthetic-demo-1",
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
            "conversation_id": "synthetic-demo-2",
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


def test_rejects_blank_messages_and_unknown_fields() -> None:
    blank = client.post(
        "/anonymize",
        json={"conversation_id": "bad", "messages": [{"role": "user", "content": "   "}]},
    )
    unknown = client.post(
        "/anonymize",
        json={
            "conversation_id": "bad",
            "messages": [{"role": "user", "content": "hello", "raw_name": "not allowed"}],
        },
    )

    assert blank.status_code == 422
    assert unknown.status_code == 422

# Anonymization Examples

This folder contains synthetic examples only.

- `request.json`: a sample `/anonymize` request for local testing.
- `challenge_backlog.json`: editable notes for the 12 MVP challenge areas.

Run the service locally, then submit the example:

```bash
curl -s http://127.0.0.1:8000/anonymize \
  -H 'content-type: application/json' \
  --data @examples/request.json
```

Do not place real contributor exports in this folder.

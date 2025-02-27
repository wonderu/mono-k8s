# mono-k8s


```bash
curl -X POST http://localhost:8001/events/ \
  -H "Content-Type: application/json" \
  -d '{"name": "user_signup", "data": {"user_id": "12345", "email": "user@example.com"}}'

```

```bash
curl http://localhost:8002/events/

```
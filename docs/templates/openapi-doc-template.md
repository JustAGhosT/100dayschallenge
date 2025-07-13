# Cognitive Mesh OpenAPI-First Documentation Template

**API Name**: [Service / Capability Name]  
**Version**: v1.0  
**Stage**: [alpha | beta | stable | deprecated]  
**Mesh Layer**: [Foundation / Reasoning / …]  
**Skill Pack**: [Linked Skill Pack]  
**PRD Reference**: [Linked PRD]  
**Owner**: [Team / Contact]  
**Last Updated**: [Date]

---

## TL;DR
One-paragraph elevator pitch of what this API does, who should use it, and the primary value it delivers across the mesh.

---

## 1. Quick Start

1. `curl -X POST https://api.mesh.company.com/v1/auth -d '{"client_id":"YOUR_ID","client_secret":"YOUR_SECRET"}'`
2. `curl -H "Authorization: Bearer $TOKEN" https://api.mesh.company.com/v1/{{resource}}`

```bash
# Example minimal call
curl -H "Authorization: Bearer $TOKEN" \ 
     -H "Content-Type: application/json" \ 
     -d '{"input":"hello"}' \ 
     https://api.mesh.company.com/v1/reasoning/analyze
```

---

## 2. Base Information

| Item | Value |
|------|-------|
| Base URL | `https://api.mesh.company.com/v1` |
| OpenAPI Spec | `/openapi.yaml` (JSON & YAML) |
| Rate Limit | 1,000 req/hr per API key |
| Auth | OAuth2 Client-Credentials (JWT) |
| SDKs | JS, Python, Go, Java, C#, Postman Collection |
| Changelog | `/changelog` endpoint, RSS feed |

---

## 3. OpenAPI Document Stub

```yaml
openapi: 3.1.0
info:
  title: {{API_NAME}}
  version: 1.0.0
  description: |
    {{Concise description – reference mesh layers and Skill Pack}}
  contact:
    name: API Support
    url: https://support.mesh.company.com
    email: api-support@mesh.company.com
servers:
  - url: https://api.mesh.company.com/v1
    description: Production
  - url: https://staging-api.mesh.company.com/v1
    description: Staging
security:
  - BearerAuth: []
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
      required: [code, message]
paths:
  /auth:
    post:
      summary: Obtain JWT access token
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                client_id:
                  type: string
                client_secret:
                  type: string
              required: [client_id, client_secret]
      responses:
        '200':
          description: Access token
          content:
            application/json:
              schema:
                type: object
                properties:
                  access_token: {type: string}
                  expires_in: {type: integer}
        '401':
          $ref: '#/components/responses/Unauthorized'
  /{{resource}}:
    get:
      summary: List resources
      responses:
        '200':
          description: OK
    post:
      summary: Create resource
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/{{Resource}}'
      responses:
        '201':
          description: Created
```

> **Tip**: Keep the spec in-repo, version-controlled, and CI-validated via spectral.

---

## 4. Endpoint Reference

| Endpoint | Method | Description | Auth | Mesh Layer |
|----------|--------|-------------|------|-----------|
| `/auth` | POST | Get JWT token | None | Agency |
| `/foundation/data/ingest` | POST | Ingest data | Bearer | Foundation |
| `/reasoning/analyze` | POST | Run AI analysis | Bearer | Reasoning |
| `/business/insights` | GET | Fetch insights | Bearer | Business |

### Request & Response Samples

```json
POST /reasoning/analyze
{
  "data": {
    "type": "text",
    "content": "I love Cognitives!"
  },
  "config": {"analysis_type": "sentiment"}
}

200 OK
{
  "result": {
    "sentiment": "positive",
    "confidence": 0.93
  },
  "metadata": {
    "processing_layer": "reasoning",
    "model_version": "v2.1"
  }
}
```

---

## 5. Authentication & Authorization

1. Obtain client credentials from Mesh Console → Developer Portal.
2. POST to `/auth` with credentials to receive a JWT.
3. Include `Authorization: Bearer <token>` header in subsequent calls.
4. Permissions are scoped via JWT claims (mesh_layer, org_id, scopes).

---

## 6. Error Handling

| HTTP Code | Condition | Retry? | Example |
|-----------|-----------|--------|---------|
| 400 Bad Request | Validation failed | No | Missing required field |
| 401 Unauthorized | Invalid/expired token | Refresh token | |
| 429 Too Many Requests | Rate limit exceeded | Retry-After header | |
| 5xx | Internal server error | Exponential backoff | |

```json
{
  "code": "FOUNDATION_VALIDATION_FAILED",
  "message": "Field 'data.content' is required"
}
```

---

## 7. Webhooks (Optional)

- **Event**: `analysis.completed`
- **Payload**:
```json
{
  "event": "analysis.completed",
  "analysis_id": "12345",
  "status": "SUCCESS",
  "output_uri": "s3://.../result.json"
}
```
- Retries with exponential backoff, signed with HMAC using your webhook secret.

---

## 8. SDK & Tooling

| Language | Package | Install |
|----------|---------|---------|
| JS/TS | `@mesh/sdk` | `npm install @mesh/sdk` |
| Python | `mesh-sdk` | `pip install mesh-sdk` |
| Go | `github.com/mesh/sdk-go` | `go get ...` |

---

## 9. Changelog
| Version | Date | Change | Migration |
|---------|------|--------|-----------|
| 1.0 | 2025-07-10 | Initial GA release | N/A |

---

## 10. FAQ & Support

- Ask questions in `#mesh-developer` Slack.
- Email support: api-support@mesh.company.com.
- SLA: critical bug response < 4h, general < 24h.

---

## 11. Compliance & Security Notes

- All data encrypted in transit (TLS 1.3) and at rest (AES-256).
- SOC 2 Type II, ISO 27001 compliant.
- PII redaction options in `/foundation/data/ingest`.

---

## 12. Appendices

### A. Complete OpenAPI YAML
[link or embed]

### B. Postman Collection
[link]

### C. Terraform Example for API Gateway Deployment
```hcl
module "mesh_api" {
  source  = "git::https://github.com/mesh/terraform-aws-mesh-api.git"
  api_spec = file("openapi.yaml")
  # ...
}
```

---

*End of OpenAPI-First Documentation Template*
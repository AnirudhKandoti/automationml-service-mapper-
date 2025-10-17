# AutomationML Service Mapper – Legacy API Transformation Prototype

Designed **schema-based transformations** ensuring **data integrity** and **access governance** between services.
Implements **secure validation** with JSON Schema (and XSD for XML), **policy-based field filtering** to prevent unauthorized data exposure, and a **modern API façade** (FastAPI) for legacy inputs—readily transferable to secure AI-accessible APIs.

## What this is
- A runnable prototype (no external systems required) that:
  - Accepts **legacy JSON or XML** payloads.
  - Validates against **legacy schemas** (JSON Schema / XSD).
  - Transforms to a **modern API shape** using a declarative YAML mapping.
  - Applies **governance policies** (e.g., `public` vs `internal`) to drop PII/Sensitive fields.
  - Validates the transformed output against a **modern JSON Schema**.
- You can keep this repo as a **blueprint** and swap schemas/mappings later.

## Quickstart

### 1) Python (recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export API_KEY=dev-key  # or set in your shell/profile
uvicorn aml_service_mapper.main:app --reload
```

Open: http://127.0.0.1:8000/docs

### 2) Docker
```bash
docker build -t aml-service-mapper:dev -f docker/Dockerfile .
docker run -p 8000:8000 -e API_KEY=dev-key aml-service-mapper:dev
```

### Example cURL
```bash
# JSON legacy → modern (public policy)
curl -s -X POST "http://127.0.0.1:8000/v1/transform/legacy-to-modern"   -H "Content-Type: application/json"   -H "X-API-Key: dev-key"   -H "X-Data-Policy: public"   --data @examples/requests/legacy_sample.json | jq

# XML legacy → modern (internal policy)
curl -s -X POST "http://127.0.0.1:8000/v1/transform/legacy-to-modern"   -H "Content-Type: application/xml"   -H "X-API-Key: dev-key"   -H "X-Data-Policy: internal"   --data @examples/requests/legacy_sample.xml | jq
```

## Repo layout
```
automationml-service-mapper/
├─ aml_service_mapper/
│  ├─ adapters/            # (mock) legacy client(s) if needed
│  ├─ schemas/             # JSON + XSD schemas
│  ├─ security/            # API key auth + governance config
│  ├─ transform/           # mapping engine + declarative mappings
│  ├─ utils/               # logging helpers
│  ├─ main.py              # FastAPI app
│  └─ config.py            # settings
├─ examples/               # sample requests/responses
├─ openapi/                # modern API spec (editable)
├─ tests/                  # pytest tests
├─ docker/                 # Dockerfile
├─ docs/                   # architecture & governance notes
├─ requirements.txt
├─ .gitignore
├─ .pre-commit-config.yaml
├─ Makefile
└─ LICENSE
```

## Security/Governance
- **Auth**: simple API Key via `X-API-Key` header (see `security/auth.py`).
- **Policies**: `X-Data-Policy: public|internal` controls which fields survive transformation (see `security/pii_fields.yaml`, `transform/policies.py`).

## Swapping in your domain
- Replace **legacy** schemas at `aml_service_mapper/schemas/json/legacy_*` and `aml_service_mapper/schemas/xml/*.xsd`.
- Replace **modern** schemas at `aml_service_mapper/schemas/json/modern_*`.
- Update the mapping in `aml_service_mapper/transform/mappings/legacy_to_modern.yaml`.
- Add/adjust **policy tags** for fields (e.g., `PII`, `SENSITIVE`).

---
© 2025 AutomationML Service Mapper prototype. Licensed under MIT.

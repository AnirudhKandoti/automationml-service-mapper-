
# Threat Model (Prototype)

- **Threat**: Unauthorized caller scrapes API.
  - **Control**: API key header (replace with OAuth/JWT in production).
- **Threat**: PII leakage via transformation.
  - **Control**: Policy tags + enforcement filter.
- **Threat**: Invalid legacy payload causes crashes.
  - **Control**: JSON/XSD validation before transform.
- **Threat**: Schema drift.
  - **Control**: CI tests validate mapping against schemas.

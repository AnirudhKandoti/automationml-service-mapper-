
# Data Governance Model

- Tag fields in the mapping with policy tags such as `PII`, `SENSITIVE`, `ID`, `PUBLIC`.
- A policy (sent as `X-Data-Policy`) controls what tags pass through.
- Default policies provided:
  - `public`: allows `PUBLIC`, `ID`; denies `PII`, `SENSITIVE`.
  - `internal`: allows `PUBLIC`, `ID`, `PII`; denies `SENSITIVE`.

To extend: add policies/tags in `aml_service_mapper/security/pii_fields.yaml`.

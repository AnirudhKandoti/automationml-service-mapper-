
# Architecture

- **FastAPI façade** exposes a clean modern endpoint.
- **ValidatorSuite** enforces contracts:
  - Legacy JSON (JSON Schema).
  - Legacy XML (XSD).
  - Modern output (JSON Schema).
- **TransformEngine** applies declarative mapping YAML:
  - Field copies, constants, simple type coercions.
  - **List mapping** (legacy `items[].qty` → modern `lines[].quantity`).
  - Field-level governance via policy tags (`PII`, `SENSITIVE`, etc.).
- **PolicyFilter** determines if a tag is allowed for a given policy (`public`, `internal`).

Replace schemas + mapping for your domain while keeping the engine intact.

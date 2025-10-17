
from __future__ import annotations
from fastapi import FastAPI, Request, Header, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any
import xmltodict
import os

from .config import settings
from .security.auth import require_api_key
from .transform.validators import ValidatorSuite
from .transform.engine import TransformEngine
from .transform.policies import PolicyFilter
from .utils.logging import get_logger

logger = get_logger(__name__)

BASE = os.path.dirname(__file__)

validator = ValidatorSuite()
policy_filter = PolicyFilter(os.path.join(BASE, "security/pii_fields.yaml"))
engine = TransformEngine(os.path.join(BASE, "transform/mappings/legacy_to_modern.yaml"), policy_filter)

app = FastAPI(title="AutomationML Service Mapper – Legacy API Transformation Prototype", version="0.1.1")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/v1/transform/legacy-to-modern")
async def legacy_to_modern(
    request: Request,
    x_data_policy: str = Header(default=settings.policy_default, alias="X-Data-Policy"),
    _auth: None = Depends(require_api_key),
):
    content_type = request.headers.get("content-type", "").split(";")[0].strip().lower()
    policy = (x_data_policy or settings.policy_default).strip().lower()

    # Parse & validate input
    if content_type in ("application/xml", "text/xml"):
        raw = await request.body()
        validator.validate_legacy_xml(raw)
        payload = xmltodict.parse(raw)
        payload = payload.get("LegacyOrderRequest") or payload
        # Normalize xmltodict's items shape to a list for mapping
        try:
            items = payload.get("order", {}).get("items")
            if isinstance(items, dict) and "item" in items:
                payload["order"]["items"] = items["item"]
        except Exception:
            pass
    elif content_type == "application/json":
        payload = await request.json()
        validator.validate_legacy_json(payload)
    else:
        raise HTTPException(status_code=415, detail=f"Unsupported Content-Type: {content_type}")

    # Transform
    try:
        modern = engine.legacy_to_modern(payload, policy=policy)
        validator.validate_modern_json(modern)
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        logger.exception("Transformation failed")
        raise HTTPException(status_code=500, detail="Transformation failed")

    return JSONResponse(modern)

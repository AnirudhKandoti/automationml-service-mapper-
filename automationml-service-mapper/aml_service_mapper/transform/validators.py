
from __future__ import annotations
from typing import Any, Dict
import json
import xmlschema
import jsonschema
from jsonschema import Draft202012Validator
import os

from ..utils.logging import get_logger

logger = get_logger(__name__)

BASE = os.path.dirname(os.path.dirname(__file__))

class ValidatorSuite:
    def __init__(self):
        with open(os.path.join(BASE, "schemas/json/legacy_api_request.schema.json"), "r", encoding="utf-8") as f:
            self.legacy_json_schema = json.load(f)
        with open(os.path.join(BASE, "schemas/json/modern_api_response.schema.json"), "r", encoding="utf-8") as f:
            self.modern_json_schema = json.load(f)

        self.legacy_xml_schema = xmlschema.XMLSchema(os.path.join(BASE, "schemas/xml/legacy_api_request.xsd"))
        self.json_in_validator = Draft202012Validator(self.legacy_json_schema)
        self.json_out_validator = Draft202012Validator(self.modern_json_schema)

    def validate_legacy_json(self, payload: Dict[str, Any]):
        errors = sorted(self.json_in_validator.iter_errors(payload), key=lambda e: e.path)
        if errors:
            msg = "; ".join([e.message for e in errors])
            raise ValueError(f"Legacy JSON validation failed: {msg}")

    def validate_legacy_xml(self, xml_bytes: bytes):
        try:
            self.legacy_xml_schema.validate(xml_bytes.decode("utf-8"))
        except Exception as e:
            raise ValueError(f"Legacy XML validation failed: {e}")

    def validate_modern_json(self, payload: Dict[str, Any]):
        errors = sorted(self.json_out_validator.iter_errors(payload), key=lambda e: e.path)
        if errors:
            msg = "; ".join([e.message for e in errors])
            raise ValueError(f"Modern JSON validation failed: {msg}")

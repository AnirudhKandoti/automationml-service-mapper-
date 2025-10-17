
from __future__ import annotations
from typing import Dict, List
import yaml
from ..utils.logging import get_logger

logger = get_logger(__name__)

class PolicyFilter:
    def __init__(self, policy_config_path: str):
        with open(policy_config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        self.policies: Dict[str, Dict[str, List[str]]] = cfg.get("policies", {})
        if not self.policies:
            logger.warning("No policies found in %s", policy_config_path)

    def is_allowed(self, policy_name: str, tag: str) -> bool:
        pol = self.policies.get(policy_name) or {}
        allow = set(pol.get("allow_tags") or [])
        deny = set(pol.get("deny_tags") or [])
        if tag in deny:
            return False
        if allow and tag not in allow:
            return False
        return True


from __future__ import annotations
from typing import Any, Dict, List
import yaml

from ..utils.logging import get_logger
from .policies import PolicyFilter
from .path_ops import get_by_path, set_by_path, del_by_path, coerce_type

logger = get_logger(__name__)

class TransformEngine:
    def __init__(self, mapping_path: str, policy_filter: PolicyFilter):
        with open(mapping_path, "r", encoding="utf-8") as f:
            self.mapping = yaml.safe_load(f)
        self.policy_filter = policy_filter
        logger.info("Loaded mapping from %s", mapping_path)

    def legacy_to_modern(self, payload: Dict[str, Any], policy: str) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        for rule in self.mapping.get("mappings", []):
            # Simple field copy
            if "from" in rule and "to" in rule:
                value = get_by_path(payload, rule["from"])
                if value is None:
                    continue
                transform = rule.get("transform")
                if transform:
                    value = coerce_type(value, transform)
                policy_tag = rule.get("policy_tag")
                if policy_tag and not self.policy_filter.is_allowed(policy, policy_tag):
                    continue
                set_by_path(out, rule["to"], value)
                continue

            # List mapping
            if "map" in rule:
                spec = rule["map"]
                src = get_by_path(payload, spec["from"])
                if src is None:
                    continue
                # Normalize xmltodict shape {item: [...]} to list
                if isinstance(src, dict) and "item" in src and isinstance(src["item"], list):
                    src = src["item"]
                if not isinstance(src, list):
                    continue
                mapped: List[Dict[str, Any]] = []
                for item in src:
                    new_item: Dict[str, Any] = {}
                    for m in spec.get("each", []):
                        v = item.get(m["from"])
                        if v is None:
                            continue
                        t = m.get("transform")
                        if t:
                            v = coerce_type(v, t)
                        new_item[m["to"]] = v
                    mapped.append(new_item)
                set_by_path(out, spec["to"], mapped)
                continue

            # Constants
            if "const" in rule:
                const = rule["const"]
                set_by_path(out, const["to"], const.get("value"))
                continue

            # Drop from input (optional)
            if "drop" in rule:
                drop = rule["drop"]
                if drop.get("policy_tag") and not self.policy_filter.is_allowed(policy, drop["policy_tag"]):
                    del_by_path(payload, drop.get("from", ""))
                continue

        set_by_path(out, "meta.policy_applied", policy)
        return out

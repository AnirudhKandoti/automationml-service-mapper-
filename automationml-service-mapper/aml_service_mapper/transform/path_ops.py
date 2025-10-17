
from __future__ import annotations
from typing import Any, Dict, List

def get_by_path(obj: Dict[str, Any], path: str, default=None):
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur

def set_by_path(obj: Dict[str, Any], path: str, value: Any):
    parts = path.split(".")
    cur = obj
    for p in parts[:-1]:
        if p not in cur or not isinstance(cur[p], dict):
            cur[p] = {}
        cur = cur[p]
    cur[parts[-1]] = value

def del_by_path(obj: Dict[str, Any], path: str):
    parts = path.split(".")
    cur = obj
    for p in parts[:-1]:
        cur = cur.get(p, {})
        if not isinstance(cur, dict):
            return
    cur.pop(parts[-1], None)

def coerce_type(value: Any, transform: str):
    if transform == "float":
        try:
            return float(value)
        except Exception:
            return value
    if transform == "int":
        try:
            return int(value)
        except Exception:
            return value
    return value

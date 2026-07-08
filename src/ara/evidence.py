from __future__ import annotations

import hashlib
from typing import Iterable
from .models import Case, Evidence


def stable_id(prefix: str, *parts: str) -> str:
    data = "|".join(parts).encode("utf-8", errors="ignore")
    return f"{prefix}_{hashlib.sha1(data).hexdigest()[:10]}"


def add_evidence(case: Case, evidence: Evidence | Iterable[Evidence]) -> Case:
    items = [evidence] if isinstance(evidence, Evidence) else list(evidence)
    existing = {e.id for e in case.evidence}
    for item in items:
        if item.id not in existing:
            case.evidence.append(item)
            existing.add(item.id)
    return case


def merge_tool_result(case: Case, result) -> Case:
    case.artifacts.extend(result.artifacts)
    add_evidence(case, result.evidence)
    case.findings.extend(result.findings)
    case.next_actions.extend(result.next_actions)
    return case

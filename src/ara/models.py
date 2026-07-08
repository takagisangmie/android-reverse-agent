from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Literal
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    pending = "pending"
    running = "running"
    success = "success"
    failed = "failed"
    skipped = "skipped"


class EvidenceKind(str, Enum):
    manifest = "manifest"
    java = "java"
    native = "native"
    network = "network"
    trace = "trace"
    crypto = "crypto"
    vmp = "vmp"
    solver = "solver"
    report = "report"
    unknown = "unknown"


class Artifact(BaseModel):
    name: str
    path: str
    kind: str = "file"
    description: str = ""


class Evidence(BaseModel):
    id: str
    kind: EvidenceKind = EvidenceKind.unknown
    source: str
    location: str = ""
    summary: str
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    raw: str | None = None
    tags: list[str] = Field(default_factory=list)


class Finding(BaseModel):
    id: str
    title: str
    category: str
    summary: str
    evidence_ids: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    severity: Literal["info", "low", "medium", "high"] = "info"
    next_actions: list[str] = Field(default_factory=list)


class NextAction(BaseModel):
    id: str
    title: str
    action_type: str
    reason: str
    inputs: dict[str, Any] = Field(default_factory=dict)
    status: TaskStatus = TaskStatus.pending


class Case(BaseModel):
    case_id: str
    apk_path: str
    workdir: str
    package_name: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: TaskStatus = TaskStatus.pending
    artifacts: list[Artifact] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    next_actions: list[NextAction] = Field(default_factory=list)

    def save(self, path: str | Path) -> None:
        Path(path).write_text(self.model_dump_json(indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "Case":
        return cls.model_validate_json(Path(path).read_text(encoding="utf-8"))


class ToolResult(BaseModel):
    artifacts: list[Artifact] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    findings: list[Finding] = Field(default_factory=list)
    next_actions: list[NextAction] = Field(default_factory=list)
    ok: bool = True
    error: str | None = None

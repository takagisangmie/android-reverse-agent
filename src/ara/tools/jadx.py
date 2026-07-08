from __future__ import annotations

from ..models import ToolResult


class JadxAdapter:
    """Adapter placeholder for jadx."""

    name = "jadx"

    def available(self) -> bool:
        return False

    def run(self, *args, **kwargs) -> ToolResult:
        return ToolResult(ok=False, error="jadx adapter is not implemented yet. Add command/API binding here.")

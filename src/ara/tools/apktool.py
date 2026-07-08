from __future__ import annotations

from ..models import ToolResult


class ApktoolAdapter:
    """Adapter placeholder for apktool."""

    name = "apktool"

    def available(self) -> bool:
        return False

    def run(self, *args, **kwargs) -> ToolResult:
        return ToolResult(ok=False, error="apktool adapter is not implemented yet. Add command/API binding here.")

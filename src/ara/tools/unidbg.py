from __future__ import annotations

from ..models import ToolResult


class UnidbgAdapter:
    """Adapter placeholder for unidbg."""

    name = "unidbg"

    def available(self) -> bool:
        return False

    def run(self, *args, **kwargs) -> ToolResult:
        return ToolResult(ok=False, error="unidbg adapter is not implemented yet. Add command/API binding here.")

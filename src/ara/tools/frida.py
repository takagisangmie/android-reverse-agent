from __future__ import annotations

from ..models import ToolResult


class FridaAdapter:
    """Adapter placeholder for frida."""

    name = "frida"

    def available(self) -> bool:
        return False

    def run(self, *args, **kwargs) -> ToolResult:
        return ToolResult(ok=False, error="frida adapter is not implemented yet. Add command/API binding here.")

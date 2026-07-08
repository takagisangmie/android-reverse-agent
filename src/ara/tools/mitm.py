from __future__ import annotations

from ..models import ToolResult


class MitmProxyAdapter:
    """Adapter placeholder for mitmproxy."""

    name = "mitmproxy"

    def available(self) -> bool:
        return False

    def run(self, *args, **kwargs) -> ToolResult:
        return ToolResult(ok=False, error="mitmproxy adapter is not implemented yet. Add command/API binding here.")

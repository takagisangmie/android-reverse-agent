from __future__ import annotations

from ..models import ToolResult


class IdaMcpAdapter:
    """Adapter placeholder for IDA MCP."""

    name = "IDA MCP"

    def available(self) -> bool:
        return False

    def run(self, *args, **kwargs) -> ToolResult:
        return ToolResult(ok=False, error="IDA MCP adapter is not implemented yet. Add command/API binding here.")

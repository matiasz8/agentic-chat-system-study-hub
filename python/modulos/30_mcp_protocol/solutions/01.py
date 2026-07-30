#!/usr/bin/env python3
import json
from typing import Any


class SimpleMCPServer:
    def __init__(self) -> None:
        self.tools = [
            {
                "name": "ping",
                "description": "Responde pong para validar conectividad.",
                "inputSchema": {"type": "object", "properties": {}},
            }
        ]

    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        method = request["method"]
        request_id = request.get("id")

        try:
            if method == "initialize":
                result = {
                    "protocolVersion": request.get("params", {}).get(
                        "protocolVersion", "2024-11-05"
                    ),
                    "serverInfo": {"name": "simple-mcp-server", "version": "1.0.0"},
                    "capabilities": {"tools": {}},
                }
            elif method == "tools/list":
                result = {"tools": self.tools}
            else:
                raise KeyError(f"Método no soportado: {method}")
            return {"jsonrpc": "2.0", "id": request_id, "result": result}
        except Exception as error:  # noqa: BLE001
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": str(error)},
            }


def main() -> None:
    server = SimpleMCPServer()
    demo_requests = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2024-11-05"},
        },
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "unknown/method"},
    ]

    print("=== Solución 01: servidor MCP mínimo ===")
    for request in demo_requests:
        print("➡️", json.dumps(request, ensure_ascii=False))
        print("⬅️", json.dumps(server.handle(request), indent=2, ensure_ascii=False))
        print("-" * 60)


if __name__ == "__main__":
    main()

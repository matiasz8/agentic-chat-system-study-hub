#!/usr/bin/env python3
"""Solución al ejercicio intermedio de dispatcher de herramientas."""

from __future__ import annotations

import time
from collections.abc import Callable

ToolHandler = Callable[[dict[str, str]], dict[str, str]]


def search_docs(payload: dict[str, str]) -> dict[str, str]:
    topic = payload.get("topic", "general")
    return {"answer": f"Guía encontrada para {topic}"}


def dispatch_tool(
    name: str, payload: dict[str, str], registry: dict[str, ToolHandler]
) -> dict[str, str]:
    started = time.perf_counter()
    handler = registry.get(name)
    if handler is None:
        return {
            "tool": name,
            "status": "error",
            "result": "tool no registrada",
            "duration_ms": "0.00",
        }

    result = handler(payload)
    duration_ms = (time.perf_counter() - started) * 1000
    return {
        "tool": name,
        "status": "ok",
        "result": str(result),
        "duration_ms": f"{duration_ms:.2f}",
    }


def main() -> None:
    registry = {"search_docs": search_docs}
    print("=== Solución 2 ===")
    print(dispatch_tool("search_docs", {"topic": "streaming"}, registry))
    print(dispatch_tool("missing_tool", {}, registry))


if __name__ == "__main__":
    main()

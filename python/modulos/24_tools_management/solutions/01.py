#!/usr/bin/env python3
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class Tool:
    name: str
    description: str
    schema: dict[str, Any]
    func: Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def invoke(self, name: str, payload: dict[str, Any]) -> Any:
        return self.tools[name].func(**payload)


def hello(name: str) -> str:
    return f"Hola, {name}"


def main() -> None:
    registry = ToolRegistry()
    registry.register(Tool("hello", "Saludo simple", {"required": ["name"]}, hello))
    print(registry.invoke("hello", {"name": "AgentCore"}))
    print(list(registry.tools))


if __name__ == "__main__":
    main()

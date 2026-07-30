#!/usr/bin/env python3
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

TYPE_MAP: dict[str, tuple[type, ...]] = {
    "string": (str,),
    "integer": (int,),
}


@dataclass
class Tool:
    name: str
    schema: dict[str, Any]
    func: Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self.tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def invoke(self, name: str, payload: dict[str, Any]) -> Any:
        tool = self.tools[name]
        self._validate(payload, tool.schema)
        return tool.func(**payload)

    def _validate(self, payload: dict[str, Any], schema: dict[str, Any]) -> None:
        for field in schema.get("required", []):
            if field not in payload:
                raise ValueError(f"Falta {field}")
        for field, rules in schema.get("properties", {}).items():
            if field not in payload:
                continue
            if not isinstance(payload[field], TYPE_MAP[rules["type"]]):
                raise ValueError(f"{field} debe ser {rules['type']}")
            if "minimum" in rules and payload[field] < rules["minimum"]:
                raise ValueError(f"{field} debe ser >= {rules['minimum']}")


def repeat_text(text: str, times: int) -> str:
    return " ".join([text] * times)


def main() -> None:
    registry = ToolRegistry()
    registry.register(
        Tool(
            "repeat_text",
            {
                "required": ["text", "times"],
                "properties": {
                    "text": {"type": "string"},
                    "times": {"type": "integer", "minimum": 1},
                },
            },
            repeat_text,
        )
    )
    print(registry.invoke("repeat_text", {"text": "tool", "times": 3}))
    try:
        registry.invoke("repeat_text", {"text": "tool", "times": 0})
    except ValueError as exc:
        print("error esperado ->", exc)


if __name__ == "__main__":
    main()

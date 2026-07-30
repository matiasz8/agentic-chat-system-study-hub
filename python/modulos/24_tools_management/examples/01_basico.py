#!/usr/bin/env python3
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class ToolDefinition:
    name: str
    description: str
    schema: dict[str, Any]
    func: Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(
        self, name: str, description: str, schema: dict[str, Any]
    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self._tools[name] = ToolDefinition(name, description, schema, func)
            return func

        return decorator

    def describe(self) -> list[str]:
        return [
            f"- {tool.name}: {tool.description} | schema={tool.schema}"
            for tool in self._tools.values()
        ]

    def invoke(self, name: str, **payload: Any) -> Any:
        return self._tools[name].func(**payload)


registry = ToolRegistry()


@registry.register(
    name="search_docs",
    description="Busca coincidencias simples en una base documental pequeña",
    schema={"type": "object", "required": ["query"], "properties": {"query": {"type": "string"}}},
)
def search_docs(query: str) -> list[str]:
    docs = ["Guía de onboarding", "Política de incidentes", "Checklist de despliegue"]
    return [doc for doc in docs if query.lower() in doc.lower()]


@registry.register(
    name="estimate_tokens",
    description="Cuenta palabras como aproximación rápida de tokens",
    schema={"type": "object", "required": ["text"], "properties": {"text": {"type": "string"}}},
)
def estimate_tokens(text: str) -> int:
    return len(text.split())


def main() -> None:
    print("== Catálogo de tools ==")
    for line in registry.describe():
        print(line)

    print("\n== Invocaciones ==")
    print("search_docs ->", registry.invoke("search_docs", query="política"))
    print("estimate_tokens ->", registry.invoke("estimate_tokens", text="uno dos tres cuatro"))


if __name__ == "__main__":
    main()

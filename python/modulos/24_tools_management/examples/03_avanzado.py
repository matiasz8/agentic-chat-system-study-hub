#!/usr/bin/env python3
from __future__ import annotations

import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeoutError
from copy import deepcopy
from dataclasses import dataclass
from typing import Any


@dataclass
class ToolVersion:
    name: str
    version: str
    category: str
    schema: dict[str, Any]
    timeout_seconds: float
    func: Callable[..., Any]


@dataclass
class AuditEntry:
    tool_name: str
    version: str
    status: str
    detail: str


class ToolManager:
    def __init__(self) -> None:
        self._tools: dict[str, dict[str, ToolVersion]] = {}
        self.audit: list[AuditEntry] = []

    def register(self, tool: ToolVersion) -> None:
        self._tools.setdefault(tool.name, {})[tool.version] = tool

    def categories(self) -> dict[str, list[str]]:
        grouped: dict[str, list[str]] = {}
        for versions in self._tools.values():
            latest = sorted(versions.values(), key=lambda item: item.version)[-1]
            grouped.setdefault(latest.category, []).append(f"{latest.name}@{latest.version}")
        return grouped

    def invoke(self, name: str, payload: dict[str, Any], version: str | None = None) -> Any:
        tool = self._resolve(name, version)
        self._validate(payload, tool.schema)
        sandbox_payload = deepcopy(payload)
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(tool.func, **sandbox_payload)
            try:
                result = future.result(timeout=tool.timeout_seconds)
                self.audit.append(AuditEntry(tool.name, tool.version, "ok", repr(result)))
                return result
            except FuturesTimeoutError:
                self.audit.append(
                    AuditEntry(tool.name, tool.version, "timeout", "Se excedió el timeout")
                )
                return {"status": "timeout", "tool": tool.name, "version": tool.version}
            except Exception as exc:
                self.audit.append(AuditEntry(tool.name, tool.version, "error", str(exc)))
                return {"status": "error", "detail": str(exc)}

    def _resolve(self, name: str, version: str | None) -> ToolVersion:
        versions = self._tools[name]
        if version is not None:
            return versions[version]
        return sorted(versions.values(), key=lambda item: item.version)[-1]

    def _validate(self, payload: dict[str, Any], schema: dict[str, Any]) -> None:
        for field in schema.get("required", []):
            if field not in payload:
                raise ValueError(f"Falta {field}")


def summarize_v1(text: str) -> str:
    return " ".join(text.split()[:5])


def summarize_v2(text: str) -> str:
    words = text.split()
    return f"Resumen ({len(words)} palabras): " + " ".join(words[:8])


def slow_lookup(query: str) -> str:
    time.sleep(0.2)
    return f"Resultado tardío para {query}"


def main() -> None:
    manager = ToolManager()
    manager.register(
        ToolVersion("summarize", "1.0.0", "nlp", {"required": ["text"]}, 1.0, summarize_v1)
    )
    manager.register(
        ToolVersion("summarize", "2.0.0", "nlp", {"required": ["text"]}, 1.0, summarize_v2)
    )
    manager.register(
        ToolVersion("slow_lookup", "1.0.0", "io", {"required": ["query"]}, 0.05, slow_lookup)
    )

    print("== Categorías y tools activas ==")
    for category, tools in manager.categories().items():
        print(category, "->", tools)

    print("\n== Hot reload simulado (usa la versión más nueva) ==")
    print(
        manager.invoke(
            "summarize", {"text": "las tools necesitan validación, versionado y observabilidad"}
        )
    )

    print("\n== Invocación fija a versión anterior ==")
    print(manager.invoke("summarize", {"text": "texto corto para comparar"}, version="1.0.0"))

    print("\n== Timeout controlado ==")
    print(manager.invoke("slow_lookup", {"query": "politicas"}))

    print("\n== Auditoría ==")
    for entry in manager.audit:
        print(entry)


if __name__ == "__main__":
    main()

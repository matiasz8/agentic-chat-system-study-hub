#!/usr/bin/env python3
from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any


@dataclass
class AuditRecord:
    timestamp: str
    agent_id: str
    tool_name: str
    inputs: dict[str, Any]
    output: Any
    success: bool
    error: str | None = None


class AuditLogger:
    def __init__(self) -> None:
        self.records: list[AuditRecord] = []

    def invoke(
        self, agent_id: str, tool_name: str, tool_func: Callable[..., Any], **kwargs: Any
    ) -> Any:
        timestamp = datetime.now(UTC).isoformat()
        try:
            result = tool_func(**kwargs)
            record = AuditRecord(timestamp, agent_id, tool_name, kwargs, result, True)
            self.records.append(record)
            return result
        except Exception as exc:
            record = AuditRecord(timestamp, agent_id, tool_name, kwargs, None, False, str(exc))
            self.records.append(record)
            raise


def search_kb(query: str, limit: int = 2) -> list[str]:
    corpus = [
        "Politica de devoluciones para productos digitales",
        "Guia de alta de clientes enterprise",
        "Runbook de incidentes de finanzas",
    ]
    return [item for item in corpus if query.lower() in item.lower()][:limit]


def summarize_text(text: str) -> str:
    if not text.strip():
        raise ValueError("Se esperaba texto no vacío")
    words = text.split()
    return " ".join(words[:8]) + ("..." if len(words) > 8 else "")


def main() -> None:
    logger = AuditLogger()

    print("== Invocaciones auditadas ==")
    kb_result = logger.invoke(
        agent_id="agent-support",
        tool_name="search_kb",
        tool_func=search_kb,
        query="politica",
    )
    print("search_kb ->", kb_result)

    summary = logger.invoke(
        agent_id="agent-support",
        tool_name="summarize_text",
        tool_func=summarize_text,
        text="Los agentes deben registrar cada decisión importante para trazabilidad.",
    )
    print("summarize_text ->", summary)

    try:
        logger.invoke(
            agent_id="agent-support",
            tool_name="summarize_text",
            tool_func=summarize_text,
            text="   ",
        )
    except ValueError as exc:
        print("error controlado ->", exc)

    print("\n== Audit trail estructurado ==")
    for record in logger.records:
        print(json.dumps(asdict(record), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

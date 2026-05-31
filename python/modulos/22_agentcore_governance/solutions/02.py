#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any, Callable, Dict, List
import json


@dataclass
class AuditRecord:
    timestamp: str
    agent_id: str
    tool_name: str
    inputs: Dict[str, Any]
    output: Any
    success: bool
    error: str | None = None


class AuditLogger:
    def __init__(self) -> None:
        self.records: List[AuditRecord] = []

    def call(self, agent_id: str, tool_name: str, func: Callable[..., Any], **payload: Any) -> Any:
        timestamp = datetime.now(UTC).isoformat()
        try:
            output = func(**payload)
            self.records.append(AuditRecord(timestamp, agent_id, tool_name, payload, output, True))
            return output
        except Exception as exc:
            self.records.append(AuditRecord(timestamp, agent_id, tool_name, payload, None, False, str(exc)))
            raise


def uppercase_message(message: str) -> str:
    if not message:
        raise ValueError("message no puede estar vacío")
    return message.upper()


def main() -> None:
    logger = AuditLogger()
    print(logger.call("agent-demo", "uppercase_message", uppercase_message, message="hola gobernanza"))

    try:
        logger.call("agent-demo", "uppercase_message", uppercase_message, message="")
    except ValueError as exc:
        print("error esperado ->", exc)

    print("\n== Registros ==")
    for record in logger.records:
        print(json.dumps(asdict(record), ensure_ascii=False))


if __name__ == "__main__":
    main()

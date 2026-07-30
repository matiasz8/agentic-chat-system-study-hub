#!/usr/bin/env python3
from __future__ import annotations

import time
from collections import defaultdict, deque
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class AuditEntry:
    agent_id: str
    tool_name: str
    decision: str
    detail: str


class GovernanceEngine:
    def __init__(self, policies: dict[str, set[str]], limit: int, window_seconds: int) -> None:
        self.policies = policies
        self.limit = limit
        self.window_seconds = window_seconds
        self.calls: dict[str, deque[float]] = defaultdict(deque)
        self.audit: list[AuditEntry] = []

    def invoke(
        self, agent_id: str, tool_name: str, func: Callable[..., Any], **payload: Any
    ) -> Any:
        if tool_name not in self.policies.get(agent_id, set()):
            self.audit.append(AuditEntry(agent_id, tool_name, "deny", "política"))
            return {"status": "denied", "reason": "política"}

        if not self._allow_rate(agent_id):
            self.audit.append(AuditEntry(agent_id, tool_name, "deny", "rate-limit"))
            return {"status": "denied", "reason": "rate-limit"}

        result = func(**payload)
        self.audit.append(AuditEntry(agent_id, tool_name, "allow", repr(result)))
        return {"status": "allowed", "result": result}

    def _allow_rate(self, agent_id: str) -> bool:
        now = time.time()
        bucket = self.calls[agent_id]
        while bucket and now - bucket[0] > self.window_seconds:
            bucket.popleft()
        if len(bucket) >= self.limit:
            return False
        bucket.append(now)
        return True


def search_kb(query: str) -> str:
    return f"Resultado para: {query}"


def main() -> None:
    engine = GovernanceEngine(
        policies={"agent-a": {"search_kb"}},
        limit=2,
        window_seconds=60,
    )

    print(engine.invoke("agent-a", "search_kb", search_kb, query="cedar"))
    print(engine.invoke("agent-a", "delete_user", search_kb, query="no aplica"))
    print(engine.invoke("agent-a", "search_kb", search_kb, query="agentcore"))
    print(engine.invoke("agent-a", "search_kb", search_kb, query="tooling"))

    print("\n== Auditoría ==")
    for entry in engine.audit:
        print(entry)


if __name__ == "__main__":
    main()

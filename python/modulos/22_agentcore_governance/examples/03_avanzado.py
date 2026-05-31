#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Any, Callable, Deque, Dict, List
import json
import time


@dataclass
class AuditEvent:
    timestamp: str
    agent_id: str
    tool_name: str
    decision: str
    detail: str


class AuditTrail:
    def __init__(self) -> None:
        self.events: List[AuditEvent] = []

    def log(self, agent_id: str, tool_name: str, decision: str, detail: str) -> None:
        self.events.append(
            AuditEvent(
                timestamp=datetime.now(UTC).isoformat(),
                agent_id=agent_id,
                tool_name=tool_name,
                decision=decision,
                detail=detail,
            )
        )


class RateLimiter:
    def __init__(self, max_calls: int, window_seconds: int) -> None:
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls: Dict[str, Deque[float]] = defaultdict(deque)

    def allow(self, agent_id: str) -> bool:
        now = time.time()
        queue = self.calls[agent_id]
        while queue and now - queue[0] > self.window_seconds:
            queue.popleft()
        if len(queue) >= self.max_calls:
            return False
        queue.append(now)
        return True


class GovernanceEngine:
    def __init__(
        self,
        tools: Dict[str, Callable[..., Any]],
        allowed_tools: Dict[str, set[str]],
        max_calls: int,
        window_seconds: int,
        alert_threshold: int = 2,
    ) -> None:
        self.tools = tools
        self.allowed_tools = allowed_tools
        self.rate_limiter = RateLimiter(max_calls=max_calls, window_seconds=window_seconds)
        self.audit = AuditTrail()
        self.alert_threshold = alert_threshold
        self.denials: Dict[str, int] = defaultdict(int)
        self.alerts: List[str] = []

    def invoke(self, agent_id: str, tool_name: str, **payload: Any) -> Dict[str, Any]:
        if tool_name not in self.allowed_tools.get(agent_id, set()):
            return self._deny(agent_id, tool_name, "deny", "Bloqueado por política")

        if not self.rate_limiter.allow(agent_id):
            return self._deny(agent_id, tool_name, "throttle", "Rate limit excedido")

        try:
            result = self.tools[tool_name](**payload)
            self.audit.log(agent_id, tool_name, "allow", f"Resultado: {result!r}")
            return {"status": "allowed", "result": result}
        except Exception as exc:
            self.audit.log(agent_id, tool_name, "error", str(exc))
            return {"status": "error", "error": str(exc)}

    def _deny(self, agent_id: str, tool_name: str, decision: str, detail: str) -> Dict[str, Any]:
        self.denials[agent_id] += 1
        self.audit.log(agent_id, tool_name, decision, detail)
        if self.denials[agent_id] >= self.alert_threshold:
            alert = (
                f"ALERTA: {agent_id} alcanzó {self.denials[agent_id]} eventos de denegación "
                f"en la ventana actual"
            )
            if alert not in self.alerts:
                self.alerts.append(alert)
        return {"status": "denied", "reason": detail}


def search_kb(query: str) -> List[str]:
    return [f"Documento relevante sobre '{query}'", "Checklist de seguridad"]


def update_ticket(ticket_id: str, status: str) -> str:
    return f"Ticket {ticket_id} actualizado a {status}"


def delete_ticket(ticket_id: str) -> str:
    return f"Ticket {ticket_id} eliminado"


def main() -> None:
    engine = GovernanceEngine(
        tools={
            "search_kb": search_kb,
            "update_ticket": update_ticket,
            "delete_ticket": delete_ticket,
        },
        allowed_tools={
            "agent-analyst": {"search_kb", "update_ticket"},
            "agent-admin": {"search_kb", "update_ticket", "delete_ticket"},
        },
        max_calls=2,
        window_seconds=30,
        alert_threshold=2,
    )

    calls = [
        ("agent-analyst", "search_kb", {"query": "controles de acceso"}),
        ("agent-analyst", "delete_ticket", {"ticket_id": "INC-100"}),
        ("agent-analyst", "update_ticket", {"ticket_id": "INC-100", "status": "review"}),
        ("agent-analyst", "search_kb", {"query": "trazabilidad"}),
        ("agent-admin", "delete_ticket", {"ticket_id": "INC-200"}),
    ]

    print("== Decisiones del motor de gobernanza ==")
    for agent_id, tool_name, payload in calls:
        outcome = engine.invoke(agent_id=agent_id, tool_name=tool_name, **payload)
        print(f"{agent_id}.{tool_name} -> {outcome}")

    print("\n== Alertas ==")
    for alert in engine.alerts or ["Sin alertas"]:
        print(alert)

    print("\n== Audit trail ==")
    for event in engine.audit.events:
        print(json.dumps(asdict(event), ensure_ascii=False))


if __name__ == "__main__":
    main()

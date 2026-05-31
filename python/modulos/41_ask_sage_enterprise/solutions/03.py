#!/usr/bin/env python3
"""Solución del ejercicio 3 del módulo Ask Sage Enterprise."""

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class AuditEvent:
    tenant_id: str
    user_id: str
    question: str
    outcome: str
    timestamp: str


class AuditLogger:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def record(self, tenant_id: str, user_id: str, question: str, outcome: str) -> None:
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        self.events.append(AuditEvent(tenant_id, user_id, question, outcome, timestamp))


class UsageAnalytics:
    def __init__(self, events: list[AuditEvent]) -> None:
        self.events = events

    def tenant_stats(self) -> Counter:
        return Counter(event.tenant_id for event in self.events)

    def user_stats(self) -> Counter:
        return Counter(event.user_id for event in self.events)

    def anomalies(self, threshold: int) -> list[str]:
        return [user for user, count in self.user_stats().items() if count > threshold]


def main() -> None:
    logger = AuditLogger()
    for user_id in ["ana", "ana", "ana", "leo"]:
        logger.record("acme", user_id, "¿Estado del SLA?", "ok")
    analytics = UsageAnalytics(logger.events)
    print("=== Solución 3 ===")
    print("Por tenant:", dict(analytics.tenant_stats()))
    print("Por usuario:", dict(analytics.user_stats()))
    print("Anomalías:", analytics.anomalies(threshold=2))


if __name__ == "__main__":
    main()

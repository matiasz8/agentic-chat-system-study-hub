#!/usr/bin/env python3
"""Simulación avanzada de Ask Sage Enterprise."""

from collections import Counter, deque
from dataclasses import dataclass
from datetime import UTC, datetime

ROLE_PERMISSIONS = {
    "admin": {"read_public", "read_restricted", "audit"},
    "viewer": {"read_public"},
}


@dataclass
class User:
    user_id: str
    tenant_id: str
    role: str


@dataclass
class Document:
    tenant_id: str
    title: str
    content: str
    permission: str


class AuditLogger:
    def __init__(self) -> None:
        self.events: list[dict[str, str]] = []

    def record(self, tenant_id: str, user_id: str, question: str, outcome: str) -> None:
        self.events.append(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "tenant_id": tenant_id,
                "user_id": user_id,
                "question": question,
                "outcome": outcome,
            }
        )


class UsageAnalytics:
    def __init__(self, events: list[dict[str, str]]) -> None:
        self.events = events

    def summary(self) -> dict[str, Counter]:
        return {
            "per_tenant": Counter(event["tenant_id"] for event in self.events),
            "per_user": Counter(event["user_id"] for event in self.events),
        }


class CircuitBreaker:
    def __init__(self, threshold: int) -> None:
        self.threshold = threshold
        self.failures = 0
        self.state = "closed"

    def call(self, should_fail: bool) -> str:
        if self.state == "open":
            return "Respuesta degradada: proveedor LLM aislado"
        if should_fail:
            self.failures += 1
            if self.failures >= self.threshold:
                self.state = "open"
            return "Error al consultar el proveedor LLM"
        self.failures = 0
        return "Respuesta enterprise generada correctamente"


def can_access(user: User, document: Document) -> bool:
    return user.tenant_id == document.tenant_id and document.permission in ROLE_PERMISSIONS.get(
        user.role, set()
    )


def retrieve(question: str, user: User, documents: list[Document]) -> list[Document]:
    tokens = [token.lower() for token in question.split() if len(token) > 3]
    ranked: list[tuple[int, Document]] = []
    for document in documents:
        if not can_access(user, document):
            continue
        score = sum(token in document.content.lower() for token in tokens)
        if score:
            ranked.append((score, document))
    return [doc for _, doc in sorted(ranked, reverse=True)]


def main() -> None:
    documents = [
        Document(
            "acme", "Guía pública", "El soporte se atiende por portal interno.", "read_public"
        ),
        Document(
            "acme",
            "Plan de auditoría",
            "Las revisiones trimestrales cubren accesos privilegiados y proveedores.",
            "read_restricted",
        ),
    ]
    user = User("sofia", "acme", "admin")
    audit = AuditLogger()
    breaker = CircuitBreaker(threshold=2)
    questions = deque(
        [
            ("¿Qué cubren las revisiones trimestrales?", False),
            ("¿Qué cubren las revisiones trimestrales?", True),
            ("¿Qué cubren las revisiones trimestrales?", True),
        ]
    )

    print("=== Ask Sage Enterprise · Avanzado ===")
    while questions:
        question, should_fail = questions.popleft()
        results = retrieve(question, user, documents)
        llm_result = breaker.call(should_fail)
        outcome = llm_result if results else "Sin contexto autorizado"
        audit.record(user.tenant_id, user.user_id, question, outcome)
        print(f"Pregunta: {question}")
        print(f"Contexto autorizado: {[doc.title for doc in results]}")
        print(f"Circuit breaker: {breaker.state}")
        print(f"Resultado: {outcome}\n")

    summary = UsageAnalytics(audit.events).summary()
    print("Resumen administrativo:")
    print(f"- Consultas por tenant: {dict(summary['per_tenant'])}")
    print(f"- Consultas por usuario: {dict(summary['per_user'])}")
    print(f"- Eventos auditados: {len(audit.events)}")


if __name__ == "__main__":
    main()

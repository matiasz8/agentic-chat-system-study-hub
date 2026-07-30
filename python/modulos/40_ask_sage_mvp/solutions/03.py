#!/usr/bin/env python3
"""Solución del ejercicio 3 del módulo Ask Sage MVP."""

import uuid
from dataclasses import dataclass, field


@dataclass
class Session:
    session_id: str
    history: list[dict[str, str]] = field(default_factory=list)


class DocumentManager:
    def __init__(self) -> None:
        self.chunks: list[str] = []

    def ingest(self, text: str) -> None:
        words = text.split()
        for start in range(0, len(words), 10):
            self.chunks.append(" ".join(words[start : start + 10]))

    def retrieve(self, question: str) -> list[str]:
        tokens = {token.lower().strip("¿?.,") for token in question.split() if len(token) > 3}
        return [chunk for chunk in self.chunks if any(token in chunk.lower() for token in tokens)]


class SessionManager:
    def __init__(self) -> None:
        self.sessions: dict[str, Session] = {}

    def create(self) -> Session:
        session = Session(session_id=str(uuid.uuid4())[:8])
        self.sessions[session.session_id] = session
        return session


class MockLLM:
    def answer(self, question: str, context: list[str]) -> str:
        if not context:
            return "No tengo suficiente contexto."
        return f"Respuesta simulada para '{question}': {' | '.join(context[:2])}"


def main() -> None:
    docs = DocumentManager()
    docs.ingest(
        "Ask Sage conserva historial de sesiones y recupera chunks relevantes antes de responder al usuario final."
    )
    session = SessionManager().create()
    question = "¿Qué hace Ask Sage antes de responder?"
    answer = MockLLM().answer(question, docs.retrieve(question))
    session.history.append({"role": "user", "message": question})
    session.history.append({"role": "assistant", "message": answer})
    print("=== Solución 3 ===")
    print(f"Sesión: {session.session_id}")
    for message in session.history:
        print(f"- {message['role']}: {message['message']}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Simulación avanzada del flujo completo de Ask Sage MVP."""

import time
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class Chunk:
    doc_id: str
    chunk_id: str
    text: str
    tags: tuple[str, ...]


@dataclass
class Session:
    session_id: str
    user_id: str
    history: list[dict[str, str]] = field(default_factory=list)


class APIKeyAuth:
    def __init__(self, valid_keys: set[str]) -> None:
        self.valid_keys = valid_keys

    def validate(self, api_key: str) -> bool:
        return api_key in self.valid_keys


class DocumentManager:
    def __init__(self) -> None:
        self.chunks: list[Chunk] = []

    def ingest(self, doc_id: str, text: str, tags: tuple[str, ...]) -> None:
        words = text.split()
        for index, start in enumerate(range(0, len(words), 12), start=1):
            piece = " ".join(words[start : start + 12])
            self.chunks.append(Chunk(doc_id, f"{doc_id}-{index}", piece, tags))

    def retrieve(self, question: str, limit: int = 3) -> list[Chunk]:
        tokens = {token.lower().strip("¿?.,") for token in question.split() if len(token) > 3}
        scored: list[tuple[int, Chunk]] = []
        for chunk in self.chunks:
            haystack = f"{' '.join(chunk.tags)} {chunk.text}".lower()
            score = sum(token in haystack for token in tokens)
            if score:
                scored.append((score, chunk))
        scored.sort(key=lambda item: (-item[0], item[1].chunk_id))
        return [chunk for _, chunk in scored[:limit]]


class SessionManager:
    def __init__(self) -> None:
        self.sessions: dict[str, Session] = {}

    def start(self, user_id: str) -> Session:
        session = Session(session_id=str(uuid.uuid4())[:8], user_id=user_id)
        self.sessions[session.session_id] = session
        return session

    def append(self, session_id: str, role: str, message: str) -> None:
        self.sessions[session_id].history.append({"role": role, "message": message})


class MockLLM:
    def stream_answer(self, question: str, chunks: list[Chunk]) -> str:
        if not chunks:
            response = "No tengo suficiente contexto para responder con confianza."
        else:
            response = (
                f"Respuesta guiada para '{question}': {'; '.join(chunk.text for chunk in chunks)}"
            )
        print("Streaming:", end=" ")
        for token in response.split():
            print(token, end=" ", flush=True)
            time.sleep(0.01)
        print()
        return response


def main() -> None:
    auth = APIKeyAuth({"ask-sage-demo-key"})
    if not auth.validate("ask-sage-demo-key"):
        raise SystemExit("API key inválida")

    docs = DocumentManager()
    docs.ingest(
        "policies",
        "La política de onboarding exige completar seguridad, acceso a herramientas y lectura de manuales durante la primera semana.",
        ("rrhh", "onboarding"),
    )
    docs.ingest(
        "security",
        "La política de seguridad pide MFA, rotación de secretos y revisión trimestral de permisos privilegiados.",
        ("seguridad", "identidad"),
    )

    sessions = SessionManager()
    session = sessions.start(user_id="ana")
    llm = MockLLM()
    question = "¿Qué pide la política de seguridad para permisos privilegiados?"
    retrieved = docs.retrieve(question)
    answer = llm.stream_answer(question, retrieved)
    sessions.append(session.session_id, "user", question)
    sessions.append(session.session_id, "assistant", answer)

    print("=== Ask Sage MVP · Avanzado ===")
    print(f"Sesión: {session.session_id}")
    print(f"Timestamp: {datetime.now(UTC).isoformat()}")
    print("Chunks recuperados:")
    for chunk in retrieved:
        print(f"- {chunk.chunk_id} ({', '.join(chunk.tags)}): {chunk.text}")
    print("\nHistorial:")
    for message in session.history:
        print(f"- {message['role']}: {message['message']}")


if __name__ == "__main__":
    main()

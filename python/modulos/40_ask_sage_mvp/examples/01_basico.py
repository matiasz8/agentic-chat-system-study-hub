#!/usr/bin/env python3
"""Ejemplo básico de Ask Sage MVP con búsqueda en memoria."""

from dataclasses import dataclass
import re
from typing import Iterable
import unicodedata


STOPWORDS = {"como", "qué", "que", "cual", "cuál", "existe", "una", "las", "los", "para", "politica", "política"}


def normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(char for char in normalized if not unicodedata.combining(char)).lower()


def tokenize(text: str) -> list[str]:
    return [token for token in re.findall(r"[a-z0-9]+", normalize(text)) if len(token) > 2 and token not in STOPWORDS]


@dataclass
class Document:
    doc_id: str
    title: str
    content: str


class InMemoryDocumentStore:
    def __init__(self, documents: Iterable[Document]) -> None:
        self.documents = list(documents)

    def search(self, question: str) -> list[Document]:
        tokens = tokenize(question)
        matches: list[tuple[int, Document]] = []
        for document in self.documents:
            haystack = normalize(f"{document.title} {document.content}")
            score = sum(token in haystack for token in tokens)
            if score:
                matches.append((score, document))
        return [document for _, document in sorted(matches, reverse=True)]


def answer_question(store: InMemoryDocumentStore, question: str) -> str:
    matches = store.search(question)
    if not matches:
        return "No encontré contexto relevante en el MVP."
    best = matches[0]
    return f"Según '{best.title}', la mejor pista es: {best.content}"


def main() -> None:
    documents = [
        Document("hr-001", "Política de vacaciones", "Las vacaciones anuales incluyen 15 días hábiles y deben acordarse con el manager."),
        Document("it-010", "Acceso remoto", "La VPN corporativa requiere autenticación multifactor y rotación trimestral de credenciales."),
        Document("ops-201", "Mesa de ayuda", "Los incidentes críticos deben escalarse por Slack y registrarse en la mesa de ayuda."),
    ]
    store = InMemoryDocumentStore(documents)
    questions = [
        "¿Cómo se gestionan las vacaciones?",
        "¿Qué pide la VPN corporativa?",
        "¿Existe una política de viáticos?",
    ]

    print("=== Ask Sage MVP · Básico ===")
    for turn, question in enumerate(questions, start=1):
        print(f"\nTurno {turn}")
        print(f"Usuario: {question}")
        print(f"Ask Sage: {answer_question(store, question)}")


if __name__ == "__main__":
    main()

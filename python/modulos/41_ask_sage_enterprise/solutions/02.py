#!/usr/bin/env python3
"""Solución del ejercicio 2 del módulo Ask Sage Enterprise."""

from dataclasses import dataclass


ROLE_PERMISSIONS = {
    "admin": {"read_public", "read_restricted"},
    "editor": {"read_public", "read_restricted"},
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


def can_access(user: User, document: Document) -> bool:
    return user.tenant_id == document.tenant_id and document.permission in ROLE_PERMISSIONS[user.role]


def search(user: User, question: str, documents: list[Document]) -> list[Document]:
    tokens = [token.lower() for token in question.split() if len(token) > 3]
    ranked = []
    for document in documents:
        if not can_access(user, document):
            continue
        score = sum(token in document.content.lower() for token in tokens)
        if score:
            ranked.append((score, document))
    return [doc for _, doc in sorted(ranked, reverse=True)]


def main() -> None:
    documents = [
        Document("acme", "FAQ", "Horarios y feriados.", "read_public"),
        Document("acme", "M&A", "Plan confidencial de expansión.", "read_restricted"),
    ]
    viewer = User("ana", "acme", "viewer")
    admin = User("leo", "acme", "admin")
    question = "¿Cuál es el plan de expansión?"
    print("=== Solución 2 ===")
    print("Viewer:", [doc.title for doc in search(viewer, question, documents)])
    print("Admin:", [doc.title for doc in search(admin, question, documents)])


if __name__ == "__main__":
    main()

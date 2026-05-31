#!/usr/bin/env python3
"""Ejemplo intermedio de RBAC para Ask Sage Enterprise."""

from dataclasses import dataclass


ROLE_PERMISSIONS = {
    "admin": {"read_public", "read_restricted", "audit"},
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
    if user.tenant_id != document.tenant_id:
        return False
    return document.permission in ROLE_PERMISSIONS.get(user.role, set())


def main() -> None:
    viewer = User("ana", "acme", "viewer")
    admin = User("leo", "acme", "admin")
    documents = [
        Document("acme", "FAQ interna", "Horarios y feriados del tenant.", "read_public"),
        Document("acme", "Informe M&A", "Documento sensible sobre adquisiciones futuras.", "read_restricted"),
    ]

    print("=== Ask Sage Enterprise · Intermedio ===")
    for user in [viewer, admin]:
        print(f"\nAccesos para {user.user_id} ({user.role}):")
        for document in documents:
            decision = "permitido" if can_access(user, document) else "denegado"
            print(f"- {document.title}: {decision}")


if __name__ == "__main__":
    main()

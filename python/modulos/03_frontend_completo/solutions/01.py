#!/usr/bin/env python3
"""Solución al ejercicio básico de gestor de sesión."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ChatSessionManager:
    messages: list[dict[str, str]] = field(default_factory=list)

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})

    def get_history(self) -> list[dict[str, str]]:
        return list(self.messages)

    def clear(self) -> None:
        self.messages.clear()


def main() -> None:
    session = ChatSessionManager()
    session.add_message("user", "Hola")
    session.add_message("assistant", "Hola, ¿en qué te ayudo?")
    print("=== Solución 1 ===")
    print(session.get_history())
    session.clear()
    print(f"Mensajes después de clear: {len(session.get_history())}")


if __name__ == "__main__":
    main()

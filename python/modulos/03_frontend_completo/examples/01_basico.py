#!/usr/bin/env python3
"""Simulación básica de manejo de sesión de chat."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Message:
    role: str
    content: str


@dataclass
class ChatSession:
    messages: List[Message] = field(default_factory=list)
    turn_number: int = 0

    def add_message(self, role: str, content: str) -> None:
        self.messages.append(Message(role=role, content=content))
        if role == "user":
            self.turn_number += 1

    def get_history(self) -> list[str]:
        return [f"{message.role}: {message.content}" for message in self.messages]

    def clear(self) -> None:
        self.messages.clear()
        self.turn_number = 0


def main() -> None:
    session = ChatSession()
    session.add_message("user", "Hola, necesito entender optimistic UI.")
    session.add_message(
        "assistant",
        "Optimistic UI actualiza la interfaz antes de confirmar la respuesta del servidor.",
    )
    session.add_message("user", "¿Y cómo guardo el historial?")

    print("=== Demo básica: sesión de chat ===")
    print(f"Turnos de usuario: {session.turn_number}\n")
    for line in session.get_history():
        print(line)

    print("\nLimpiando sesión...")
    session.clear()
    print(f"Mensajes después de clear(): {len(session.messages)}")


if __name__ == "__main__":
    main()

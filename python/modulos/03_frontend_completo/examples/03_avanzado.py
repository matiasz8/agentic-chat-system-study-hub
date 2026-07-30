#!/usr/bin/env python3
"""Simulación avanzada de un frontend de chat con state machine."""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum

ToolHandler = Callable[[dict[str, str]], dict[str, str]]


class TurnState(str, Enum):
    IDLE = "idle"
    THINKING = "thinking"
    TOOL_CALL = "tool_call"
    STREAMING = "streaming"
    ERROR = "error"


@dataclass
class Message:
    role: str
    content: str


@dataclass
class ChatController:
    registry: dict[str, ToolHandler]
    state: TurnState = TurnState.IDLE
    history: list[Message] = field(default_factory=list)
    retry_limit: int = 2

    def set_state(self, new_state: TurnState) -> None:
        self.state = new_state
        print(f"[state] -> {self.state.value}")

    def add_message(self, role: str, content: str) -> None:
        self.history.append(Message(role=role, content=content))

    def stream_text(self, text: str) -> None:
        self.set_state(TurnState.STREAMING)
        for token in text.split():
            print(f"[stream] {token}")
            time.sleep(0.05)

    def dispatch_tool(self, name: str, payload: dict[str, str]) -> dict[str, str]:
        self.set_state(TurnState.TOOL_CALL)
        return self.registry[name](payload)

    def handle_turn(self, user_message: str) -> None:
        self.add_message("user", user_message)
        self.set_state(TurnState.THINKING)

        for attempt in range(1, self.retry_limit + 1):
            try:
                if "precio" in user_message.lower() and attempt == 1:
                    raise RuntimeError("Fallo transitorio consultando pricing service")

                tool_result = self.dispatch_tool("lookup_product", {"query": user_message})
                final_answer = (
                    "Encontré información útil. "
                    f"{tool_result['summary']} "
                    "Ahora la UI puede renderizar texto incremental y acciones."
                )
                self.add_message("assistant", final_answer)
                self.stream_text(final_answer)
                self.set_state(TurnState.IDLE)
                return
            except Exception as error:
                self.set_state(TurnState.ERROR)
                print(f"[error] intento {attempt}: {error}")
                if attempt >= self.retry_limit:
                    fallback = (
                        "No pude completar la acción; muestra un botón de reintento en la UI."
                    )
                    self.add_message("assistant", fallback)
                    print(f"[assistant] {fallback}")
                    self.set_state(TurnState.IDLE)
                    return
                print("[retry] reintentando turno...")
                self.set_state(TurnState.THINKING)


def lookup_product(payload: dict[str, str]) -> dict[str, str]:
    query = payload["query"]
    return {
        "summary": f"La búsqueda para '{query}' devolvió una tarjeta con precio, stock y CTA de compra."
    }


def main() -> None:
    controller = ChatController(registry={"lookup_product": lookup_product})
    print("=== Demo avanzada: chat frontend completo ===")
    controller.handle_turn("Quiero el precio del plan enterprise")

    print("\nHistorial final:")
    for message in controller.history:
        print(f"- {message.role}: {message.content}")


if __name__ == "__main__":
    main()

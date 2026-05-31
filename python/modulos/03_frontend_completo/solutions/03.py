#!/usr/bin/env python3
"""Solución al ejercicio avanzado de turn manager con estados."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum


class State(str, Enum):
    IDLE = "idle"
    THINKING = "thinking"
    TOOL_CALL = "tool_call"
    STREAMING = "streaming"
    ERROR = "error"


@dataclass
class TurnManager:
    state: State = State.IDLE
    history: list[tuple[str, str]] = field(default_factory=list)

    def set_state(self, state: State) -> None:
        self.state = state
        print(f"[state] {self.state.value}")

    def run_tool(self, query: str) -> str:
        self.set_state(State.TOOL_CALL)
        return f"Tool result para '{query}'"

    def stream(self, text: str) -> None:
        self.set_state(State.STREAMING)
        for token in text.split():
            print(f"[token] {token}")
            time.sleep(0.04)

    def handle_turn(self, user_message: str) -> None:
        self.history.append(("user", user_message))
        self.set_state(State.THINKING)
        try:
            tool_result = self.run_tool(user_message)
            answer = f"Respuesta final usando {tool_result}"
            self.history.append(("assistant", answer))
            self.stream(answer)
            self.set_state(State.IDLE)
        except Exception as error:
            self.set_state(State.ERROR)
            fallback = f"Error recuperable: {error}"
            self.history.append(("assistant", fallback))
            print(fallback)
            self.set_state(State.IDLE)


def main() -> None:
    manager = TurnManager()
    print("=== Solución 3 ===")
    manager.handle_turn("Necesito datos del dashboard")
    print("Historial:")
    for role, content in manager.history:
        print(f"- {role}: {content}")


if __name__ == "__main__":
    main()

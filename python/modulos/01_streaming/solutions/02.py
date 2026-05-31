#!/usr/bin/env python3
"""Solución al ejercicio intermedio de formateo SSE."""

from __future__ import annotations


def format_sse(event_id: int, data: str, event: str = "token", retry: int = 1500) -> str:
    lines = [f"id: {event_id}", f"event: {event}", f"retry: {retry}"]
    lines.extend(f"data: {line}" for line in data.splitlines() or [""])
    return "\n".join(lines) + "\n\n"


def main() -> None:
    tokens = ["El", "frontend", "recibe", "progreso", "inmediato"]
    print("=== Solución 2 ===\n")
    for event_id, token in enumerate(tokens, start=1):
        print(format_sse(event_id, token), end="")

    print(format_sse(len(tokens) + 1, "[DONE]", event="done"), end="")


if __name__ == "__main__":
    main()

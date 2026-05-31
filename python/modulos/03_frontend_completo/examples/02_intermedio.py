#!/usr/bin/env python3
"""Simulación intermedia de tool calls en un chat con agentes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

ToolHandler = Callable[[dict[str, str]], dict[str, str]]


@dataclass
class ToolCall:
    name: str
    payload: dict[str, str]


def tool_weather(payload: dict[str, str]) -> dict[str, str]:
    city = payload.get("city", "desconocida")
    return {"tool": "weather", "result": f"Clima despejado en {city}, 24°C"}


def tool_calendar(payload: dict[str, str]) -> dict[str, str]:
    topic = payload.get("topic", "sin tema")
    return {"tool": "calendar", "result": f"Reunión agendada para revisar {topic} a las 15:00"}


def decide_tool(user_message: str) -> ToolCall:
    lowered = user_message.lower()
    if "clima" in lowered:
        return ToolCall(name="weather", payload={"city": "Buenos Aires"})
    return ToolCall(name="calendar", payload={"topic": "la demo del agente"})


def run_agent_turn(user_message: str, registry: dict[str, ToolHandler]) -> str:
    call = decide_tool(user_message)
    print(f"Agente decide invocar: {call.name} con {call.payload}")
    tool_result = registry[call.name](call.payload)
    print(f"Herramienta respondió: {tool_result}")
    return (
        f"Respuesta final del agente: usé {tool_result['tool']} y obtuve -> "
        f"{tool_result['result']}"
    )


def main() -> None:
    registry: dict[str, ToolHandler] = {
        "weather": tool_weather,
        "calendar": tool_calendar,
    }
    user_message = "¿Cómo está el clima para la reunión de mañana?"

    print("=== Demo intermedia: tool call cycle ===")
    print(f"Usuario: {user_message}")
    final_answer = run_agent_turn(user_message, registry)
    print(final_answer)


if __name__ == "__main__":
    main()

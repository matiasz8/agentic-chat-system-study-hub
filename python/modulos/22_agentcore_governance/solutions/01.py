#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Agent:
    agent_id: str
    name: str
    capabilities: List[str]
    owner: str
    status: str


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: Dict[str, Agent] = {}

    def add(self, agent: Agent) -> None:
        if agent.agent_id in self._agents:
            raise ValueError(f"ID duplicado: {agent.agent_id}")
        self._agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> Agent:
        return self._agents[agent_id]

    def find_by_capability(self, capability: str) -> List[Agent]:
        return [agent for agent in self._agents.values() if capability in agent.capabilities]


def main() -> None:
    registry = AgentRegistry()
    registry.add(Agent("agent-a", "Compliance Bot", ["audit", "search"], "legal", "active"))
    registry.add(Agent("agent-b", "Ops Bot", ["restart", "search"], "platform", "maintenance"))

    print("== Consulta individual ==")
    print(registry.get("agent-a"))

    print("\n== Agentes con 'search' ==")
    for agent in registry.find_by_capability("search"):
        print(f"{agent.agent_id} -> {agent.name} ({agent.status})")


if __name__ == "__main__":
    main()

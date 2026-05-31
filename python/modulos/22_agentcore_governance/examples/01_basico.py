#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class AgentMetadata:
    agent_id: str
    name: str
    capabilities: List[str]
    owner: str
    status: str = "active"
    tags: Dict[str, str] = field(default_factory=dict)


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: Dict[str, AgentMetadata] = {}

    def register(self, agent: AgentMetadata) -> None:
        if agent.agent_id in self._agents:
            raise ValueError(f"El agente {agent.agent_id} ya existe")
        self._agents[agent.agent_id] = agent

    def capabilities_of(self, agent_id: str) -> List[str]:
        return list(self._agents[agent_id].capabilities)

    def agents_for_capability(self, capability: str) -> List[AgentMetadata]:
        return [
            agent
            for agent in self._agents.values()
            if capability in agent.capabilities and agent.status == "active"
        ]

    def summary(self) -> List[str]:
        rows = []
        for agent in self._agents.values():
            rows.append(
                f"- {agent.agent_id}: {agent.name} | owner={agent.owner} "
                f"| status={agent.status} | capabilities={', '.join(agent.capabilities)}"
            )
        return rows


def main() -> None:
    registry = AgentRegistry()
    registry.register(
        AgentMetadata(
            agent_id="agent-risk",
            name="Risk Reviewer",
            capabilities=["read_ticket", "score_risk", "request_approval"],
            owner="equipo-compliance",
            tags={"env": "prod", "criticality": "high"},
        )
    )
    registry.register(
        AgentMetadata(
            agent_id="agent-support",
            name="Support Copilot",
            capabilities=["search_kb", "summarize", "draft_reply"],
            owner="equipo-soporte",
        )
    )
    registry.register(
        AgentMetadata(
            agent_id="agent-shadow",
            name="Shadow Agent",
            capabilities=["search_kb"],
            owner="laboratorio",
            status="disabled",
        )
    )

    print("== Registro de agentes ==")
    for row in registry.summary():
        print(row)

    print("\n== Capacidades de agent-risk ==")
    print(registry.capabilities_of("agent-risk"))

    print("\n== Agentes activos con capacidad 'search_kb' ==")
    for agent in registry.agents_for_capability("search_kb"):
        print(f"{agent.agent_id} -> {agent.name}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import json
import time
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class ToolDefinition:
    name: str
    description: str
    handler: Callable[[dict[str, Any]], str]


@dataclass
class MCPServerNode:
    name: str
    tools: dict[str, ToolDefinition]
    last_heartbeat: float = field(default_factory=time.time)
    failures: int = 0

    def health(self) -> dict[str, Any]:
        age_seconds = time.time() - self.last_heartbeat
        status = 'healthy' if age_seconds < 5 and self.failures < 2 else 'degraded'
        return {'server': self.name, 'status': status, 'age_seconds': round(age_seconds, 2), 'failures': self.failures}

    def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> str:
        self.last_heartbeat = time.time()
        return self.tools[tool_name].handler(arguments)


class MCPHub:
    def __init__(self, servers: list[MCPServerNode]) -> None:
        self.servers = {server.name: server for server in servers}
        self.routing_table = self._build_routing_table()

    def _build_routing_table(self) -> dict[str, tuple[str, str]]:
        collisions: dict[str, list[str]] = {}
        for server in self.servers.values():
            for tool_name in server.tools:
                collisions.setdefault(tool_name, []).append(server.name)

        routing: dict[str, tuple[str, str]] = {}
        for tool_name, owners in collisions.items():
            if len(owners) == 1:
                routing[tool_name] = (owners[0], tool_name)
            else:
                for owner in owners:
                    routing[f'{owner}.{tool_name}'] = (owner, tool_name)
        return routing

    def list_tools(self) -> list[dict[str, str]]:
        items = []
        for exposed_name, (server_name, local_name) in sorted(self.routing_table.items()):
            description = self.servers[server_name].tools[local_name].description
            items.append({'name': exposed_name, 'server': server_name, 'description': description})
        return items

    def call_tool(self, exposed_name: str, arguments: dict[str, Any]) -> str:
        server_name, local_name = self.routing_table[exposed_name]
        server = self.servers[server_name]
        health = server.health()
        if health['status'] != 'healthy':
            raise RuntimeError(f"Servidor {server_name} no disponible: {health}")
        return server.call_tool(local_name, arguments)

    def health_report(self) -> list[dict[str, Any]]:
        return [server.health() for server in self.servers.values()]


def main() -> None:
    weather_server = MCPServerNode(
        name='weather',
        tools={
            'search': ToolDefinition('search', 'Busca clima por ciudad.', lambda args: f"Clima estimado para {args['query']}: 21 °C"),
            'forecast': ToolDefinition('forecast', 'Pronóstico de tres días.', lambda args: f"Pronóstico para {args['city']}: sol, nubes, lluvia"),
        },
    )
    notes_server = MCPServerNode(
        name='notes',
        tools={
            'search': ToolDefinition('search', 'Busca notas de estudio.', lambda args: f"Notas encontradas para {args['query']}: MCP y JSON-RPC"),
            'summarize': ToolDefinition('summarize', 'Resume una nota.', lambda args: f"Resumen de {args['note_id']}: conceptos clave concentrados."),
        },
    )
    slow_server = MCPServerNode(
        name='legacy',
        tools={
            'stats': ToolDefinition('stats', 'Devuelve métricas antiguas.', lambda args: f"Métricas para {args['scope']}: 3 errores, 8 warnings"),
        },
        last_heartbeat=time.time() - 10,
        failures=2,
    )

    hub = MCPHub([weather_server, notes_server, slow_server])

    print('=== Hub MCP avanzado ===')
    print('Catálogo agregado:')
    print(json.dumps(hub.list_tools(), indent=2, ensure_ascii=False))
    print('-' * 72)
    print('Estado de salud:')
    print(json.dumps(hub.health_report(), indent=2, ensure_ascii=False))
    print('-' * 72)

    demo_calls = [
        ('weather.search', {'query': 'Madrid'}),
        ('notes.search', {'query': 'MCP'}),
        ('forecast', {'city': 'Bogotá'}),
    ]

    for exposed_name, arguments in demo_calls:
        result = hub.call_tool(exposed_name, arguments)
        print(f'✅ {exposed_name}({arguments}) -> {result}')

    try:
        hub.call_tool('stats', {'scope': 'legacy'})
    except Exception as error:  # noqa: BLE001
        print(f'⚠️ Llamada bloqueada por health monitoring: {error}')

    print('Aprendizaje clave: un hub puede agregar servidores y resolver colisiones con namespaces.')


if __name__ == '__main__':
    main()

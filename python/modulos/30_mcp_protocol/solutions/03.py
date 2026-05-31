#!/usr/bin/env python3
import json
from typing import Any


class DemoServer:
    def __init__(self) -> None:
        self.tools = {
            'echo': {
                'description': 'Devuelve el texto recibido.',
                'handler': lambda args: args['text'],
            },
            'sum_numbers': {
                'description': 'Suma una lista de enteros.',
                'handler': lambda args: str(sum(args['numbers'])),
            },
        }

    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        request_id = request.get('id')
        try:
            if request['method'] == 'initialize':
                result = {'protocolVersion': '2024-11-05', 'serverInfo': {'name': 'demo-server', 'version': '1.0.0'}, 'capabilities': {'tools': {}}}
            elif request['method'] == 'tools/list':
                result = {'tools': [
                    {'name': name, 'description': data['description'], 'inputSchema': {'type': 'object', 'properties': {}}}
                    for name, data in self.tools.items()
                ]}
            elif request['method'] == 'tools/call':
                params = request['params']
                name = params['name']
                if name not in self.tools:
                    raise KeyError(f'Tool no encontrada: {name}')
                text = self.tools[name]['handler'](params.get('arguments', {}))
                result = {'content': [{'type': 'text', 'text': text}]}
            else:
                raise KeyError(f"Método no soportado: {request['method']}")
            return {'jsonrpc': '2.0', 'id': request_id, 'result': result}
        except Exception as error:  # noqa: BLE001
            return {'jsonrpc': '2.0', 'id': request_id, 'error': {'code': -32020, 'message': str(error)}}


class MCPClient:
    def __init__(self, server: DemoServer) -> None:
        self.server = server
        self.next_id = 1
        self.tool_cache: list[dict[str, Any]] = []

    def send(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        request = {'jsonrpc': '2.0', 'id': self.next_id, 'method': method}
        if params is not None:
            request['params'] = params
        self.next_id += 1
        response = self.server.handle(request)
        if 'error' in response:
            message = response['error']['message']
            raise RuntimeError(f'Error MCP: {message}')
        return response['result']

    def initialize(self) -> None:
        result = self.send('initialize')
        print(f"Conectado a {result['serverInfo']['name']} ({result['protocolVersion']})")

    def discover_tools(self) -> None:
        result = self.send('tools/list')
        self.tool_cache = result['tools']
        print('Tools disponibles:')
        for tool in self.tool_cache:
            print(f"- {tool['name']}: {tool['description']}")

    def call_tool(self, name: str, arguments: dict[str, Any]) -> None:
        try:
            result = self.send('tools/call', {'name': name, 'arguments': arguments})
            print(f"✅ {name}: {result['content'][0]['text']}")
        except RuntimeError as error:
            print(f"⚠️ {name}: {error}")


def main() -> None:
    client = MCPClient(DemoServer())
    client.initialize()
    client.discover_tools()
    print('-' * 60)
    client.call_tool('echo', {'text': 'Hola desde el cliente'})
    client.call_tool('sum_numbers', {'numbers': [4, 8, 15, 16, 23, 42]})
    client.call_tool('missing_tool', {})
    print('-' * 60)
    print('Catálogo cacheado:')
    print(json.dumps(client.tool_cache, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import io
import json
from dataclasses import dataclass
from typing import Any


@dataclass
class Document:
    uri: str
    title: str
    text: str


class RichMCPServer:
    def __init__(self) -> None:
        self.documents = {
            'doc://mcp/intro': Document(
                uri='doc://mcp/intro',
                title='Introducción a MCP',
                text='MCP estandariza cómo un host descubre tools, resources y prompts. '
                'Es útil para conectar agentes con sistemas externos.',
            ),
            'doc://python/jsonrpc': Document(
                uri='doc://python/jsonrpc',
                title='JSON-RPC con Python',
                text='JSON-RPC 2.0 usa requests y responses con campos jsonrpc, id, method y params. '
                'Una implementación mínima puede vivir sobre stdin y stdout.',
            ),
        }
        self.prompts = {
            'study_note': 'Resume {topic} en 3 bullets para una sesión de estudio.',
            'compare_topics': 'Compara {left} vs {right} con ventajas y riesgos.',
        }

    def dispatch(self, message: dict[str, Any]) -> dict[str, Any]:
        method = message['method']
        request_id = message.get('id')

        try:
            handlers = {
                'initialize': self.handle_initialize,
                'resources/list': self.handle_resources_list,
                'resources/read': self.handle_resources_read,
                'tools/list': self.handle_tools_list,
                'tools/call': self.handle_tools_call,
                'prompts/list': self.handle_prompts_list,
                'prompts/get': self.handle_prompts_get,
            }
            result = handlers[method](message.get('params', {}))
            return {'jsonrpc': '2.0', 'id': request_id, 'result': result}
        except Exception as error:  # noqa: BLE001
            return {
                'jsonrpc': '2.0',
                'id': request_id,
                'error': {'code': -32001, 'message': str(error)},
            }

    def handle_initialize(self, params: dict[str, Any]) -> dict[str, Any]:
        return {
            'protocolVersion': params.get('protocolVersion', '2024-11-05'),
            'serverInfo': {'name': 'rich-mcp-demo', 'version': '1.0.0'},
            'capabilities': {'resources': {}, 'tools': {}, 'prompts': {}},
        }

    def handle_resources_list(self, _: dict[str, Any]) -> dict[str, Any]:
        resources = [
            {'uri': doc.uri, 'name': doc.title, 'mimeType': 'text/plain'}
            for doc in self.documents.values()
        ]
        return {'resources': resources}

    def handle_resources_read(self, params: dict[str, Any]) -> dict[str, Any]:
        document = self.documents[params['uri']]
        return {'contents': [{'uri': document.uri, 'mimeType': 'text/plain', 'text': document.text}]}

    def handle_tools_list(self, _: dict[str, Any]) -> dict[str, Any]:
        return {
            'tools': [
                {
                    'name': 'search',
                    'description': 'Busca documentos por palabra clave.',
                    'inputSchema': {
                        'type': 'object',
                        'properties': {'query': {'type': 'string'}},
                        'required': ['query'],
                    },
                },
                {
                    'name': 'summarize',
                    'description': 'Resume un recurso a una sola oración.',
                    'inputSchema': {
                        'type': 'object',
                        'properties': {'uri': {'type': 'string'}},
                        'required': ['uri'],
                    },
                },
            ]
        }

    def handle_tools_call(self, params: dict[str, Any]) -> dict[str, Any]:
        name = params['name']
        arguments = params.get('arguments', {})
        if name == 'search':
            query = arguments['query'].lower()
            matches = [doc.title for doc in self.documents.values() if query in doc.text.lower() or query in doc.title.lower()]
            text = 'Coincidencias: ' + (', '.join(matches) if matches else 'ninguna')
        elif name == 'summarize':
            document = self.documents[arguments['uri']]
            first_sentence = document.text.split('. ')[0].strip().rstrip('.')
            text = f'Resumen de {document.title}: {first_sentence}.'
        else:
            raise KeyError(f'Tool desconocida: {name}')
        return {'content': [{'type': 'text', 'text': text}]}

    def handle_prompts_list(self, _: dict[str, Any]) -> dict[str, Any]:
        return {
            'prompts': [
                {'name': name, 'description': template}
                for name, template in self.prompts.items()
            ]
        }

    def handle_prompts_get(self, params: dict[str, Any]) -> dict[str, Any]:
        name = params['name']
        arguments = params.get('arguments', {})
        template = self.prompts[name]
        rendered = template.format(**arguments)
        return {'messages': [{'role': 'user', 'content': {'type': 'text', 'text': rendered}}]}


def run_simulation() -> str:
    server = RichMCPServer()
    incoming = io.StringIO('
'.join([
        json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'protocolVersion': '2024-11-05'}}),
        json.dumps({'jsonrpc': '2.0', 'id': 2, 'method': 'resources/list'}),
        json.dumps({'jsonrpc': '2.0', 'id': 3, 'method': 'resources/read', 'params': {'uri': 'doc://mcp/intro'}}),
        json.dumps({'jsonrpc': '2.0', 'id': 4, 'method': 'tools/list'}),
        json.dumps({'jsonrpc': '2.0', 'id': 5, 'method': 'tools/call', 'params': {'name': 'search', 'arguments': {'query': 'python'}}}),
        json.dumps({'jsonrpc': '2.0', 'id': 6, 'method': 'prompts/get', 'params': {'name': 'compare_topics', 'arguments': {'left': 'stdio', 'right': 'HTTP+SSE'}}}),
    ]))
    outgoing = io.StringIO()

    for line in incoming:
        message = json.loads(line)
        response = server.dispatch(message)
        outgoing.write(json.dumps({'request': message, 'response': response}, ensure_ascii=False) + '
')

    return outgoing.getvalue()


def main() -> None:
    print('=== Simulación intermedia: loop stdin/stdout ===')
    transcript = run_simulation().strip().splitlines()
    for entry in transcript:
        event = json.loads(entry)
        print('➡️', json.dumps(event['request'], ensure_ascii=False))
        print('⬅️', json.dumps(event['response'], ensure_ascii=False, indent=2))
        print('-' * 72)

    print('Aprendizaje clave: el mismo loop JSON-RPC sirve para resources, tools y prompts.')


if __name__ == '__main__':
    main()

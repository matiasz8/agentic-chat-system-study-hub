#!/usr/bin/env python3
import ast
import json
from typing import Any, Callable


class SafeCalculator(ast.NodeVisitor):
    OPERATORS = {
        ast.Add: lambda a, b: a + b,
        ast.Sub: lambda a, b: a - b,
        ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b,
        ast.Pow: lambda a, b: a ** b,
        ast.Mod: lambda a, b: a % b,
        ast.USub: lambda a: -a,
        ast.UAdd: lambda a: a,
    }

    def visit_Expression(self, node: ast.Expression) -> float:
        return self.visit(node.body)

    def visit_BinOp(self, node: ast.BinOp) -> float:
        operator = self.OPERATORS.get(type(node.op))
        if operator is None:
            raise ValueError('Operador no permitido')
        return operator(self.visit(node.left), self.visit(node.right))

    def visit_UnaryOp(self, node: ast.UnaryOp) -> float:
        operator = self.OPERATORS.get(type(node.op))
        if operator is None:
            raise ValueError('Operador unario no permitido')
        return operator(self.visit(node.operand))

    def visit_Constant(self, node: ast.Constant) -> float:
        if not isinstance(node.value, (int, float)):
            raise ValueError('Solo se permiten números')
        return float(node.value)

    def generic_visit(self, node: ast.AST) -> float:
        raise ValueError(f'Nodo no permitido: {type(node).__name__}')


def evaluate_expression(expression: str) -> float:
    tree = ast.parse(expression, mode='eval')
    return SafeCalculator().visit(tree)


class InMemoryMCPServer:
    def __init__(self) -> None:
        self.tools: dict[str, tuple[dict[str, Any], Callable[..., str]]] = {
            'get_weather': (
                {
                    'name': 'get_weather',
                    'description': 'Devuelve un clima simulado para una ciudad.',
                    'inputSchema': {
                        'type': 'object',
                        'properties': {
                            'city': {'type': 'string'},
                            'unit': {'type': 'string', 'enum': ['C', 'F']},
                        },
                        'required': ['city'],
                    },
                },
                self.get_weather,
            ),
            'calculate': (
                {
                    'name': 'calculate',
                    'description': 'Evalúa expresiones aritméticas básicas.',
                    'inputSchema': {
                        'type': 'object',
                        'properties': {'expression': {'type': 'string'}},
                        'required': ['expression'],
                    },
                },
                self.calculate,
            ),
        }

    def get_weather(self, city: str, unit: str = 'C') -> str:
        dataset = {
            'madrid': {'C': '22 °C, soleado', 'F': '71.6 °F, soleado'},
            'bogota': {'C': '14 °C, nublado', 'F': '57.2 °F, nublado'},
            'barcelona': {'C': '24 °C, brisa marina', 'F': '75.2 °F, brisa marina'},
        }
        normalized = city.strip().lower()
        weather = dataset.get(normalized, {'C': '20 °C, estable', 'F': '68.0 °F, estable'})
        return f'Clima en {city.title()}: {weather[unit]}'

    def calculate(self, expression: str) -> str:
        result = evaluate_expression(expression)
        return f'Resultado de {expression} = {result:g}'

    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        method = request['method']
        request_id = request.get('id')

        try:
            if method == 'tools/list':
                return {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'result': {'tools': [schema for schema, _ in self.tools.values()]},
                }

            if method == 'tools/call':
                params = request.get('params', {})
                name = params['name']
                arguments = params.get('arguments', {})
                _, tool = self.tools[name]
                text = tool(**arguments)
                return {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'result': {'content': [{'type': 'text', 'text': text}]},
                }

            raise KeyError(f'Método no soportado: {method}')
        except Exception as error:  # noqa: BLE001
            return {
                'jsonrpc': '2.0',
                'id': request_id,
                'error': {'code': -32000, 'message': str(error)},
            }


def pretty(label: str, payload: dict[str, Any]) -> None:
    print(label)
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print('-' * 72)


def main() -> None:
    server = InMemoryMCPServer()
    messages = [
        {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list'},
        {
            'jsonrpc': '2.0',
            'id': 2,
            'method': 'tools/call',
            'params': {'name': 'get_weather', 'arguments': {'city': 'Madrid', 'unit': 'C'}},
        },
        {
            'jsonrpc': '2.0',
            'id': 3,
            'method': 'tools/call',
            'params': {'name': 'calculate', 'arguments': {'expression': '(2 + 3) * 4 - 5'}},
        },
    ]

    print('=== Simulación básica de intercambio MCP ===')
    for message in messages:
        pretty('➡️ Request', message)
        response = server.handle(message)
        pretty('⬅️ Response', response)

    print('Aprendizaje clave: tools/list descubre capacidades y tools/call ejecuta acciones.')


if __name__ == '__main__':
    main()

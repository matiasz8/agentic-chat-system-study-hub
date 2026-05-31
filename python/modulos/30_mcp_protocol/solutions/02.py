#!/usr/bin/env python3
import ast
import json
from datetime import datetime, timedelta, timezone
from typing import Any


class Calculator(ast.NodeVisitor):
    OPS = {
        ast.Add: lambda a, b: a + b,
        ast.Sub: lambda a, b: a - b,
        ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b,
        ast.USub: lambda a: -a,
    }

    def visit_Expression(self, node: ast.Expression) -> float:
        return self.visit(node.body)

    def visit_BinOp(self, node: ast.BinOp) -> float:
        operator = self.OPS.get(type(node.op))
        if operator is None:
            raise ValueError('Operación no permitida')
        return operator(self.visit(node.left), self.visit(node.right))

    def visit_UnaryOp(self, node: ast.UnaryOp) -> float:
        operator = self.OPS.get(type(node.op))
        if operator is None:
            raise ValueError('Operación unaria no permitida')
        return operator(self.visit(node.operand))

    def visit_Constant(self, node: ast.Constant) -> float:
        if not isinstance(node.value, (int, float)):
            raise ValueError('Solo números permitidos')
        return float(node.value)

    def generic_visit(self, node: ast.AST) -> float:
        raise ValueError(f'Nodo inválido: {type(node).__name__}')


def safe_eval(expression: str) -> float:
    return Calculator().visit(ast.parse(expression, mode='eval'))


class ToolServer:
    def tools_list(self) -> list[dict[str, Any]]:
        return [
            {'name': 'calculator', 'description': 'Calculadora segura', 'inputSchema': {'type': 'object', 'properties': {'expression': {'type': 'string'}}, 'required': ['expression']}},
            {'name': 'string_transform', 'description': 'Transforma texto', 'inputSchema': {'type': 'object', 'properties': {'text': {'type': 'string'}, 'operation': {'type': 'string'}}, 'required': ['text', 'operation']}},
            {'name': 'datetime_info', 'description': 'Devuelve fecha y hora', 'inputSchema': {'type': 'object', 'properties': {'timezone_offset': {'type': 'number'}}, 'required': []}},
        ]

    def tool_call(self, name: str, arguments: dict[str, Any]) -> str:
        if name == 'calculator':
            return f"Resultado: {safe_eval(arguments['expression']):g}"
        if name == 'string_transform':
            text = arguments['text']
            operation = arguments['operation']
            actions = {
                'upper': text.upper,
                'lower': text.lower,
                'title': text.title,
                'reverse': lambda: text[::-1],
            }
            if operation not in actions:
                raise ValueError(f'Operación desconocida: {operation}')
            return f"Texto transformado: {actions[operation]()}"
        if name == 'datetime_info':
            offset = float(arguments.get('timezone_offset', 0))
            zone = timezone(timedelta(hours=offset))
            now = datetime.now(zone)
            return f"Hora local: {now.isoformat()} ({now.strftime('%A')})"
        raise KeyError(f'Tool inexistente: {name}')

    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        try:
            if request['method'] == 'tools/list':
                result = {'tools': self.tools_list()}
            elif request['method'] == 'tools/call':
                params = request['params']
                text = self.tool_call(params['name'], params.get('arguments', {}))
                result = {'content': [{'type': 'text', 'text': text}]}
            else:
                raise KeyError(f"Método desconocido: {request['method']}")
            return {'jsonrpc': '2.0', 'id': request.get('id'), 'result': result}
        except Exception as error:  # noqa: BLE001
            return {'jsonrpc': '2.0', 'id': request.get('id'), 'error': {'code': -32010, 'message': str(error)}}


def main() -> None:
    server = ToolServer()
    requests = [
        {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list'},
        {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call', 'params': {'name': 'calculator', 'arguments': {'expression': '10 / 2 + 7'}}},
        {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call', 'params': {'name': 'string_transform', 'arguments': {'text': 'mcp protocol', 'operation': 'title'}}},
        {'jsonrpc': '2.0', 'id': 4, 'method': 'tools/call', 'params': {'name': 'datetime_info', 'arguments': {'timezone_offset': -3}}},
    ]

    print('=== Solución 02: tools/call con herramientas útiles ===')
    for request in requests:
        print(json.dumps(server.handle(request), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Tuple


TYPE_MAP: Dict[str, Tuple[type, ...]] = {
    "string": (str,),
    "integer": (int,),
    "number": (int, float),
    "boolean": (bool,),
    "object": (dict,),
    "array": (list,),
}


class ToolExecutionError(RuntimeError):
    pass


@dataclass
class ToolSpec:
    name: str
    func: Callable[..., Any]
    input_schema: Dict[str, Any]
    output_type: type


class ToolExecutor:
    def __init__(self) -> None:
        self._tools: Dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        self._tools[spec.name] = spec

    def invoke(self, name: str, payload: Dict[str, Any]) -> Any:
        spec = self._tools[name]
        self._validate(payload, spec.input_schema)
        try:
            result = spec.func(**payload)
        except Exception as exc:
            raise ToolExecutionError(f"La tool {name} falló: {exc}") from exc
        if not isinstance(result, spec.output_type):
            raise ToolExecutionError(
                f"La tool {name} devolvió {type(result).__name__}, se esperaba {spec.output_type.__name__}"
            )
        return result

    def _validate(self, payload: Dict[str, Any], schema: Dict[str, Any]) -> None:
        if schema.get("type") != "object" or not isinstance(payload, dict):
            raise ToolExecutionError("El payload debe ser un objeto")
        for key in schema.get("required", []):
            if key not in payload:
                raise ToolExecutionError(f"Falta el campo requerido: {key}")
        for key, rules in schema.get("properties", {}).items():
            if key not in payload:
                continue
            expected = TYPE_MAP[rules["type"]]
            if not isinstance(payload[key], expected):
                raise ToolExecutionError(f"{key} debe ser de tipo {rules['type']}")
            if "minimum" in rules and payload[key] < rules["minimum"]:
                raise ToolExecutionError(f"{key} debe ser >= {rules['minimum']}")


def repeat_text(text: str, times: int) -> str:
    return " | ".join(text for _ in range(times))


def broken_tool(text: str) -> int:
    return len(text.split())


def main() -> None:
    executor = ToolExecutor()
    executor.register(
        ToolSpec(
            name="repeat_text",
            func=repeat_text,
            input_schema={
                "type": "object",
                "required": ["text", "times"],
                "properties": {
                    "text": {"type": "string"},
                    "times": {"type": "integer", "minimum": 1},
                },
            },
            output_type=str,
        )
    )
    executor.register(
        ToolSpec(
            name="broken_tool",
            func=broken_tool,
            input_schema={
                "type": "object",
                "required": ["text"],
                "properties": {"text": {"type": "string"}},
            },
            output_type=str,
        )
    )

    print("== Validación correcta ==")
    print(executor.invoke("repeat_text", {"text": "audit", "times": 2}))

    print("\n== Error de input ==")
    try:
        executor.invoke("repeat_text", {"text": "audit", "times": 0})
    except ToolExecutionError as exc:
        print(exc)

    print("\n== Error de output ==")
    try:
        executor.invoke("broken_tool", {"text": "salida inesperada"})
    except ToolExecutionError as exc:
        print(exc)


if __name__ == "__main__":
    main()

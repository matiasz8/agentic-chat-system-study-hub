#!/usr/bin/env python3
"""
Solución 03 – Pipeline con registro de componentes y streaming
Módulo 02: Generative UI
"""

import time
from dataclasses import dataclass
from typing import Iterator

REGISTRO: dict[str, type] = {}


def componente(nombre: str):
    def decorador(cls):
        REGISTRO[nombre] = cls
        return cls
    return decorador


@componente("Grafico")
@dataclass
class Grafico:
    titulo: str
    valores: list[int]

    def renderizar(self) -> str:
        barras = " | ".join(f"{v}" for v in self.valores)
        return f"  📊 {self.titulo}: [{barras}]"


@componente("Alerta")
@dataclass
class Alerta:
    mensaje: str
    nivel: str = "warning"

    def renderizar(self) -> str:
        return f"  ⚠️  [{self.nivel.upper()}] {self.mensaje}"


def _tool_calls_simulados(mensaje: str) -> list[dict]:
    return [
        {"componente": "Grafico", "props": {"titulo": "Stock por sede", "valores": [1500, 120, 85]}},
        {"componente": "Alerta", "props": {"mensaje": "Sede Sur con stock crítico.", "nivel": "error"}},
        {"componente": "Desconocido", "props": {}},
    ]


def pipeline(mensaje: str) -> Iterator[str]:
    for tc in _tool_calls_simulados(mensaje):
        time.sleep(0.05)
        cls = REGISTRO.get(tc["componente"])
        if cls is None:
            yield f"  ⚠️ Componente no registrado: {tc['componente']!r}"
        else:
            yield cls(**tc["props"]).renderizar()


def main():
    print("Pipeline Generative UI – streaming de componentes\n")
    for bloque in pipeline("¿Cuál es el stock actual?"):
        print(bloque, flush=True)


if __name__ == "__main__":
    main()

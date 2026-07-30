#!/usr/bin/env python3
"""
Ejemplo 03 – Avanzado: Pipeline Generative UI completo
Módulo 02: Generative UI

Muestra el pipeline completo:
  1. El usuario envía un mensaje.
  2. El agente procesa y emite tool calls estructurados.
  3. El backend mapea cada tool call a un componente UI.
  4. Los componentes se "streaman" al frontend en orden.

Implementado con Python stdlib + generadores (sin librerías externas).
"""

import time
from collections.abc import Iterator
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Registro de componentes UI
# ---------------------------------------------------------------------------

REGISTRO_COMPONENTES: dict[str, type] = {}


def componente(nombre: str):
    """Decorador que registra una clase como componente UI."""

    def decorador(cls):
        REGISTRO_COMPONENTES[nombre] = cls
        return cls

    return decorador


@componente("StockChart")
@dataclass
class StockChart:
    titulo: str
    sedes: list[str]
    valores: list[int]

    def renderizar(self) -> str:
        lineas = [f"  📊 {self.titulo}"]
        max_v = max(self.valores) if self.valores else 1
        for sede, val in zip(self.sedes, self.valores):
            barras = "█" * int(val / max_v * 20)
            lineas.append(f"  {sede:<12} {barras} {val}")
        return "\n".join(lineas)


@componente("AlertaBanner")
@dataclass
class AlertaBanner:
    mensaje: str
    nivel: str = "warning"

    def renderizar(self) -> str:
        iconos = {"info": "ℹ️", "warning": "⚠️", "error": "🚨"}
        return f"  {iconos.get(self.nivel, '•')} [{self.nivel.upper()}] {self.mensaje}"


@componente("RequisicionForm")
@dataclass
class RequisicionForm:
    medicamento: str
    cantidad_sugerida: int
    sedes_afectadas: list[str]

    def renderizar(self) -> str:
        sedes = ", ".join(self.sedes_afectadas)
        return (
            f"  📋 Formulario de Requisición\n"
            f"     Medicamento: {self.medicamento}\n"
            f"     Cantidad   : {self.cantidad_sugerida} unidades\n"
            f"     Destino    : {sedes}"
        )


# ---------------------------------------------------------------------------
# Motor del agente (simula tool calls del LLM)
# ---------------------------------------------------------------------------


def _simular_tool_calls(mensaje_usuario: str) -> list[dict]:
    """
    El LLM real devolvería tool calls; aquí los simulamos.
    Cada dict tiene 'componente' (nombre) y 'props' (argumentos).
    """
    if "stock" in mensaje_usuario.lower() or "comparativa" in mensaje_usuario.lower():
        return [
            {
                "componente": "StockChart",
                "props": {
                    "titulo": "Stock Medicamento X – Por Sede",
                    "sedes": ["Central", "Norte", "Sur", "Este"],
                    "valores": [1500, 120, 85, 340],
                },
            },
            {
                "componente": "AlertaBanner",
                "props": {
                    "mensaje": "Sede Norte y Sede Sur con stock crítico (< 150 und.).",
                    "nivel": "error",
                },
            },
            {
                "componente": "RequisicionForm",
                "props": {
                    "medicamento": "Medicamento X",
                    "cantidad_sugerida": 500,
                    "sedes_afectadas": ["Norte", "Sur"],
                },
            },
        ]
    return [
        {
            "componente": "AlertaBanner",
            "props": {"mensaje": "No entendí la consulta. Intenta de nuevo.", "nivel": "info"},
        }
    ]


# ---------------------------------------------------------------------------
# Pipeline: mensaje → tool calls → componentes streamados
# ---------------------------------------------------------------------------


def pipeline_generative_ui(mensaje: str) -> Iterator[str]:
    """
    Genera componentes UI de forma incremental (simulando streaming).
    Cada yield es un bloque de UI listo para renderizar.
    """
    tool_calls = _simular_tool_calls(mensaje)

    for tc in tool_calls:
        time.sleep(0.08)  # simula latencia de generación

        nombre = tc["componente"]
        props = tc["props"]
        cls = REGISTRO_COMPONENTES.get(nombre)

        if cls is None:
            yield f"  ⚠️ Componente desconocido: {nombre!r}"
            continue

        instancia = cls(**props)
        yield f"\n[STREAM] Componente: {nombre}\n{instancia.renderizar()}"


# ---------------------------------------------------------------------------
# Flujo principal
# ---------------------------------------------------------------------------


def main():
    print("=" * 60)
    print("Módulo 02 – Ejemplo 03: Pipeline Generative UI completo")
    print("=" * 60)

    print(f"\nComponentes registrados: {list(REGISTRO_COMPONENTES.keys())}")

    mensaje = "Muéstrame la comparativa de stock del medicamento X"
    print(f"\nUsuario: {mensaje!r}")
    print("\n--- Iniciando stream de componentes ---")

    for bloque_ui in pipeline_generative_ui(mensaje):
        print(bloque_ui, flush=True)

    print("\n--- Stream finalizado ---")
    print("\n✅ Pipeline Generative UI completo demostrado.")


if __name__ == "__main__":
    main()

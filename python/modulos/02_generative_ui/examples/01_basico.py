#!/usr/bin/env python3
"""
Ejemplo 01 – Básico: Selección de componente según tipo de datos
Módulo 02: Generative UI

Muestra cómo el backend decide qué "componente" renderizar basándose
en la estructura de los datos devueltos por el agente.
"""

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Definición de componentes UI (en React serían JSX; aquí son dataclasses)
# ---------------------------------------------------------------------------


@dataclass
class ComponenteTexto:
    contenido: str

    def renderizar(self) -> str:
        return f"[TEXTO] {self.contenido}"


@dataclass
class ComponenteAlerta:
    mensaje: str
    nivel: str  # "info" | "warning" | "error"

    def renderizar(self) -> str:
        iconos = {"info": "ℹ️", "warning": "⚠️", "error": "❌"}
        icono = iconos.get(self.nivel, "•")
        return f"[ALERTA {self.nivel.upper()}] {icono} {self.mensaje}"


@dataclass
class ComponenteTabla:
    columnas: list[str]
    filas: list[list]

    def renderizar(self) -> str:
        encabezado = " | ".join(f"{c:<12}" for c in self.columnas)
        separador = "-" * len(encabezado)
        filas_str = "\n".join(" | ".join(f"{str(v):<12}" for v in fila) for fila in self.filas)
        return f"[TABLA]\n{encabezado}\n{separador}\n{filas_str}"


# ---------------------------------------------------------------------------
# Selector de componente (lógica Generative UI)
# ---------------------------------------------------------------------------


def seleccionar_componente(datos: dict):
    """
    Elige el componente adecuado según el tipo y contenido de los datos.

    En el SDK real (TypeScript):
        const ui = createStreamableUI();
        if (data.type === 'table') ui.update(<DataTable {...data} />);
    """
    tipo = datos.get("tipo")

    if tipo == "stock_tabla":
        return ComponenteTabla(
            columnas=["Sede", "Medicamento", "Unidades"],
            filas=datos["filas"],
        )
    elif tipo == "alerta_stock":
        return ComponenteAlerta(
            mensaje=datos["mensaje"],
            nivel=datos.get("nivel", "warning"),
        )
    else:
        return ComponenteTexto(contenido=datos.get("texto", str(datos)))


# ---------------------------------------------------------------------------
# Flujo principal
# ---------------------------------------------------------------------------


def main():
    print("=" * 60)
    print("Módulo 02 – Ejemplo 01: Selección de componente UI")
    print("=" * 60)

    respuestas_agente = [
        {
            "tipo": "stock_tabla",
            "filas": [
                ["Sede Central", "Medicamento X", 1500],
                ["Sede Norte", "Medicamento X", 120],
                ["Sede Sur", "Medicamento X", 85],
            ],
        },
        {
            "tipo": "alerta_stock",
            "mensaje": "Stock crítico en Sede Sur: menos de 100 unidades.",
            "nivel": "error",
        },
        {
            "tipo": "texto",
            "texto": "Se ha iniciado una requisición automática para Sede Sur.",
        },
    ]

    print("\nSimulando respuestas del agente y selección de componentes:\n")
    for i, respuesta in enumerate(respuestas_agente, 1):
        componente = seleccionar_componente(respuesta)
        print(f"Respuesta {i} → {type(componente).__name__}")
        print(componente.renderizar())
        print()

    print("✅ Selección de componentes según tipo de datos completada.")


if __name__ == "__main__":
    main()

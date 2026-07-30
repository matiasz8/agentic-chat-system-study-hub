#!/usr/bin/env python3
"""
Ejemplo 02 – Intermedio: Payloads estructurados y validación
Módulo 02: Generative UI

Muestra cómo estructurar los payloads que el backend envía al frontend
y cómo validarlos antes de renderizar el componente.
"""

import json
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Schema de validación (simulado sin Pydantic/zod)
# ---------------------------------------------------------------------------

ESQUEMAS = {
    "grafico_barras": {
        "campos_requeridos": ["titulo", "etiquetas", "valores"],
        "tipos": {"titulo": str, "etiquetas": list, "valores": list},
    },
    "tarjeta_producto": {
        "campos_requeridos": ["nombre", "precio", "stock"],
        "tipos": {"nombre": str, "precio": (int, float), "stock": int},
    },
    "formulario_requisicion": {
        "campos_requeridos": ["medicamento_id", "cantidad", "sede_destino"],
        "tipos": {"medicamento_id": str, "cantidad": int, "sede_destino": str},
    },
}


def validar_payload(tipo: str, datos: dict) -> list[str]:
    """
    Valida que el payload cumpla con el esquema del componente.
    Devuelve lista de errores (vacía = válido).

    Equivale a zod.parse() en TypeScript.
    """
    errores: list[str] = []
    esquema = ESQUEMAS.get(tipo)
    if esquema is None:
        errores.append(f"Tipo de componente desconocido: {tipo!r}")
        return errores

    for campo in esquema["campos_requeridos"]:
        if campo not in datos:
            errores.append(f"Campo requerido ausente: {campo!r}")

    for campo, tipo_esperado in esquema["tipos"].items():
        if campo in datos and not isinstance(datos[campo], tipo_esperado):
            errores.append(
                f"Campo {campo!r}: se esperaba {tipo_esperado}, "
                f"se recibió {type(datos[campo]).__name__}"
            )
    return errores


# ---------------------------------------------------------------------------
# Generador de payload estructurado
# ---------------------------------------------------------------------------


@dataclass
class PayloadUI:
    tipo_componente: str
    datos: dict
    valido: bool = field(init=False, default=False)
    errores: list[str] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.errores = validar_payload(self.tipo_componente, self.datos)
        self.valido = len(self.errores) == 0

    def serializar(self) -> str:
        """Simula la serialización JSON que se envía al frontend."""
        return json.dumps(
            {
                "componente": self.tipo_componente,
                "props": self.datos,
                "valido": self.valido,
            },
            ensure_ascii=False,
            indent=2,
        )


def construir_payload_desde_agente(intencion: str, contexto: dict) -> PayloadUI:
    """
    El agente LLM detecta la intención y construye el payload correcto.
    En producción, esta lógica viene del tool call del LLM.
    """
    if intencion == "ver_comparativa":
        return PayloadUI(
            tipo_componente="grafico_barras",
            datos={
                "titulo": "Comparativa de stock por sede",
                "etiquetas": contexto.get("sedes", []),
                "valores": contexto.get("stocks", []),
            },
        )
    elif intencion == "ver_producto":
        return PayloadUI(
            tipo_componente="tarjeta_producto",
            datos=contexto,
        )
    elif intencion == "crear_requisicion":
        return PayloadUI(
            tipo_componente="formulario_requisicion",
            datos=contexto,
        )
    else:
        return PayloadUI(tipo_componente="desconocido", datos={})


# ---------------------------------------------------------------------------
# Flujo principal
# ---------------------------------------------------------------------------


def main():
    print("=" * 60)
    print("Módulo 02 – Ejemplo 02: Payloads estructurados")
    print("=" * 60)

    casos = [
        (
            "ver_comparativa",
            {"sedes": ["Central", "Norte", "Sur"], "stocks": [1500, 120, 85]},
        ),
        (
            "ver_producto",
            {"nombre": "Medicamento X", "precio": 45.90, "stock": 1500},
        ),
        (
            "crear_requisicion",
            # Falta "sede_destino" → debe fallar validación
            {"medicamento_id": "MED-001", "cantidad": 200},
        ),
    ]

    for intencion, contexto in casos:
        payload = construir_payload_desde_agente(intencion, contexto)
        print(f"\nIntención: {intencion!r}")
        print(f"  Válido  : {payload.valido}")
        if payload.errores:
            for error in payload.errores:
                print(f"  ❌ {error}")
        else:
            print(f"  JSON    :\n{payload.serializar()}")

    print("\n✅ Payloads estructurados y validación demostrados.")


if __name__ == "__main__":
    main()
